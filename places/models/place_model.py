import uuid
from django.db import models


class Place(models.Model):
    """장소 공유 모델"""

    CATEGORY_CHOICES = [
        ('RESTAURANT', '맛집'),
        ('CAFE', '카페'),
        ('PC_ROOM', 'PC방'),
        ('KARAOKE', '노래방'),
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
        related_name='places',
        verbose_name="작성자"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="장소명"
    )
    description = models.TextField(
        verbose_name="설명"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        verbose_name="카테고리"
    )
    latitude = models.FloatField(
        verbose_name="위도"
    )
    longitude = models.FloatField(
        verbose_name="경도"
    )
    naver_map_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="네이버지도 링크"
    )
    is_anonymous = models.BooleanField(
        default=False,
        verbose_name="익명 여부"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="작성일"
    )

    class Meta:
        db_table = 'place'
        verbose_name = '장소'
        verbose_name_plural = '장소'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"
