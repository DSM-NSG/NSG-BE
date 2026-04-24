from django.contrib.auth.hashers import make_password
from django.db import transaction


def withdraw_user(user):
    with transaction.atomic():
        user.is_active = False
        user.name = "알 수 없는 사용자"
        user.account_id = None
        user.student_id = f"withdrawn_{user.id}"
        user.password_hash = make_password(None)
        user.save(update_fields=[
            'is_active', 'name', 'account_id', 'student_id', 'password_hash'
        ])
