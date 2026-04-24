# 테스트 추가 계획

## 기능 개요
pytest-django + factory_boy 조합으로 service 레이어 단위 테스트와 API 통합 테스트를 작성한다.

---

## 변경 파일 목록

### 신규 생성
- `requirements-dev.txt` — 테스트 전용 의존성 (pytest-django, factory_boy, faker)
- `pytest.ini` — pytest 설정 (DJANGO_SETTINGS_MODULE 등)
- `tests/__init__.py`
- `tests/factories.py` — UserFactory, PostFactory, CommentFactory, LikeFactory, MajorFactory, PlaceFactory
- `tests/test_auth_service.py` — AuthService.login() 단위 테스트
- `tests/test_post_service.py` — create_tip, create_major_post, delete_post, get_popular_major_tags 단위 테스트
- `tests/test_comment_service.py` — create_comment, create_reply, delete_comment 단위 테스트
- `tests/test_like_service.py` — toggle_like 단위 테스트
- `tests/test_posts_api.py` — TIP/MAJOR 게시글 API 통합 테스트
- `tests/test_users_api.py` — 로그인 API 통합 테스트

### 수정 없음 (기존 각 앱의 `tests.py`는 빈 파일로 유지)

---

## 테스트 범위

### Service 단위 테스트
| 파일 | 테스트 대상 |
|------|------------|
| `test_auth_service.py` | 로컬 유저 로그인 성공, 비밀번호 불일치 실패, DSM API 호출 (mock), cohort 계산 |
| `test_post_service.py` | TIP 생성, MAJOR 생성, 게시글 삭제(본인/타인), 인기 태그 점수 계산 |
| `test_comment_service.py` | 댓글 생성, 대댓글 생성, 댓글 삭제(본인/타인) |
| `test_like_service.py` | 좋아요 토글(on→off, off→on), like_count 정확성 |

### API 통합 테스트
| 파일 | 테스트 대상 |
|------|------------|
| `test_users_api.py` | POST /users/login — 로컬 유저 성공, 인증 실패 |
| `test_posts_api.py` | TIP 목록/생성/상세/삭제, MAJOR 목록/생성/삭제, 댓글 생성/삭제, 좋아요 토글 |

---

## 구현 순서
1. `requirements-dev.txt` 작성
2. `pytest.ini` 작성
3. `tests/factories.py` — Factory 클래스 정의
4. Service 단위 테스트 4개 파일
5. API 통합 테스트 2개 파일

---

## 고려사항
- DSM 외부 API 호출은 `unittest.mock.patch`로 목킹
- DB는 실제 테스트 DB 사용 (`@pytest.mark.django_db`)
- 각 테스트는 독립적 — factory로 데이터 생성, teardown 자동

## 상태
- [x] 작성 완료
- [x] 승인됨
- [x] 구현 완료 — 52 passed in 17.80s
