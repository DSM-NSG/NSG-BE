from django.db import transaction
from django.shortcuts import get_object_or_404

from posts.models import Post, Comment
from posts.service.post_service import get_or_create_anonymous_number


def create_comment(*, user, post_id, content, is_anonymous):
    post = get_object_or_404(Post, id=post_id)
    with transaction.atomic():
        comment = Comment.objects.create(
            author=user,
            post=post,
            content=content,
            is_anonymous=is_anonymous,
        )
        if is_anonymous:
            get_or_create_anonymous_number(post, user)
        return comment


def create_reply(*, user, post_id, comment_id, content, is_anonymous):
    post = get_object_or_404(Post, id=post_id)
    parent = get_object_or_404(Comment, id=comment_id, post=post, parent=None)
    with transaction.atomic():
        reply = Comment.objects.create(
            author=user,
            post=post,
            parent=parent,
            content=content,
            is_anonymous=is_anonymous,
        )
        if is_anonymous:
            get_or_create_anonymous_number(post, user)
        return reply


def delete_comment(*, user, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    if comment.author != user:
        raise PermissionError()
    comment.delete()
