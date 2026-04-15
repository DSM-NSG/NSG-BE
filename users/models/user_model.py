import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, student_id, password=None, **extra_fields):
        if not student_id:
            raise ValueError("student_id는 필수입니다.")
        user = self.model(student_id=student_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """사용자 계정 모델"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    student_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="학번",
        help_text="학년-반-번호 형식 (예: 1-2-3)"
    )
    grade = models.IntegerField(
        verbose_name="학년",
        help_text="학년 (1~3)"
    )
    class_num = models.IntegerField(
        verbose_name="반",
        help_text="반 번호"
    )
    num = models.IntegerField(
        verbose_name="번호",
        help_text="번호"
    )
    name = models.CharField(
        max_length=100,
        verbose_name="이름"
    )
    cohort = models.IntegerField(
        verbose_name="기수",
        help_text="대마고 기수"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="활성 여부"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="가입일"
    )

    USERNAME_FIELD = 'student_id'
    REQUIRED_FIELDS = ['grade', 'class_num', 'num', 'name', 'cohort']

    objects = UserManager()

    class Meta:
        db_table = 'user'
        verbose_name = '사용자'
        verbose_name_plural = '사용자'
        indexes = [
            models.Index(fields=['cohort']),
        ]
        unique_together = [['grade', 'class_num', 'num']]

    def __str__(self):
        return f"{self.grade}학년 {self.class_num}반 {self.num}번 {self.name}"
