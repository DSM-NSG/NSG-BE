import uuid
from django.db import models


class Comment(models.Model):
    """댓글/대댓글 모델

    parent_id가 NULL이면 댓글, 값이 있으면 대댓글
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    author = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='comments',
        verbose_name="작성자"
    )
    post = models.ForeignKey(
        'posts.Post',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="대상 게시글"
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name="부모 댓글",
        help_text="대댓글일 경우 작성"
    )
    content = models.TextField(
        verbose_name="내용"
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
        db_table = 'comment'
        verbose_name = '댓글'
        verbose_name_plural = '댓글'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post', 'created_at']),
            models.Index(fields=['parent']),
        ]

    def __str__(self):
        if self.parent:
            return f"[대댓글] {self.content[:20]}..."
        return f"[댓글] {self.content[:20]}..."

    def is_reply(self):
        """대댓글 여부 확인"""
        return self.parent is not None
