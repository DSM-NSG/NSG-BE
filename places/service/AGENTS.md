<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-22 | Updated: 2026-04-22 -->

# places/service

## Purpose
장소 비즈니스 로직 레이어. 장소 생성, 조회, 삭제 등 핵심 로직을 담당한다.

## Key Files

| File | Description |
|------|-------------|
| `place_service.py` | 장소 생성/조회/삭제 비즈니스 로직 |
| `__init__.py` | 패키지 초기화 |

## For AI Agents

### Working In This Directory
- 쓰기 작업에 `transaction.atomic()` 사용
- 권한 체크: 수정/삭제 시 `place.author == user` 확인
- 키워드 전용 인자(`*`) 패턴 권장

### Common Patterns
- `get_object_or_404(Place, id=place_id)` 패턴
- 목록 조회: `Place.objects.filter(category=category)` + `ordering = ['-created_at']`

## Dependencies

### Internal
- `places.models.Place`
- `config.exceptions.CustomAPIException`

<!-- MANUAL: -->
