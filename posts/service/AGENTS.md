<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-22 | Updated: 2026-04-22 -->

# posts/service

## Purpose
게시글 관련 비즈니스 로직 레이어. 게시글 생성/삭제, 댓글 생성/삭제, 좋아요 토글, 인기 전공 태그 점수 계산을 담당한다. 트랜잭션 안전성과 race condition 방지가 핵심 관심사다.

## Key Files

| File | Description |
|------|-------------|
| `post_service.py` | `create_tip`, `create_major_post`, `delete_post`, `get_popular_major_tags` |
| `comment_service.py` | 댓글/대댓글 생성, 삭제 로직 |
| `like_service.py` | 좋아요 토글 — `Post.like_count` F() 업데이트 |
| `__init__.py` | 패키지 초기화 |

## For AI Agents

### Working In This Directory
- 모든 쓰기 작업은 `transaction.atomic()` 사용
- `get_popular_major_tags()`: 점수 = `Σ (1.0 + like_count × 2.0) × 1 / (1 + 경과일수 × 0.1)` — top_n(기본 10) 반환
- 익명 순번(`PostAnonymousUser`)은 반드시 `select_for_update()`로 race condition 방지
- 좋아요 수 증감: `Post.objects.filter(id=...).update(like_count=F('like_count') + 1)` 패턴

### Common Patterns
- 키워드 전용 인자(`*`) 패턴으로 명시적 호출
- `get_object_or_404` 사용으로 404 처리 간결화
- 권한 체크: `if post.author != user: raise PermissionError()`
- 이미지는 `PostImage.objects.bulk_create([...])` 일괄 저장

## Dependencies

### Internal
- `posts.models` — Post, PostImage, PostAnonymousUser, MajorTag, Comment, Like
- `places.Place` — TIP 게시글 생성 시 place_id

<!-- MANUAL: -->
