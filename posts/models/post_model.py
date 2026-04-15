import uuid
from django.db import models


class Post(models.Model):
    """통합 게시글 모델 - 꿀팁(TIP)과 전공(MAJOR) 게시글"""

    POST_TYPE_CHOICES = [
        ('TIP', '꿀팁'),
        ('MAJOR', '전공'),
    ]

    TIP_CATEGORY_CHOICES = [
        ('PLACE', '장소'),
        ('DORM_LIFE', '기숙사생활'),
        ('SCHOOL_LIFE', '대마고생활'),
        ('ETC', '기타'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    author = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        verbose_name="작성자"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="제목"
    )
    body = models.TextField(
        verbose_name="내용"
    )
    post_type = models.CharField(
        max_length=10,
        choices=POST_TYPE_CHOICES,
        verbose_name="게시글 유형"
    )
    category = models.CharField(
        max_length=20,
        choices=TIP_CATEGORY_CHOICES,
        blank=True,
        verbose_name="카테고리",
        help_text="TIP: 장소/기숙사생활/대마고생활/기타, MAJOR: MajorTag로 관리"
    )
    place = models.ForeignKey(
        'places.Place',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name="태그된 장소",
        help_text="TIP 전용, nullable"
    )
    is_anonymous = models.BooleanField(
        default=False,
        verbose_name="익명 여부"
    )
    like_count = models.IntegerField(
        default=0,
        verbose_name="좋아요 수"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="작성일"
    )

    class Meta:
        db_table = 'post'
        verbose_name = '게시글'
        verbose_name_plural = '게시글'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post_type', '-created_at']),
            models.Index(fields=['category']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"[{self.get_post_type_display()}] {self.title}"
