<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-22 | Updated: 2026-04-22 -->

# images

## Purpose
이미지 업로드 Django 앱. 게시글/장소에 첨부할 이미지를 AWS S3에 업로드하고 URL을 반환한다. 모델 없이 API와 서비스 레이어만 존재하며, 업로드된 이미지 URL은 `posts.PostImage` 등 다른 모델에서 참조한다.

## Key Files

| File | Description |
|------|-------------|
| `apps.py` | Django 앱 설정 (`ImagesConfig`) |
| `__init__.py` | 패키지 초기화 |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `apis/` | 이미지 업로드 API 뷰, URL, 시리얼라이저 (see `apis/AGENTS.md`) |
| `service/` | S3 업로드 비즈니스 로직 (see `service/AGENTS.md`) |

## For AI Agents

### Working In This Directory
- 이 앱은 DB 모델 없음 — 이미지 메타데이터는 다른 앱에서 관리
- 허용 확장자: `jpg`, `jpeg`, `png`, `gif`, `webp`
- 최대 파일 크기: 10MB
- S3 키 패턴: `images/{uuid}.{ext}`

### Common Patterns
- S3 URL 형식: `https://{bucket}.s3.{region}.amazonaws.com/images/{uuid}.{ext}`
- 인증된 사용자만 업로드 가능 (JWT 필요)

## Dependencies

### Internal
- `config.exceptions` — `CustomAPIException` (파일 형식/크기 오류)
- `posts.PostImage` — 업로드된 URL을 저장하는 모델

### External
- `boto3` — AWS S3 클라이언트
- `Pillow` — 이미지 처리 (필요시)

<!-- MANUAL: -->
