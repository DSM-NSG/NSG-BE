<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-22 | Updated: 2026-04-22 -->

# users/apis

## Purpose
사용자 인증 API 레이어. 로그인 엔드포인트를 제공한다. 뷰는 얇게 유지하고 실제 인증 로직은 `service/auth_service.py`에 위임한다.

## Key Files

| File | Description |
|------|-------------|
| `views.py` | `LoginView` — POST 요청 수신, AuthService 호출, JWT 반환 |
| `urls.py` | `users/` 경로 하위 URL 패턴 정의 |
| `serializer.py` | 로그인 요청/응답 직렬화 |

## For AI Agents

### Working In This Directory
- 새 엔드포인트 추가 시: `views.py` 뷰 작성 → `urls.py` 등록 → `config/config/urls.py` 확인
- 뷰에 비즈니스 로직 작성 금지 — 반드시 `service/` 레이어로 위임
- URL prefix: `users/` (루트 urls.py에서 `path('users/', include('users.apis.urls'))`)

### Common Patterns
- `APIView` 또는 `GenericAPIView` 기반
- 인증 불필요 뷰: `permission_classes = [AllowAny]`
- 응답: `Response(data, status=status.HTTP_200_OK)`

## Dependencies

### Internal
- `users/service/auth_service.py` — 인증 로직
- `config/config/exceptions.py` — 에러 응답

<!-- MANUAL: -->
