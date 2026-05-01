# Storage Strategies

이 프로젝트에서 `storage` 단위에 실제로 사용 중인 구현 전략 요약.

## 핵심 전략

- application Port는 Adapter가 구현하고 저장소 세부 구현은 Adapter 뒤에 숨긴다.
- 단순 CRUD는 JpaRepository, 복잡 쿼리와 Projection은 QueryDslRepository로 분리한다.
- 도메인 모델과 Entity 변환은 별도 Extension/Mapper가 담당한다.
- Entity 변경과 DDL 변경은 같은 변경 단위로 관리한다.

## 근거가 된 코드 패턴

- `{Entity}Adapter`, `{Entity}JpaRepository`, `{Entity}QueryDslRepository` - 저장소 역할 분리
- `{Entity}Entity`, `{Entity}Extension` - 인프라 모델과 도메인 모델 변환
- `db/changelog` 또는 `sql` migration 파일 - DDL 변경 이력

## 세부 문서

- [storage-adapter-convention](storage-adapter-convention.md) - Adapter, Repository, Entity, 변환 컴포넌트를 작성할 때
- [querydsl-convention](querydsl-convention.md) - 동적 조건, Projection, pagination 쿼리를 작성할 때
- [ddl-management](ddl-management.md) - DDL 파일과 변경 이력을 관리할 때
