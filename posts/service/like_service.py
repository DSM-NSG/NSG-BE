from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404

from posts.models import Post, Like


def toggle_like(*, user, post_id):
    post = get_object_or_404(Post, id=post_id)
    with transaction.atomic():
        like = Like.objects.filter(post=post, user=user).first()
        if like:
            like.delete()
            Post.objects.filter(id=post_id).update(like_count=F('like_count') - 1)
            is_liked = False
        else:
            Like.objects.create(post=post, user=user)
            Post.objects.filter(id=post_id).update(like_count=F('like_count') + 1)
            is_liked = True
        post.refresh_from_db()
        return is_liked, post.like_count
