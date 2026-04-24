<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-22 | Updated: 2026-04-22 -->

# images/service

## Purpose
이미지 업로드 비즈니스 로직 레이어. 파일 확장자/크기 검증 후 AWS S3에 업로드하고 공개 URL을 반환한다.

## Key Files

| File | Description |
|------|-------------|
| `image_service.py` | `ImageService.upload(file)` — 확장자/크기 검증, S3 업로드, URL 반환 |
| `__init__.py` | 패키지 초기화 |

## For AI Agents

### Working In This Directory
- 허용 확장자: `{"jpg", "jpeg", "png", "gif", "webp"}`
- 최대 크기: 10MB (`MAX_FILE_SIZE = 10 * 1024 * 1024`)
- S3 키: `images/{uuid4}.{ext}`
- S3 클라이언트는 `settings.AWS_ACCESS_KEY`, `AWS_SECRET_KEY`, `AWS_STATIC`(region) 사용
- URL 형식: `https://{AWS_BUCKET}.s3.{AWS_STATIC}.amazonaws.com/images/{uuid}.{ext}`
- 검증 실패 시 `CustomAPIException` raise (한국어 메시지)

### Common Patterns
- `@staticmethod` 패턴
- 파일 확장자 추출: `file.name.rsplit(".", 1)[-1].lower()`
- `boto3.client("s3").upload_fileobj(file, bucket, key, ExtraArgs={"ContentType": ...})`

## Dependencies

### Internal
- `config.exceptions.CustomAPIException`

### External
- `boto3` — AWS S3 SDK
- `django.conf.settings` — AWS 자격증명

<!-- MANUAL: -->
