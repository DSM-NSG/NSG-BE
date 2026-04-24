<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-22 | Updated: 2026-04-22 -->

# users/service

## Purpose
사용자 인증 비즈니스 로직 레이어. DSM 공식 로그인 API 연동, 로컬 DB 유저 생성/조회, 비밀번호 해시 검증, JWT 발급을 담당한다.

## Key Files

| File | Description |
|------|-------------|
| `auth_service.py` | `AuthService` 클래스 — `login()` 정적 메서드, DSM API 연동, JWT 발급 |
| `__init__.py` | 패키지 초기화 |

## For AI Agents

### Working In This Directory
- `AuthService.login(*, account_id, password)` 흐름:
  1. 로컬 DB에서 `account_id`로 유저 조회
  2. 존재하면 `check_password(password, user.password_hash)` 검증
  3. 없으면 외부 DSM API(`POST /dsm-login/user/user-data`) 호출 → 유저 생성
  4. JWT `access_token` + `refresh_token` 반환
- DSM API 실패 시 `InvalidCredentialsException` raise
- cohort 계산 공식: `현재연도 - grade - 2013`

### Common Patterns
- 정적 메서드(`@staticmethod`) 패턴
- 키워드 전용 인자(`*`) 사용으로 명시적 호출 강제
- 외부 HTTP 호출은 `timeout=10` 설정

## Dependencies

### Internal
- `users.models.User`
- `config.exceptions.InvalidCredentialsException`

### External
- `rest_framework_simplejwt.tokens.RefreshToken`
- `django.contrib.auth.hashers` — `make_password`, `check_password`
- `requests` — DSM API HTTP 호출

<!-- MANUAL: -->
