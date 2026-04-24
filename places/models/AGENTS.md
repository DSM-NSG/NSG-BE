<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-22 | Updated: 2026-04-22 -->

# places/models

## Purpose
장소 모델 패키지. `Place` 모델을 정의하며 학교 주변 장소(맛집/카페/PC방/노래방/기타)의 위치 정보, 설명, 네이버 지도 링크를 저장한다.

## Key Files

| File | Description |
|------|-------------|
| `place_model.py` | `Place` 모델 — UUID PK, 카테고리, 위도/경도, 네이버지도 URL |
| `__init__.py` | `Place` 모델 export |

## For AI Agents

### Working In This Directory
- 카테고리 선택지: `RESTAURANT`, `CAFE`, `PC_ROOM`, `KARAOKE`, `ETC`
- `latitude`, `longitude`: FloatField — 소수점 정밀도 주의
- `naver_map_url`: URLField(max_length=500), blank/null 허용
- 장소 추가 시 마이그레이션: `python config/manage.py makemigrations places`

### Common Patterns
- UUID PK, `ordering = ['-created_at']`
- DB 테이블명: `place`, 인덱스: `category`, `created_at`

## Dependencies

### Internal
- `users.User` — author FK
- `posts.Post` — 역참조 `place.posts.all()` (TIP 게시글에서 참조)

<!-- MANUAL: -->
