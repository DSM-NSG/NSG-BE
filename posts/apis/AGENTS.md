<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-22 | Updated: 2026-04-22 -->

# posts/apis

## Purpose
게시글, 댓글, 좋아요 API 레이어. 뷰는 얇게 유지하고 비즈니스 로직은 `service/` 레이어로 위임한다. drf-spectacular를 통해 OpenAPI 스펙이 자동 생성된다.

## Key Files

| File | Description |
|------|-------------|
| `views.py` | 게시글 CRUD, 댓글, 좋아요, 인기 전공 태그 뷰 |
| `urls.py` | posts 관련 URL 패턴 (`/posts/`, `/comments/`, `/likes/` 등) |
| `serializers.py` | 요청/응답 직렬화 — Post, Comment, Like, Major 시리얼라이저 |

## For AI Agents

### Working In This Directory
- URL prefix: 루트 urls.py에서 `path('', include('posts.apis.urls'))` — prefix 없음
- 인증 필요 뷰: `permission_classes = [IsAuthenticated]`
- 뷰에서 현재 사용자: `request.user`
- 새 API 추가 시 `api-spec/`에 버전 파일도 함께 업데이트 필요

### Common Patterns
- 시리얼라이저에서 `author_id` 같은 관계 필드는 UUID 문자열로 직렬화
- 목록 응답에는 페이지네이션 고려
- `is_liked` 등 현재 사용자 기반 필드는 `SerializerMethodField`로 처리

## Dependencies

### Internal
- `posts/service/` — post_service, comment_service, like_service
- `posts/models/` — Post, Comment, Like, Major, MajorTag

<!-- MANUAL: -->
