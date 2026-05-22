# QueryDsl 컨벤션

이 문서는 `storage` 단위에서 QueryDsl로 동적 조건, Projection, pagination 쿼리를 작성하는 전략을 정리한다.

## 목적

- 복잡한 조회 쿼리를 선언적으로 읽히게 한다.
- 동적 조건과 조인 재사용 기준을 통일한다.
- pagination과 fetch join 조합으로 인한 성능 문제를 막는다.

## 적용 범위

- QueryDslRepository의 동적 조건 검색
- 조인, 정렬, pagination, count 쿼리
- 조회 전용 Projection

Adapter, Entity, 변환 규칙은 [storage-adapter-convention](storage-adapter-convention.md)이 소유한다.

## 책임

- QueryDslRepository 안에서 복잡 쿼리 구현을 캡슐화한다.
- 쿼리 작성 순서를 고정해 의도를 드러낸다.
- 반환 타입을 Entity, Domain, Projection DTO 중 목적에 맞게 선택한다.

## 전체 흐름

```text
{Entity}Adapter
  -> {Entity}QueryDslRepository
    -> BooleanExpression?
    -> queryFactory
    -> Entity | Projection
    -> Domain mapping when needed
```

## 세부 규칙

### 동적 조건

- `BooleanBuilder` 대신 `BooleanExpression?` 반환 방식을 사용한다.
- 단순 조건은 `where` 절에 직접 작성한다.
- 날짜 범위, OR 조합, 여러 필드 묶음처럼 복잡한 조건만 private 메서드로 추출한다.
- `where()`에 `null`을 전달하면 QueryDsl이 해당 조건을 무시하는 동작을 활용한다.

### 쿼리 작성 순서

쿼리는 아래 순서를 기본으로 작성한다.

```text
select -> from -> join -> where -> groupBy -> having -> orderBy -> offset/limit
```

- 순서를 임의로 섞지 않는다.
- 동일한 조인 조합이 여러 쿼리에서 반복될 때만 확장 함수나 private 메서드로 묶는다.
- 단일 쿼리에서만 쓰는 조인은 인라인으로 유지한다.

### 조건 그룹핑

- 조건이 5개 이하이면 `where` 절에 직접 나열한다.
- 조건이 10개 이상이면 도메인 의미 단위로 그룹핑한다.
- 같은 Repository 안에서 재사용되면 private 메서드로 둔다.
- 여러 Repository에서 재사용되면 별도 유틸 또는 companion object를 검토한다.

### Pagination

- fetch join과 pagination을 함께 사용하지 않는다.
- pagination이 필요하면 2-step 조인을 사용한다.
- Step 1은 조건에 맞는 ID만 offset/limit으로 조회한다.
- Step 2는 ID 기준으로 연관 데이터를 조회한다.
- count 쿼리는 content 쿼리와 분리한다.
- 전체 건수 생략이 가능하면 `PageableExecutionUtils.getPage()` 사용을 검토한다.

### Projection

- Entity 전체가 필요하면 Entity 조회 후 Domain으로 변환한다.
- 읽기 전용 목록은 `Projections.constructor`를 사용한다.
- `Tuple.get()`은 타입 안정성이 낮으므로 기본값으로 사용하지 않는다.

## 금지 규칙

- `BooleanBuilder`를 사용하지 않는다.
- fetch join과 pagination을 함께 사용하지 않는다.
- `Tuple.get()` 중심 Projection을 사용하지 않는다.
- 쿼리 작성 순서를 임의로 바꾸지 않는다.
- 실제 재사용이 없는 조건과 조인을 과도하게 추출하지 않는다.
- QueryDsl 타입을 application Port 시그니처로 노출하지 않는다.

## 예외와 경계

- 일회성 집계 쿼리처럼 constructor Projection이 과도하면 제한적으로 Tuple을 사용할 수 있다.
- 페이지 크기가 매우 작아도 fetch join pagination은 기본 금지로 본다.
- Projection DTO가 application 응답 계약이면 application DTO와 소유권을 먼저 검토한다.

## 완료 체크리스트

아래 항목을 모두 충족해야 완료로 판정한다.

- [ ] `금지 규칙` 섹션의 각 항목을 위반하는 코드, 문서, 설정 변경이 없다.
- [ ] 동적 조건이 `BooleanExpression?` 방식으로 작성되어 있다.
- [ ] pagination 쿼리가 2-step 방식과 분리된 count 쿼리를 사용한다.
- [ ] Projection은 타입 안정적인 constructor 기반으로 작성되어 있다.
- [ ] QueryDsl 구현 세부사항이 persistence 경계 밖으로 새지 않는다.
