<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-22 | Updated: 2026-04-22 -->

# users/models

## Purpose
사용자 모델 패키지. `AbstractBaseUser` 기반의 커스텀 `User` 모델과 `UserManager`를 정의한다. 학번(`student_id`)을 로그인 식별자로 사용하며 UUID를 PK로 사용한다.

## Key Files

| File | Description |
|------|-------------|
| `user_model.py` | `User` 모델 및 `UserManager` 정의 |
| `__init__.py` | `User` 모델 export |

## For AI Agents

### Working In This Directory
- `User` 필드 추가/변경 시 마이그레이션 필수: `python config/manage.py makemigrations users`
- `USERNAME_FIELD = 'student_id'` — DRF 인증과 JWT는 `student_id` 기반
- `REQUIRED_FIELDS`: grade, class_num, num, name, cohort
- `unique_together = [['grade', 'class_num', 'num']]` — 동일 학번 중복 방지

### Common Patterns
- PK: `UUIDField(default=uuid.uuid4, editable=False)`
- `password_hash` 필드에 `make_password()`로 해시된 값 저장 (`password` 필드 미사용)
- `cohort` = `현재연도 - grade - 2013` 공식으로 계산

## Dependencies

### Internal
- `users/migrations/` — 마이그레이션 파일 자동 생성 경로

<!-- MANUAL: -->
