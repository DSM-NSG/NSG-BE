import uuid
from django.db import models


class PostAnonymousUser(models.Model):
    """게시글 내 익명 번호 매핑 모델

    익명 작성자가 같은 게시글에 댓글을 달아도 동일한 익명 번호 유지
    (post_id, user_id) unique 제약 필요
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    post = models.ForeignKey(
        'posts.Post',
        on_delete=models.CASCADE,
        related_name='anonymous_users',
        verbose_name="게시글"
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='anonymous_mappings',
        verbose_name="실제 사용자"
    )
    anonymous_number = models.IntegerField(
        verbose_name="게시글 내 익명 순번",
        help_text="1부터 증가"
    )

    class Meta:
        db_table = 'post_anonymous_user'
        verbose_name = '게시글 익명 사용자'
        verbose_name_plural = '게시글 익명 사용자'
        indexes = [
            models.Index(fields=['post', 'user']),
        ]

    def __str__(self):
        return f"{self.post.title} - 익명{self.anonymous_number}"
