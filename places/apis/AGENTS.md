<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-22 | Updated: 2026-04-22 -->

# places/apis

## Purpose
장소 API 레이어. 장소 목록 조회, 생성, 상세 조회 엔드포인트를 제공한다. 비즈니스 로직은 `service/` 레이어로 위임한다.

## Key Files

| File | Description |
|------|-------------|
| `views.py` | 장소 조회/생성 뷰 |
| `urls.py` | places 관련 URL 패턴 |
| `serializers.py` | Place 요청/응답 직렬화 |

## For AI Agents

### Working In This Directory
- URL prefix: 루트 urls.py에서 `path('', include('places.apis.urls'))` — prefix 없음
- 인증 필요 뷰: `permission_classes = [IsAuthenticated]`
- 새 API 추가 시 `api-spec/`에 버전 파일도 함께 업데이트

### Common Patterns
- 카테고리 필터링은 쿼리 파라미터(`?category=CAFE`)로 처리
- 위치 기반 정렬/필터 추가 시 `latitude`, `longitude` 활용

## Dependencies

### Internal
- `places/service/place_service.py`
- `places/models/place_model.py`

<!-- MANUAL: -->
