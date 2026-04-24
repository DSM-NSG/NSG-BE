# 회원탈퇴 기능 구현 계획

## 기능 개요
유저가 회원탈퇴를 요청하면 계정을 비활성화하고 개인정보를 익명화한다.
유저 행(row)은 삭제하지 않고 유지한다.

---

## 핵심 설계 결정: Soft Delete + PII 초기화

### 왜 삭제하지 않는가
현재 FK 구조상 User 행을 실제로 삭제하면 `SET_NULL`이 동작해
Post/Comment/Place/Like/PostAnonymousUser의 author가 모두 null이 된다.
콘텐츠는 남지만 작성자 정보가 완전히 소실되므로 채택하지 않는다.

### 채택 방식: is_active=False + PII 초기화

| 필드 | 처리 |
|------|------|
| `is_active` | `False` → JWT 인증 즉시 차단 |
| `name` | `"탈퇴한 사용자"` |
| `account_id` | `None` (이미 nullable) |
| `student_id` | `f"withdrawn_{user.id}"` (unique 제약 유지) |
| `password_hash` | `make_password(None)` — unusable password |
| grade, class_num, num, cohort | **유지** (이름 없이 식별 불가) |

### JWT 토큰 무효화
`token_blacklist` 미설치 상태이지만 별도 설정 불필요.
SimpleJWT 기본 인증 규칙이 `user.is_active`를 체크하므로
`is_active=False` 설정만으로 기존 토큰이 즉시 거부된다.

### 기존 콘텐츠 처리
| Entity | on_delete | 처리 방식 |
|--------|-----------|---------|
| Post | SET_NULL | **유지** — author FK 그대로, 익명화된 이름 노출 |
| Comment | SET_NULL | **유지** — 동일 |
| Place | SET_NULL | **유지** — 동일 |
| Like | SET_NULL | **유지** — like_count는 수동 카운터라 영향 없음 |
| PostAnonymousUser | SET_NULL | **유지** — 익명 번호 일관성 유지 |

---

## 변경 파일 목록

### 신규 생성
- `users/service/user_service.py` — `withdraw_user()` 서비스 함수

### 수정
- `users/apis/views.py` — `WithdrawView` 추가
- `users/apis/urls.py` — `DELETE /users/me/` 경로 추가

### 변경 없음
- 모델: 별도 필드 추가/마이그레이션 불필요 (기존 필드 값만 변경)
- posts, places, comments: 코드 수정 없음

---

## API 엔드포인트

```
DELETE /users/me/
Authorization: Bearer <access_token>
```

요청 바디 없음 — 인증된 토큰으로 본인 확인 충분

응답:
- `204 No Content` — 탈퇴 성공
- `401 Unauthorized` — 미인증

---

## 서비스 로직

```python
def withdraw_user(user):
    with transaction.atomic():
        user.is_active = False
        user.name = "탈퇴한 사용자"
        user.account_id = None
        user.student_id = f"withdrawn_{user.id}"
        user.password_hash = make_password(None)
        user.save(update_fields=[
            'is_active', 'name', 'account_id', 'student_id', 'password_hash'
        ])
```

---

## 구현 순서

1. `users/service/user_service.py` 생성 — `withdraw_user()` 구현
2. `users/apis/views.py` — `WithdrawView` 추가
3. `users/apis/urls.py` — URL 등록
4. 테스트 작성
5. api-spec 버전 업

---

## 고려사항

### 탈퇴 후 게시글 author 표시
`_author_data()`는 author가 존재하면 name, grade 등을 그대로 반환한다.
탈퇴 유저의 경우 `name="알 수 없는 사용자"`가 노출된다.
클라이언트에서 회색 처리 등 UX 처리 권장.
서버에서 `is_active` 체크해 null 반환하는 방식도 가능 — 논의 필요.

### 재가입
`student_id`가 `withdrawn_{uuid}`로 바뀌므로 원래 학번으로 재가입 가능.

### grade/class_num/num unique_together
탈퇴 유저의 조합을 초기화하려면 null 허용 마이그레이션이 필요해 보류.
이름 익명화만으로 프라이버시 충분하다고 판단.
