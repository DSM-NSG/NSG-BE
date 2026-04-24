<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-22 | Updated: 2026-04-22 -->

# posts/models

## Purpose
게시글 관련 모델 패키지. 통합 게시글(`Post`), 댓글(`Comment`), 좋아요(`Like`), 전공(`Major`), 전공 태그(`MajorTag`), 게시글 이미지(`PostImage`), 익명 순번(`PostAnonymousUser`) 모델을 정의한다.

## Key Files

| File | Description |
|------|-------------|
| `post_model.py` | `Post` — TIP/MAJOR 통합 게시글, UUID PK, author/place FK |
| `comment_model.py` | `Comment` — 댓글/대댓글 (self FK `parent`로 계층 구조) |
| `like_model.py` | `Like` — 게시글 좋아요 (User+Post unique_together) |
| `major_model.py` | `Major` — 전공 카테고리 마스터 테이블 |
| `major_tag_model.py` | `MajorTag` — Post↔Major M:N 연결 테이블 |
| `post_image_model.py` | `PostImage` — 게시글 첨부 이미지 URL + 순서 |
| `post_anonymous_user_model.py` | `PostAnonymousUser` — 게시글 내 익명 순번 매핑 |
| `__init__.py` | 모든 모델 export |

## For AI Agents

### Working In This Directory
- `Post.post_type`: `'TIP'` 또는 `'MAJOR'` — 두 유형을 하나의 테이블로 통합 관리
- TIP 게시글만 `category`(PLACE/DORM_LIFE/SCHOOL_LIFE/ETC) 사용, MAJOR는 빈 문자열
- `Comment.parent`: self FK — NULL이면 댓글, 값 있으면 대댓글
- `Like`: `(user, post)` unique_together로 중복 좋아요 방지
- `PostAnonymousUser`: 동일 post에서 같은 user의 익명 순번 보장 (race condition → `select_for_update`)

### Common Patterns
- 모든 모델 UUID PK
- `ordering = ['-created_at']` (Post, Place)
- DB 인덱스: `post_type + created_at`, `category`, `post + created_at`

## Dependencies

### Internal
- `users.User` — author FK (Post, Comment, Like)
- `places.Place` — Post의 place FK

<!-- MANUAL: -->
