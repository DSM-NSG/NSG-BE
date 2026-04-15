import uuid
from django.db import models


class Major(models.Model):
    """전공 카테고리 모델"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    major = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="전공 카테고리"
    )

    class Meta:
        db_table = 'major'
        verbose_name = '전공'
        verbose_name_plural = '전공'
        ordering = ['major']

    def __str__(self):
        return self.major
