<!-- Parent: ../AGENTS.md -->
<!-- Generated: 2026-04-22 | Updated: 2026-04-22 -->

# api-spec

## Purpose
OpenAPI 3.0.3 스펙 버전 이력 디렉토리. 새 API가 추가되거나 변경될 때마다 이전 버전을 복사해 버전을 올린 파일을 생성한다. 루트의 `api-spec.json`은 항상 이 디렉토리의 최신 버전과 동일하게 유지된다.

## Key Files

| File | Description |
|------|-------------|
| `v1.0.0.json` | 최초 릴리즈 — users, posts, places, images API 전체 스펙 |

## For AI Agents

### Working In This Directory
- **새 API 추가 시**: 이전 버전 파일을 복사하여 버전 올린 파일 생성 후 변경사항 추가
- **버전 규칙**: minor(새 엔드포인트) → `v1.x.0.json`, patch(스펙 오류) → `v1.x.y.json`, major(하위 호환 불가) → `v2.0.0.json`
- **루트 동기화**: 버전 파일 작성 후 반드시 루트 `api-spec.json`도 동일하게 업데이트

### Common Patterns
- 각 파일은 완전한 OpenAPI 3.0.3 스펙 포함 (참조가 아닌 전체 내용)
- `info.version` 필드를 파일명과 일치시킬 것

## Dependencies

### Internal
- 루트 `api-spec.json` — 항상 이 디렉토리의 최신 버전과 동기화

<!-- MANUAL: -->
