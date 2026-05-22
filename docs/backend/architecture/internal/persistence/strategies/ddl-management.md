# DDL Management 컨벤션

이 문서는 storage Entity 변경과 DDL 파일 변경을 함께 관리하는 전략을 정리한다.

## 목적

- Entity와 실제 DB schema의 불일치를 막는다.
- DDL 파일 위치와 변경 단위를 고정한다.
- migration 도구가 없는 프로젝트에서도 schema 변경 흔적을 문서화한다.

## 적용 범위

- 신규 table DDL
- 기존 table schema 변경
- 초기 seed data 파일
- Entity 변경과 DDL 변경의 commit 단위

## 책임

- DDL 파일 경로 규칙을 정의한다.
- Entity 변경 시 함께 갱신해야 하는 schema 파일을 명확히 한다.
- Flyway/Liquibase 없는 수동 DDL 관리 방식을 고정한다.

## 전체 흐름

```text
{Entity}Entity change
  -> sql/{domain}/{table}.sql update
  -> same commit
```

## 세부 규칙

### 파일 위치

| 파일 종류 | 위치 |
|----------|------|
| 테이블 DDL | `sql/{domain}/{table}.sql` |
| 초기 seed 데이터 | `sql/{domain}/seed.sql` |

### 버전 관리

- Flyway/Liquibase 스타일의 버전 접두사를 사용하지 않는다.
- 스키마 변경 시 해당 `.sql` 파일을 직접 수정한다.
- Entity 신규 생성 또는 변경과 DDL 변경은 같은 commit에 포함한다.

## 금지 규칙

- `V1__`, `V2__` 같은 버전 접두사를 파일명에 사용하지 않는다.
- Entity 변경과 DDL 변경을 다른 commit으로 분리하지 않는다.
- `sql/` 외부 위치에 DDL 파일을 두지 않는다.
- DDL 변경 없이 Entity 컬럼, 타입, nullability만 수정하지 않는다.

## 예외와 경계

- 실제 프로젝트가 Flyway/Liquibase를 사용하면 이 문서를 migration 전략 문서로 교체한다.
- 운영 DB migration 절차가 별도 정책에 있으면 해당 정책을 우선한다.
- seed data가 환경별로 달라지면 환경별 파일 분리 기준을 별도 문서로 둔다.

## 완료 체크리스트

아래 항목을 모두 충족해야 완료로 판정한다.

- [ ] `금지 규칙` 섹션의 각 항목을 위반하는 코드, 문서, 설정 변경이 없다.
- [ ] DDL 파일이 `sql/{domain}/{table}.sql` 경로에 있다.
- [ ] Entity 변경과 DDL 변경이 같은 변경 단위에 포함되어 있다.
- [ ] migration 도구 사용 여부와 파일명 규칙이 문서 또는 빌드 설정에 명시되어 있다.
