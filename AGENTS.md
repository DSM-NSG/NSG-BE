<!-- Generated: 2026-04-22 | Updated: 2026-04-22 -->

# NSG-BE

## Purpose
DSM(대덕소프트웨어마이스터고) 학생 커뮤니티 플랫폼 백엔드 API 서버.
Django 6.0.3 + Django REST Framework 기반으로 게시글(꿀팁/전공), 장소 공유, 이미지 업로드 기능을 제공한다.
DSM 공식 로그인 API와 연동하여 학번 기반 인증을 처리하고 JWT 토큰을 발급한다.

## Key Files

| File | Description |
|------|-------------|
| `manage.py` → `config/manage.py` | Django 관리 명령 진입점 |
| `requirements.txt` | Python 의존성 목록 |
| `Dockerfile` | Docker 이미지 빌드 설정 |
| `docker-compose.yml` | 로컬 개발환경 컨테이너 구성 |
| `api-spec.json` | 최신 OpenAPI 3.0.3 전체 스펙 (항상 최신 버전과 동일) |
| `CLAUDE.md` | AI 에이전트용 개발 규칙 (plan.md 워크플로우, API 명세 관리) |
| `erd.md` | DB 엔티티 관계도 |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `config/` | Django 프로젝트 설정 (settings, urls, exceptions, utils) (see `config/AGENTS.md`) |
| `api-spec/` | OpenAPI 스펙 버전 이력 파일들 (see `api-spec/AGENTS.md`) |
| `users/` | 사용자 인증 앱 — DSM 로그인 연동, JWT 발급 (see `users/AGENTS.md`) |
| `posts/` | 게시글 앱 — 꿀팁/전공 게시글, 댓글, 좋아요 (see `posts/AGENTS.md`) |
| `places/` | 장소 공유 앱 — 맛집/카페 등 위치 정보 (see `places/AGENTS.md`) |
| `images/` | 이미지 업로드 앱 — S3 업로드 처리 (see `images/AGENTS.md`) |

## For AI Agents

### Working In This Directory
- 새 기능 구현 전 반드시 `plan.md`를 작성하고 사용자 승인을 받을 것
- 새 API 구현 완료 시 `api-spec/`에 버전 파일 추가, `api-spec.json` 동기화
- 모든 UUID는 PK로 사용 (`uuid.uuid4`, `editable=False`)
- 에러 메시지는 한국어로 작성 (`CustomAPIException` 상속)

### Testing Requirements
- 현재 테스트 파일은 각 앱의 `tests.py`에 위치 (내용 미작성 상태)
- 비즈니스 로직 변경 시 service 레이어 단위 테스트 작성 권장

### Common Patterns
- 각 앱: `models/` + `apis/` + `service/` 3-레이어 구조
- 뷰(View)는 얇게 유지: 직렬화(Serializer) + 서비스 호출만
- 트랜잭션이 필요한 작업은 `transaction.atomic()` 사용

## Dependencies

### External
- `Django==6.0.3` — 웹 프레임워크
- `djangorestframework==3.16.1` — REST API
- `djangorestframework_simplejwt==5.5.1` — JWT 인증
- `drf-spectacular==0.29.0` — OpenAPI 스펙 자동 생성
- `psycopg2-binary==2.9.11` — PostgreSQL 드라이버
- `boto3==1.38.0` — AWS S3 이미지 업로드
- `django-environ==0.13.0` — 환경변수 관리

<!-- MANUAL: 기존 프로젝트 규칙은 CLAUDE.md에서 관리됩니다 -->
