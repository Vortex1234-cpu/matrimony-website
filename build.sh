#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

# Auto create superuser
python manage.py shell << 'EOF'
import os
from django.contrib.auth import get_user_model
User = get_user_model()

username = os.environ.get('DJANGO_ADMIN_USERNAME', 'admin')
email = os.environ.get('DJANGO_ADMIN_EMAIL', 'admin.matrimonyinfo@gmail.com')
password = os.environ.get('DJANGO_ADMIN_PASSWORD', 'K@r@n@772004')
phone = os.environ.get('DJANGO_ADMIN_PHONE', '6374247042')

try:
    if not User.objects.filter(username=username).exists():
        user = User(
            username=username,
            email=email,
            phone=phone,
            first_name='Admin',
            is_staff=True,
            is_superuser=True,
            is_active=True,
            is_verified=True,
        )
        user.set_password(password)
        user.save()
        print('Admin created successfully')
    else:
        # Update existing admin password
        user = User.objects.get(username=username)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        print('Admin password updated')
except Exception as e:
    print(f'Admin error: {e}')
EOF

# Seed plans
python manage.py shell << 'EOF'
try:
    from payments.models import Plan
    if not Plan.objects.exists():
        Plan.objects.create(
            name='free', price=0,
            duration_days=36500,
            can_send_interest=True,
            can_view_contact=False,
            can_message=False,
            max_interests_per_week=3,
        )
        Plan.objects.create(
            name='silver', price=999,
            duration_days=90,
            can_send_interest=True,
            can_view_contact=True,
            can_message=False,
            max_interests_per_week=30,
        )
        Plan.objects.create(
            name='gold', price=1999,
            duration_days=180,
            can_send_interest=True,
            can_view_contact=True,
            can_message=True,
            max_interests_per_week=999,
        )
        print('Plans seeded')
    else:
        print('Plans exist')
except Exception as e:
    print(f'Plans error: {e}')
EOF