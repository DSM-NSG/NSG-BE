from django.shortcuts import get_object_or_404

from places.models import Place


def create_place(*, user, title, description, category, latitude, longitude, naver_map_url=None, is_anonymous=False):
    return Place.objects.create(
        author=user,
        title=title,
        description=description,
        category=category,
        latitude=latitude,
        longitude=longitude,
        naver_map_url=naver_map_url,
        is_anonymous=is_anonymous,
    )


def delete_place(*, user, place_id):
    place = get_object_or_404(Place, id=place_id)
    if place.author != user:
        raise PermissionError()
    place.delete()
