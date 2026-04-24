<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-22 | Updated: 2026-04-22 -->

# images/apis

## Purpose
이미지 업로드 API 레이어. 파일을 받아 S3에 업로드하고 URL을 반환하는 단일 엔드포인트를 제공한다.

## Key Files

| File | Description |
|------|-------------|
| `views.py` | `ImageUploadView` — multipart/form-data 파일 수신, ImageService 호출, URL 반환 |
| `urls.py` | `images/` 경로 하위 URL 패턴 |
| `serializers.py` | 업로드 요청/응답 직렬화 |

## For AI Agents

### Working In This Directory
- URL prefix: `images/` (루트 urls.py: `path('images/', include('images.apis.urls'))`)
- 요청: `Content-Type: multipart/form-data`, `file` 필드
- 응답: `{"url": "https://...s3.amazonaws.com/images/{uuid}.{ext}"}`
- 인증 필요: `permission_classes = [IsAuthenticated]`

### Common Patterns
- `request.FILES['file']`로 파일 접근
- 서비스 호출: `ImageService.upload(file)` → URL 반환

## Dependencies

### Internal
- `images/service/image_service.py`

<!-- MANUAL: -->
