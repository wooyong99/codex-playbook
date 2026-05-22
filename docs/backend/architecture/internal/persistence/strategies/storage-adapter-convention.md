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

QueryDsl 쿼리 작성 규칙은 [querydsl-convention](querydsl-convention.md)이 소유한다.

## 책임

- application Port 인터페이스를 구현한다.
- 단순 저장과 조회는 JpaRepository에 위임한다.
- 복잡한 검색, Projection, pagination은 QueryDslRepository에 위임한다.
- 모든 반환값을 Domain 객체 또는 application Port 타입으로 변환한다.

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
| Adapter | `{Entity}Adapter` |
| JpaRepository | `{Entity}JpaRepository` |
| QueryDslRepository | `{Entity}QueryDslRepository` |
| JPA Entity | `{Entity}Entity` |
| 변환 파일 | `{Entity}Extension.kt` |

### Adapter 구조

- Adapter는 `@Repository`로 선언한다.
- Adapter는 application 계층의 Port 인터페이스를 구현한다.
- Adapter는 JpaRepository와 QueryDslRepository를 생성자 주입받는다.
- Adapter는 JPA Entity를 그대로 반환하지 않고 Domain 또는 Port Result로 변환한다.

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
- `@OneToMany`를 불필요하게 선언하지 않는다.
- `FetchType.EAGER`를 사용하지 않는다.
- `open-in-view: true`에 의존하지 않는다.
- 단순 Repository에 복잡한 동적 조건과 Projection을 계속 추가하지 않는다.

## 예외와 경계

- 단일 조회가 단순하지만 성능 튜닝이 필요하면 QueryDslRepository로 옮길 수 있다.
- Entity와 Domain 구조가 거의 같아도 변환 책임은 분리한다.
- 저장소 구현 기술이 JPA가 아니면 실제 기술명에 맞추되 Port 외부 노출 금지 원칙은 유지한다.

## 완료 기준

- Adapter가 application Port를 구현하고 저장 기술 세부사항을 숨긴다.
- JpaRepository와 QueryDslRepository의 책임이 분리되어 있다.
- Entity와 Domain 변환이 `{Entity}Extension.kt`에 모여 있다.
- storage 밖으로 JPA Entity가 노출되지 않는다.
