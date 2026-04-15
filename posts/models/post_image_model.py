import uuid
from django.db import models


class PostImage(models.Model):
    """게시글 첨부 이미지 모델 - 순서 보장"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    post = models.ForeignKey(
        'posts.Post',
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="연결된 게시글"
    )
    image_url = models.URLField(
        max_length=500,
        verbose_name="이미지 URL"
    )
    order_index = models.IntegerField(
        verbose_name="이미지 표시 순서",
        help_text="0부터 시작하는 순서"
    )

    class Meta:
        db_table = 'post_image'
        verbose_name = '게시글 이미지'
        verbose_name_plural = '게시글 이미지'
        ordering = ['post', 'order_index']
        indexes = [
            models.Index(fields=['post', 'order_index']),
        ]
        unique_together = [['post', 'order_index']]

    def __str__(self):
        return f"{self.post.title} - 이미지 {self.order_index}"
