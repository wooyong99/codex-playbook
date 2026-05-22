# Persistence Strategies

이 문서는 `backend/internal/persistence` 모듈의 역할형 전략 문서 맵을 소유한다.

## 목적

- persistence 내부 컴포넌트의 책임을 전략별로 분리한다.
- `Storage Adapter`, `QueryDsl`, `DDL Management`의 선택 기준을 한곳에서 찾게 한다.
- 레거시 템플릿 대신 현재 전략 문서의 용어를 기준으로 persistence 구조를 설명한다.

## 적용 범위

- application Port 구현체와 Repository 분리
- JPA Entity, Domain 변환, QueryDsl 쿼리 작성
- Entity 변경과 DDL 파일 관리

## 전략 문서

| 전략 | 문서 | 책임 |
|------|------|------|
| Storage Adapter | [storage-adapter-convention](storage-adapter-convention.md) | Port 구현, JpaRepository/QueryDslRepository 위임, Entity 변환 |
| QueryDsl | [querydsl-convention](querydsl-convention.md) | 동적 조건, Projection, pagination 쿼리 작성 |
| DDL Management | [ddl-management](ddl-management.md) | DDL 파일 위치와 Entity 변경 동반 관리 |

## 공통 의존 흐름

```text
application Port
  -> {Entity}Adapter
    -> {Entity}JpaRepository
    -> {Entity}QueryDslRepository
    -> {Entity}Extension
      -> Domain
      -> {Entity}Entity

sql/{domain}/{table}.sql
  -> database schema
```
