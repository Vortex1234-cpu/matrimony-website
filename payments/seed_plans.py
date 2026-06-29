from payments.models import Plan

def seed():
    # Free Plan
    Plan.objects.update_or_create(
        name='free',
        defaults={
            'price': 0,
            'duration_days': 36500,
            'can_send_interest': True,
            'can_view_contact': False,
            'can_message': False,
            'max_interests_per_week': 3,
            'description': 'Basic free plan'
        }
    )

    # Silver Plan
    Plan.objects.update_or_create(
        name='silver',
        defaults={
            'price': 999,
            'duration_days': 90,
            'can_send_interest': True,
            'can_view_contact': True,
            'can_message': False,
            'max_interests_per_week': 30,
            'description': 'Silver plan'
        }
    )

    # Gold Plan
    Plan.objects.update_or_create(
        name='gold',
        defaults={
            'price': 1999,
            'duration_days': 180,
            'can_send_interest': True,
            'can_view_contact': True,
            'can_message': True,
            'max_interests_per_week': 999,
            'description': 'Gold plan'
        }
    )

    print("✅ Plans seeded successfully!")