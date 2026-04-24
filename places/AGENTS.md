<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-22 | Updated: 2026-04-22 -->

# places

## Purpose
장소 공유 Django 앱. 학교 주변 맛집, 카페, PC방, 노래방 등 장소 정보를 등록하고 공유한다. 위도/경도 좌표와 네이버 지도 링크를 저장하며, 익명 등록도 지원한다. 게시글 앱의 TIP 게시글에서 장소를 태그할 수 있다.

## Key Files

| File | Description |
|------|-------------|
| `apps.py` | Django 앱 설정 (`PlacesConfig`) |
| `models.py` | `models/` 패키지의 배럴 export |
| `admin.py` | Django Admin 등록 |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `models/` | Place 모델 정의 (see `models/AGENTS.md`) |
| `apis/` | 장소 API 뷰, URL, 시리얼라이저 (see `apis/AGENTS.md`) |
| `service/` | 장소 조회/생성 비즈니스 로직 (see `service/AGENTS.md`) |
| `migrations/` | DB 마이그레이션 파일 (자동 생성) |

## For AI Agents

### Working In This Directory
- 카테고리: RESTAURANT/CAFE/PC_ROOM/KARAOKE/ETC
- 위도(`latitude`), 경도(`longitude`): FloatField — 지도 연동 시 좌표 정확도 주의
- `naver_map_url`: 선택 필드 (blank/null 허용)
- `posts.Place` FK로 역참조: `place.posts.all()`

### Common Patterns
- UUID PK, `ordering = ['-created_at']`
- DB 테이블명: `place`

## Dependencies

### Internal
- `users.User` — author FK
- `posts.Post` — TIP 게시글에서 `place` FK로 참조됨

<!-- MANUAL: -->
