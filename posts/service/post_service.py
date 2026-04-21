from collections import defaultdict

from django.db import transaction
from django.db.models import F, Max
from django.shortcuts import get_object_or_404
from django.utils import timezone as django_timezone

from posts.models import Post, PostImage, PostAnonymousUser, MajorTag


def get_or_create_anonymous_number(post, user):
    """게시글 내 익명 순번 조회 또는 생성 (race condition 방지를 위해 transaction + select_for_update 사용)"""
    with transaction.atomic():
        mapping = PostAnonymousUser.objects.select_for_update().filter(post=post, user=user).first()
        if not mapping:
            max_num = (
                PostAnonymousUser.objects.filter(post=post)
                .aggregate(max=Max('anonymous_number'))['max'] or 0
            )
            mapping = PostAnonymousUser.objects.create(
                post=post, user=user, anonymous_number=max_num + 1
            )
        return mapping.anonymous_number


def create_tip(*, user, title, body, category, is_anonymous, place_id=None, image_urls=None):
    with transaction.atomic():
        post = Post.objects.create(
            author=user,
            title=title,
            body=body,
            post_type='TIP',
            category=category,
            place_id=place_id,
            is_anonymous=is_anonymous,
        )
        if is_anonymous:
            get_or_create_anonymous_number(post, user)
        if image_urls:
            PostImage.objects.bulk_create([
                PostImage(post=post, image_url=url, order_index=i)
                for i, url in enumerate(image_urls)
            ])
        return post


def create_major_post(*, user, title, body, major_ids, is_anonymous, image_urls=None):
    with transaction.atomic():
        post = Post.objects.create(
            author=user,
            title=title,
            body=body,
            post_type='MAJOR',
            category='',
            is_anonymous=is_anonymous,
        )
        if is_anonymous:
            get_or_create_anonymous_number(post, user)
        MajorTag.objects.bulk_create([
            MajorTag(post=post, major_id=major_id)
            for major_id in major_ids
        ])
        if image_urls:
            PostImage.objects.bulk_create([
                PostImage(post=post, image_url=url, order_index=i)
                for i, url in enumerate(image_urls)
            ])
        return post


def get_popular_major_tags(*, top_n=10):
    """
    인기 전공 태그 top_n개 반환.
    점수 = Σ (1.0 + like_count × 2.0) × 1 / (1 + 경과일수 × 0.1)
    """
    major_tags = (
        MajorTag.objects
        .filter(post__post_type='MAJOR')
        .select_related('major', 'post')
        .only('major__id', 'major__major', 'post__id', 'post__like_count', 'post__created_at')
    )

    now = django_timezone.now()
    scores = defaultdict(lambda: {'major': None, 'score': 0.0, 'post_count': 0, 'total_likes': 0})

    for mt in major_tags:
        post = mt.post
        days_elapsed = (now - post.created_at).total_seconds() / 86400
        decay = 1.0 / (1.0 + days_elapsed * 0.1)
        post_score = (1.0 + post.like_count * 2.0) * decay

        entry = scores[mt.major_id]
        entry['major'] = mt.major
        entry['score'] += post_score
        entry['post_count'] += 1
        entry['total_likes'] += post.like_count

    ranked = sorted(scores.values(), key=lambda x: x['score'], reverse=True)
    return ranked[:top_n]


def delete_post(*, user, post_id, post_type):
    post = get_object_or_404(Post, id=post_id, post_type=post_type)
    if post.author != user:
        raise PermissionError()
    post.delete()
