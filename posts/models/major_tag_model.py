import uuid
from django.db import models


class MajorTag(models.Model):
    """전공 태그 모델 - 게시글과 전공 간의 다대다 관계"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    post = models.ForeignKey(
        'posts.Post',
        on_delete=models.CASCADE,
        related_name='major_tags',
        verbose_name="대상 게시글"
    )
    major = models.ForeignKey(
        'posts.Major',
        on_delete=models.CASCADE,
        related_name='major_tags',
        verbose_name="대상 전공"
    )

    class Meta:
        db_table = 'major_tag'
        verbose_name = '전공 태그'
        verbose_name_plural = '전공 태그'
        unique_together = [['post', 'major']]
        indexes = [
            models.Index(fields=['post']),
            models.Index(fields=['major']),
        ]

    def __str__(self):
        return f"{self.post.title} - {self.major.major}"
