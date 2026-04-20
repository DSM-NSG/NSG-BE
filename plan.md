# 기능 계획서 — S3 이미지 업로드 API

> 이 파일은 새 기능 개발 전 작성되며, 사용자 검토 후 구현을 시작합니다.

---

## 기능 개요

게시글 작성 시 첨부할 이미지를 S3에 업로드하고 URL을 반환하는 API를 만든다.
클라이언트는 이 URL을 게시글 생성 API의 `image_urls` 필드에 담아 전송한다.

---

## 변경 파일 목록

### 신규 생성
- `images/` — 새 Django 앱
  - `images/__init__.py`
  - `images/apps.py`
  - `images/apis/views.py` — `ImageUploadView`
  - `images/apis/serializers.py` — 요청/응답 시리얼라이저
  - `images/apis/urls.py` — URL 등록
  - `images/service/image_service.py` — S3 업로드 로직

### 수정
- `requirements.txt` — `boto3` 추가
- `config/config/settings.py` — S3 환경변수 로드
- `config/config/urls.py` — images 앱 URL 포함
- `.env.example` — S3 환경변수 항목 추가

### 마이그레이션
없음 (모델 변경 없음)

---

## API 엔드포인트

| Method | 경로 | 인증 | 설명 |
|--------|------|------|------|
| POST | `/images/upload/` | 필요 | 이미지 S3 업로드 후 URL 반환 |

### 요청 (multipart/form-data)
```
image: <파일>   # 필수, 이미지 파일 (jpg/jpeg/png/gif/webp)
```

### 응답 (200 OK)
```json
{
  "url": "https://<bucket>.s3.<region>.amazonaws.com/images/<uuid>.<ext>"
}
```

### 에러 응답
| 상황 | 상태코드 | 메시지 |
|------|----------|--------|
| 파일 없음 | 400 | "이미지 파일을 첨부해주세요." |
| 허용되지 않는 확장자 | 400 | "지원하지 않는 파일 형식입니다." |

---

## 서비스 로직 (`image_service.py`)

1. 파일 확장자 검증 (jpg, jpeg, png, gif, webp만 허용)
2. 파일명: `images/{uuid4}.{ext}` 로 S3 키 생성 (중복 방지)
3. boto3로 S3에 업로드 (`put_object`, `ContentType` 설정)
4. 업로드된 파일의 public URL 반환
   - `https://{bucket}.s3.{region}.amazonaws.com/images/{uuid}.{ext}`

---

## 구현 순서

1. [x] `boto3` 추가 (`requirements.txt`)
2. [x] S3 환경변수 추가 (`settings.py`, `.env.example`)
3. [x] `images` 앱 생성 (디렉토리 및 기본 파일)
4. [x] `image_service.py` — S3 업로드 로직
5. [x] `serializers.py` — 요청/응답 시리얼라이저
6. [x] `views.py` — `ImageUploadView`
7. [x] `urls.py` + `config/urls.py` 등록
8. [x] `settings.py` INSTALLED_APPS에 `images` 추가

---

## 고려사항

- **인증**: `IsAuthenticated` 필수 (로그인한 유저만 업로드 가능)
- **버킷 공개 설정**: S3 버킷에서 퍼블릭 읽기 허용 필요 (또는 CloudFront 사용)
- **파일 크기**: 서비스 레이어에서 10MB 제한
- **S3 키**: `images/{uuid}.{ext}` 형태로 저장

---

## 상태

- [x] 작성 완료
- [x] 사용자 검토 중
- [x] 승인됨
- [x] 구현 완료
