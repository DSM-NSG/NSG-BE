import uuid
from django.db import models


class Like(models.Model):
    """좋아요 모델 - 게시글 전용"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='likes',
        verbose_name="좋아요 누른 사용자"
    )
    post = models.ForeignKey(
        'posts.Post',
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name="좋아요 대상 게시글"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="좋아요 생성일"
    )

    class Meta:
        db_table = 'like'
        verbose_name = '좋아요'
        verbose_name_plural = '좋아요'
        unique_together = [['user', 'post']]
        indexes = [
            models.Index(fields=['post']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        user_display = self.user.name if self.user else "탈퇴한 사용자"
        return f"{user_display} -> {self.post.title}"
