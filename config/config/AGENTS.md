<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-22 | Updated: 2026-04-22 -->

# config/config

## Purpose
Django 설정 패키지. 프로젝트 전역 설정(settings.py), URL 라우팅(urls.py), 커스텀 예외 처리(exceptions.py), DRF 응답 핸들러(utils.py), ASGI/WSGI 엔트리포인트를 포함한다.

## Key Files

| File | Description |
|------|-------------|
| `settings.py` | Django 전역 설정 — DB, JWT, S3, DRF, INSTALLED_APPS, 타임존(Asia/Seoul) |
| `urls.py` | 루트 URL 라우팅 — users/posts/places/images 앱 URL 포함, Swagger UI |
| `exceptions.py` | 커스텀 예외 클래스 — `CustomAPIException`, `InvalidCredentialsException` |
| `utils.py` | DRF 커스텀 예외 핸들러 — 응답에 `status_code`, `message` 필드 추가 |
| `asgi.py` | ASGI 애플리케이션 엔트리포인트 |
| `wsgi.py` | WSGI 애플리케이션 엔트리포인트 |
| `.env` | 환경변수 파일 (SECRET_KEY, DB_*, AWS_*) — git 미추적 |

## For AI Agents

### Working In This Directory
- 새 앱 추가 시 `settings.py`의 `INSTALLED_APPS`에 등록
- 새 앱 URL 추가 시 `urls.py`에 `include()` 항목 추가
- 한국어 에러는 반드시 `exceptions.py`의 `CustomAPIException`을 상속해서 정의
- 환경변수는 `.env` 파일에서 `django-environ`으로 로드 (`env("KEY_NAME")`)

### Common Patterns
- 모든 API 에러 응답 형식: `{"detail": "...", "status_code": 4xx, "message": "..."}`
- JWT: Access 30분, Refresh 7일, Bearer 헤더 방식
- DB: PostgreSQL, `DB_SCHEMA` 환경변수로 search_path 설정 가능

### Testing Requirements
- settings.py 변경 시 `python config/manage.py check` 실행

## Dependencies

### Internal
- 모든 앱(`users`, `posts`, `places`, `images`)이 이 패키지에 의존

### External
- `django-environ` — `.env` 파일 로드
- `drf-spectacular` — `/api/schema/`, `/api/swagger/` 자동 생성
- `rest_framework_simplejwt` — JWT 인증 백엔드

<!-- MANUAL: -->
