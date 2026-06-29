from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
from .models import Plan, Subscription
import logging
import requests
import uuid

logger = logging.getLogger(__name__)


# =============================================
# PLANS PAGE — Public (no login required)
# =============================================
def plans_page(request):
    try:
        plans = Plan.objects.all().order_by('price')
        if not plans.exists():
            _seed_plans()
            plans = Plan.objects.all().order_by('price')

        current_subscription = None
        if request.user.is_authenticated:
            current_subscription = Subscription.objects.filter(
                user=request.user,
                status='active',
                end_date__gt=timezone.now()
            ).first()

        return render(request, 'payments/plans.html', {
            'plans': plans,
            'current_subscription': current_subscription,
           'razorpay_key': getattr(settings, 'RAZORPAY_KEY_ID', ''),
        })
    except Exception as e:
        logger.error(f'Plans page error: {e}')
        return render(request, 'payments/plans.html', {
            'plans': [],
            'current_subscription': None,
            'razorpay_key': '',
        })

# =============================================
# CREATE ORDER — Cashfree
# =============================================

@login_required
def create_order(request, plan_id):
    try:
        plan = get_object_or_404(Plan, id=plan_id)

        app_id = settings.CASHFREE_APP_ID
        secret_key = settings.CASHFREE_SECRET_KEY

        if not app_id or not secret_key:
            messages.error(request, '❌ Payment gateway not configured.')
            return redirect('plans_page')

        order_id = f"order_{request.user.id}_{plan.id}_{uuid.uuid4().hex[:8]}"

        base_url = (
            "https://sandbox.cashfree.com/pg/orders"
            if settings.CASHFREE_ENV == 'TEST'
            else "https://api.cashfree.com/pg/orders"
        )

        headers = {
            "x-client-id": app_id,
            "x-client-secret": secret_key,
            "x-api-version": "2023-08-01",
            "Content-Type": "application/json",
        }

        payload = {
            "order_id": order_id,
            "order_amount": float(plan.price),
            "order_currency": "INR",
            "customer_details": {
                "customer_id": str(request.user.id),
                "customer_name": request.user.first_name or request.user.username,
                "customer_email": request.user.email or "noemail@example.com",
                "customer_phone": request.user.phone or "9999999999",
            },
            "order_meta": {
                "return_url": (
                    f"{settings.SITE_URL}/payments/payment-success/"
                    f"?order_id={{order_id}}&plan_id={plan.id}"
                ),
            },
        }

        response = requests.post(base_url, json=payload, headers=headers)
        data = response.json()

        if response.status_code not in (200, 201):
            logger.error(f'Cashfree order error: {data}')
            messages.error(request, '❌ Could not create payment order.')
            return redirect('plans_page')

        payment_session_id = data.get('payment_session_id')

        cashfree_mode = (
            "sandbox" if settings.CASHFREE_ENV == 'TEST' else "production"
        )

        return render(request, 'payments/checkout.html', {
            'plan': plan,
            'payment_session_id': payment_session_id,
            'order_id': order_id,
            'cashfree_env': cashfree_mode,
        })

    except Exception as e:
        logger.error(f'Create order error: {e}')
        messages.error(request, f'❌ Payment error: {str(e)}')
        return redirect('plans_page')
    
# =============================================
# PAYMENT SUCCESS
# =============================================
@login_required
def payment_success(request):
    try:
        order_id = request.GET.get('order_id', '')
        plan_id = request.GET.get('plan_id', '')

        if not order_id or not plan_id:
            messages.error(request, '❌ Missing payment details.', extra_tags='payment_modal')
            return redirect('plans_page')

        plan = get_object_or_404(Plan, id=plan_id)

        base_url = (
            f"https://sandbox.cashfree.com/pg/orders/{order_id}"
            if settings.CASHFREE_ENV == 'TEST'
            else f"https://api.cashfree.com/pg/orders/{order_id}"
        )
        headers = {
            "x-client-id": settings.CASHFREE_APP_ID,
            "x-client-secret": settings.CASHFREE_SECRET_KEY,
            "x-api-version": "2023-08-01",
        }
        response = requests.get(base_url, headers=headers)
        data = response.json()

        if data.get('order_status') != 'PAID':
            messages.error(
                request,
                '❌ Payment not completed.',
                extra_tags='payment_modal'
            )
            return redirect('payment_failed')

        Subscription.objects.filter(
            user=request.user, status='active'
        ).update(status='expired')

        from datetime import timedelta
        subscription = Subscription.objects.create(
            user=request.user,
            plan=plan,
            status='active',
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=plan.duration_days),
            razorpay_order_id=order_id,  # reuse field for cashfree order id
            amount_paid=plan.price,
        )

        try:
            profile = request.user.profile
            profile.is_premium = True
            profile.save()
        except Exception:
            pass

        messages.success(
            request,
            f'🎉 Payment successful! {plan.name} plan active until '
            f'{subscription.end_date.strftime("%d %B %Y")}.',
            extra_tags='payment_modal'
        )
        return redirect('my_plan')

    except Exception as e:
        logger.error(f'Payment success error: {e}')
        messages.error(request, f'❌ Error: {str(e)}', extra_tags='payment_modal')
        return redirect('plans_page')
    
# =============================================
# PAYMENT FAILED
# =============================================
@login_required
def payment_failed(request):
    messages.error(
        request,
        '❌ Payment was not completed. '
        'Please try again or contact support.',
        extra_tags='payment_modal'
    )
    return render(request, 'payments/payment_failed.html')


# =============================================
# MY PLAN
# =============================================
@login_required
def my_plan(request):
    try:
        subscription = Subscription.objects.filter(
            user=request.user,
            status='active',
            end_date__gt=timezone.now()
        ).first()

        expired_subscriptions = Subscription.objects.filter(
            user=request.user,
            status='expired'
        ).order_by('-end_date')[:5]

        return render(request, 'payments/my_plan.html', {
            'subscription': subscription,
            'expired_subscriptions': expired_subscriptions,
        })
    except Exception as e:
        logger.error(f'My plan error: {e}')
        messages.error(request, f'Error: {str(e)}')
        return redirect('dashboard')


# =============================================
# SEED PLANS HELPER
# =============================================
def _seed_plans():
    try:
        if not Plan.objects.exists():
            Plan.objects.create(
                name='free',
                price=0,
                duration_days=36500,
                can_send_interest=True,
                can_view_contact=False,
                can_message=False,
                max_interests_per_week=3,
            )
            Plan.objects.create(
                name='silver',
                price=999,
                duration_days=90,
                can_send_interest=True,
                can_view_contact=True,
                can_message=False,
                max_interests_per_week=30,
            )
            Plan.objects.create(
                name='gold',
                price=1999,
                duration_days=180,
                can_send_interest=True,
                can_view_contact=True,
                can_message=True,
                max_interests_per_week=999,
            )
            logger.info('Plans seeded successfully')
    except Exception as e:
        logger.error(f'Seed plans error: {e}')