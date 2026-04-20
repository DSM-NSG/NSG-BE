import uuid

import boto3
from django.conf import settings

from config.exceptions import CustomAPIException

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


class ImageService:
    @staticmethod
    def upload(file) -> str:
        ext = file.name.rsplit(".", 1)[-1].lower()

        if ext not in ALLOWED_EXTENSIONS:
            raise CustomAPIException("지원하지 않는 파일 형식입니다.")

        if file.size > MAX_FILE_SIZE:
            raise CustomAPIException("파일 크기는 10MB를 초과할 수 없습니다.")

        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
            region_name=settings.AWS_STATIC,
        )

        key = f"images/{uuid.uuid4()}.{ext}"
        s3.upload_fileobj(
            file,
            settings.AWS_BUCKET,
            key,
            ExtraArgs={"ContentType": file.content_type},
        )

        url = f"https://{settings.AWS_BUCKET}.s3.{settings.AWS_STATIC}.amazonaws.com/{key}"
        return url
