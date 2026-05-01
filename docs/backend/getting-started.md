# Backend Getting Started

## 기술 스택

| 영역 | 기술 |
|------|------|
| 언어 | Kotlin 1.9.25 |
| 프레임워크 | Spring Boot 3.5.11 |
| 데이터 접근 | Spring Data JPA / Hibernate |
| 데이터베이스 | MySQL 8.0, H2 |
| 빌드 | Gradle 8.x (Kotlin DSL) |
| 테스트 | JUnit 5, Spring Boot Test |
| 런타임 | Java 17 |

## 로컬 실행

```bash
docker-compose -f docker-compose-local.yml up -d
./gradlew build -x test --parallel
./gradlew :{app-module}:bootRun --args='--spring.profiles.active=local'
```

## 테스트

```bash
./gradlew test
```

## 프로필 / 환경 변수

| 항목 | 설명 | 근거 |
|------|------|------|
| `local` | 로컬 개발 프로필 | `--spring.profiles.active=local` |
| `storage` | MySQL DB 설정 프로필 | 기존 backend 실행 안내 |

## 확인 필요

- 실제 프로젝트 적용 시 `{app-module}` 값을 코드베이스의 실행 모듈명으로 교체한다.
- 프로젝트별 필수 환경 변수와 의존 서비스는 코드와 설정 파일을 확인한 뒤 추가한다.
