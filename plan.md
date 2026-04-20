# 기능 계획서 — 마이페이지 API

> 이 파일은 새 기능 개발 전 작성되며, 사용자 검토 후 구현을 시작합니다.

---

## 기능 개요

Access Token을 통해 현재 로그인한 사용자의 기본 정보(user_id, 학년, 반, 번호, 기수)를 반환하는 마이페이지 조회 API를 추가한다.

---

## 변경 파일 목록

### 수정
- `users/apis/views.py` — `MyPageView` 추가
- `users/apis/serializer.py` — `MyPageSerializer` 추가
- `users/apis/urls.py` — `/users/me/` 경로 등록

### 신규 생성
없음 (모델 변경 없음, 마이그레이션 불필요)

---

## 모델 변경

없음. 기존 `User` 모델의 필드만 사용:
- `id` (UUID)
- `grade` (Integer)
- `class_num` (Integer)
- `num` (Integer)
- `cohort` (Integer, nullable)

---

## API 엔드포인트

| Method | 경로 | 인증 | 설명 |
|--------|------|------|------|
| GET | `/users/me/` | 필요 (Bearer JWT) | 내 정보 조회 |

### 요청 헤더
```
Authorization: Bearer <access_token>
```

### 응답 스키마 (200 OK)
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "grade": 2,
  "class_num": 1,
  "num": 15,
  "cohort": 9
}
```

### 에러 응답
| 상황 | 상태코드 | 메시지 |
|------|----------|--------|
| 토큰 없음 / 만료 | 401 | DRF 기본 처리 |

---

## 서비스 로직

서비스 레이어 없이 뷰에서 직접 처리 (단순 조회이므로).
- `request.user`에서 인증된 유저 객체를 그대로 직렬화하여 반환

---

## 구현 순서

1. [x] `MyPageSerializer` 작성 (`users/apis/serializer.py`)
2. [x] `MyPageView` 작성 (`users/apis/views.py`) — `RetrieveAPIView` 또는 `APIView`
3. [x] URL 등록 (`users/apis/urls.py`)

---

## 고려사항

- **인증**: `IsAuthenticated` 퍼미션 클래스 적용 필수
- **cohort**: nullable 필드이므로 응답에 `null` 포함 가능
- **서비스 레이어**: 비즈니스 로직이 없는 단순 조회라 뷰에서 직접 처리

---

## 상태

- [x] 작성 완료
- [x] 사용자 검토 중
- [x] 승인됨
- [x] 구현 완료
