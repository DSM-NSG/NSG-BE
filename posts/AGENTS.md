<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-22 | Updated: 2026-04-22 -->

# posts

## Purpose
게시글 Django 앱. 꿀팁(TIP)과 전공(MAJOR) 두 가지 유형의 게시글을 통합 관리한다. 댓글/대댓글, 좋아요, 익명 게시/댓글, 이미지 첨부, 전공 태그 기능을 제공한다. 인기 전공 태그 점수 알고리즘(시간 감쇠 + 좋아요 가중치)도 포함한다.

## Key Files

| File | Description |
|------|-------------|
| `apps.py` | Django 앱 설정 (`PostsConfig`) |
| `models.py` | `models/` 패키지의 배럴 export |
| `admin.py` | Django Admin 등록 |

## Subdirectories

| Directory | Purpose |
|-----------|---------|
| `models/` | Post, Comment, Like, Major, MajorTag, PostImage, PostAnonymousUser 모델 (see `models/AGENTS.md`) |
| `apis/` | 게시글/댓글/좋아요 API 뷰, URL, 시리얼라이저 (see `apis/AGENTS.md`) |
| `service/` | 게시글 생성/삭제, 댓글, 좋아요 비즈니스 로직 (see `service/AGENTS.md`) |
| `migrations/` | DB 마이그레이션 파일 (자동 생성) |

## For AI Agents

### Working In This Directory
- TIP 게시글: `category` 필드(PLACE/DORM_LIFE/SCHOOL_LIFE/ETC) 필수, `place` FK 선택
- MAJOR 게시글: `category` 빈 문자열, `MajorTag`로 전공 연결
- 익명 게시글의 순번 관리: `PostAnonymousUser` — race condition 방지를 위해 `select_for_update` 사용
- 좋아요 수 변경 시 `Post.like_count` 필드를 `F()` 표현식으로 업데이트

### Common Patterns
- 트랜잭션 필수: `create_tip`, `create_major_post` 모두 `transaction.atomic()` 사용
- 인기 태그 점수 공식: `Σ (1.0 + like_count × 2.0) × 1 / (1 + 경과일수 × 0.1)`

## Dependencies

### Internal
- `users.User` — author FK
- `places.Place` — TIP 게시글의 장소 FK
- `config.exceptions` — `CustomAPIException`

<!-- MANUAL: -->
