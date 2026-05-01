# Frontend Performance

프론트엔드 성능 가이드 문서의 단일 진입점.

## 문서 목록

- [rendering-guidelines](rendering-guidelines.md): re-render 방지, key 안정성, memo/useMemo/useCallback 기준
- [caching-strategy](caching-strategy.md): staleTime/gcTime, 쿼리 키 설계, prefetch, invalidation
- [list-optimization](list-optimization.md): 페이지네이션, debounce, 가상 스크롤, 무한 스크롤

## 운영 원칙

- 성능 문서를 추가·수정할 때 이 README의 문서 목록을 함께 갱신한다.
- 상위 문서(예: `docs/frontend/README.md`)는 개별 성능 파일이 아닌 이 README를 참조한다.
