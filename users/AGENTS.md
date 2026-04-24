<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-22 | Updated: 2026-04-22 -->

# users

## Purpose
사용자 인증 Django 앱. DSM(대덕소프트웨어마이스터고) 공식 로그인 API와 연동하여 학번 기반 인증을 처리하고 JWT 토큰을 발급한다. 최초 로그인 시 외부 DSM API를 호출하여 사용자를 로컬 DB에 생성하고, 이후에는 로컬 비밀번호 해시로 검증한다.

## Key Files

| File | Description |
|------|-------------|
| `apps.py` | Django 앱 설정 (`UsersConfig`) |
| `models.py` | `models/` 패키지의 배럴 export |
| `admin.py` | Django Admin 등록 |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `models/` | User 모델 정의 (see `models/AGENTS.md`) |
| `apis/` | 인증 API 뷰, URL, 시리얼라이저 (see `apis/AGENTS.md`) |
| `service/` | DSM 로그인 연동 및 JWT 발급 비즈니스 로직 (see `service/AGENTS.md`) |
| `migrations/` | DB 마이그레이션 파일 (자동 생성) |

## For AI Agents

### Working In This Directory
- `AUTH_USER_MODEL = 'users.User'` — 커스텀 User 모델 사용, `AbstractBaseUser` 기반
- 새 사용자 필드 추가 시: `models/user_model.py` 수정 → `makemigrations` → `migrate`
- 인증 로직 변경은 반드시 `service/auth_service.py`에서만

### Common Patterns
- `student_id`: `{grade}-{class_num}-{num}` 형식 (예: `1-2-3`)
- UUID PK 사용
- 외부 DSM API: `POST https://dsm-login.dsmhs.kr/dsm-login/user/user-data`

## Dependencies

### Internal
- `config.exceptions` — `InvalidCredentialsException` 사용

### External
- `rest_framework_simplejwt` — JWT 토큰 발급
- `requests` — 외부 DSM 로그인 API 호출

<!-- MANUAL: -->
