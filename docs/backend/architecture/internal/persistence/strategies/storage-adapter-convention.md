# Storage Adapter 컨벤션

이 문서는 application 저장소 Port를 storage 구현체로 연결하는 `Storage Adapter` 전략을 정리한다.

## 목적

- application Port 뒤에 JPA와 QueryDsl 구현 세부사항을 숨긴다.
- 단순 CRUD와 복잡 쿼리 책임을 분리한다.
- Entity와 Domain 변환 책임을 persistence 경계 안에 둔다.

## 적용 범위

- `{Entity}Adapter`
- `{Entity}JpaRepository`
- `{Entity}QueryDslRepository`
- `{Entity}Entity`
- `{Entity}Extension.kt`
- JPA 전환 전 runtime 저장소 역할을 하는 in-memory adapter

QueryDsl 쿼리 작성 규칙은 [querydsl-convention](querydsl-convention.md)이 소유한다.

## 책임

- application Port 인터페이스를 구현한다.
- 단순 저장과 조회는 JpaRepository에 위임한다.
- 복잡한 검색, Projection, pagination은 QueryDslRepository에 위임한다.
- 모든 반환값을 Domain 객체 또는 application Port 타입으로 변환한다.
- 임시 in-memory adapter도 저장 기술 세부사항을 숨기고 application에는 Port 계약만 노출한다.

## 전체 흐름

```text
application Port
  -> {Entity}Adapter
    -> {Entity}JpaRepository
    -> {Entity}QueryDslRepository
    -> {Entity}Extension.toDomain()
    -> {Entity}Extension.toEntity()
```

## 세부 규칙

### 네이밍

| 구성 요소 | 패턴 |
|-----------|------|
| Application Port | `{Aggregate}RepositoryPort` |
| Adapter | `{Entity}Adapter` |
| JpaRepository | `{Entity}JpaRepository` |
| QueryDslRepository | `{Entity}QueryDslRepository` |
| JPA Entity | `{Entity}Entity` |
| 변환 파일 | `{Entity}Extension.kt` |

- 저장소 Port 인터페이스는 application 계층에 두고 `{Aggregate}RepositoryPort`로 이름 짓는다.
- 저장소 Port 이름을 `Store`, `Repository`, `Gateway`만으로 끝내지 않는다.
- persistence 구현체는 application Port 이름의 `Port` suffix를 반복하지 않고 저장 기술 또는 adapter 역할이 드러나게 이름 짓는다.

### Adapter 구조

- Adapter는 `@Repository`로 선언한다.
- Adapter는 application 계층의 Port 인터페이스를 구현한다.
- Adapter는 JpaRepository와 QueryDslRepository를 생성자 주입받는다.
- Adapter는 JPA Entity를 그대로 반환하지 않고 Domain 또는 Port Result로 변환한다.
- JPA를 아직 사용하지 않는 임시 adapter도 `internal/persistence` 아래에 두고, Map, lock, id generator 같은 저장 세부사항을 application으로 노출하지 않는다.

### Repository 분리

- JpaRepository는 저장, 삭제, ID 기반 조회, 단순 조건 조회, 존재 여부 확인만 담당한다.
- QueryDslRepository는 동적 조건 검색, 복잡한 조인, Projection, 집계, pagination을 담당한다.
- 단순 Spring Data 메서드명 쿼리가 길어지면 QueryDslRepository로 옮긴다.

### Entity 작성

- Entity는 JPA 매핑에만 집중한다.
- Entity는 `class`로 선언하고 `data class`로 만들지 않는다.
- `@Column(nullable = false)`로 NOT NULL 제약을 명시한다.
- Enum은 `@Enumerated(EnumType.STRING)`을 사용한다.
- 연관관계는 `FetchType.LAZY`를 기본으로 한다.
- 생성/수정 시간이 필요하면 `BaseEntity` 같은 공통 감사 필드를 사용한다.

### Domain 변환

- 변환 로직은 `{Entity}Extension.kt`의 extension function으로 작성한다.
- `toDomain()`은 domain 모델의 `reconstitute()`를 사용한다.
- `toEntity()`는 storage Entity 생성을 담당한다.
- Entity나 Domain 클래스 내부에 변환 메서드를 넣지 않는다.

## 금지 규칙

- JPA Entity를 storage 밖으로 반환하지 않는다.
- Entity에 비즈니스 로직을 넣지 않는다.
- Entity나 Domain 클래스 내부에 변환 로직을 넣지 않는다.
- 저장소 Port 인터페이스를 `*Port` suffix 없이 만들지 않는다.
- 저장소 Port를 `Store`, `Repository`, `Gateway` 같은 non-Port 계약명으로 새로 정의하지 않는다.
- application production source에 저장소 adapter 구현체를 두지 않는다.
- in-memory 저장소 구현을 단순 테스트 대역처럼 application 내부에 배치하지 않는다.
- `@OneToMany`를 불필요하게 선언하지 않는다.
- `FetchType.EAGER`를 사용하지 않는다.
- `open-in-view: true`에 의존하지 않는다.
- 단순 Repository에 복잡한 동적 조건과 Projection을 계속 추가하지 않는다.

## 예외와 경계

- 단일 조회가 단순하지만 성능 튜닝이 필요하면 QueryDslRepository로 옮길 수 있다.
- Entity와 Domain 구조가 거의 같아도 변환 책임은 분리한다.
- 저장소 구현 기술이 JPA가 아니면 실제 기술명에 맞추되 Port 외부 노출 금지 원칙은 유지한다.

## 완료 체크리스트

아래 항목을 모두 충족해야 완료로 판정한다.

- [ ] `금지 규칙` 섹션의 각 항목을 위반하는 코드, 문서, 설정 변경이 없다.
- [ ] 저장소 Port 인터페이스 이름이 `{Aggregate}RepositoryPort` 또는 동등한 `*Port` suffix 패턴을 따른다.
- [ ] Adapter가 application Port를 구현하고 저장 기술 세부사항을 숨긴다.
- [ ] runtime 저장소 adapter는 구현 기술과 무관하게 `internal/persistence` 아래에 있다.
- [ ] application production source에는 저장소 Port 인터페이스만 있고 adapter 구현체가 없다.
- [ ] JpaRepository와 QueryDslRepository의 책임이 분리되어 있다.
- [ ] Entity와 Domain 변환이 `{Entity}Extension.kt`에 모여 있다.
- [ ] storage 밖으로 JPA Entity가 노출되지 않는다.
