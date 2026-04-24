<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-22 | Updated: 2026-04-22 -->

# config

## Purpose
Django 프로젝트의 최상위 설정 디렉토리. `manage.py` 실행 진입점과 내부 `config/` 패키지(설정, URL, 예외 처리 등)를 포함한다. 프로젝트 루트에서 `python config/manage.py` 명령으로 Django를 실행한다.

## Key Files

| File | Description |
|------|-------------|
| `manage.py` | Django 관리 명령 실행 진입점 (`DJANGO_SETTINGS_MODULE=config.settings`) |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `config/` | Django 설정 패키지 — settings, urls, exceptions, utils (see `config/AGENTS.md`) |

## For AI Agents

### Working In This Directory
- Django 명령 실행: `python config/manage.py runserver`, `python config/manage.py migrate`
- `manage.py`는 수정하지 않음

### Common Patterns
- `DJANGO_SETTINGS_MODULE`은 `config.settings`를 가리킴

## Dependencies

### Internal
- `config/config/` — Django 설정 패키지

<!-- MANUAL: -->
