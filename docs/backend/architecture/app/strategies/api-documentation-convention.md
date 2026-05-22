# OpenAPI 문서화 컨벤션

이 문서는 app 계층 REST API의 OpenAPI 문서화 규칙을 정리한다.

## 목적

- API 구현과 외부 계약 문서가 어긋나지 않게 한다.
- Request/Response DTO, error response, version, security 요구사항을 OpenAPI에 드러낸다.
- 클라이언트가 endpoint를 사용할 때 필요한 계약 정보를 코드 가까이에 유지한다.

## 적용 범위

- Controller와 endpoint method의 OpenAPI annotation
- Request/Response schema 문서
- 공통 response, error response, security scheme, tag 구성
- API version과 deprecation 표시

REST resource 설계는 [resource-design-convention](resource-design-convention.md)이 소유한다.
DTO field의 required, nullable, optional 의미는 [dto-convention](dto-convention.md)이 소유한다.

## 책임

- endpoint의 목적, 입력, 출력, 오류, 보안 요구사항을 문서화한다.
- DTO schema가 API 계약을 충분히 설명하게 한다.
- 공통 response와 error response를 재사용 가능한 component로 관리한다.
- breaking change와 deprecation 정보를 version 정책과 연결한다.

## 전체 흐름

```text
Controller endpoint
  -> tag
  -> operationId
  -> request schema
  -> success response schema
  -> error response references
  -> security and deprecation metadata
```

## 세부 규칙

### Operation

- 모든 public endpoint는 summary와 operationId를 가진다.
- operationId는 [naming-convention](naming-convention.md)의 `{verb}{Resource}` 형식을 따른다.
- tag는 resource 단위로 묶는다.
- description에는 business rule 전체가 아니라 API 사용자가 알아야 하는 계약 제약만 적는다.

### Schema

- Request DTO와 Response DTO field에는 required, nullable, example, description을 필요한 만큼 제공한다.
- nullable field는 null의 의미를 설명한다.
- enum은 가능한 값을 문서에 노출한다.
- 날짜, 금액, ID, cursor token처럼 format이 중요한 field는 예시를 둔다.

### Response

- 성공 응답은 공통 envelope 안의 실제 data schema를 문서화한다.
- 오류 응답은 공통 error schema를 참조한다.
- endpoint별로 발생 가능한 대표 error code를 문서화한다.
- validation error, authorization error, not found, conflict 같은 공통 오류는 shared response component를 재사용한다.

### Security와 version

- 인증이 필요한 endpoint는 security requirement를 명시한다.
- admin endpoint는 admin 권한 요구사항을 문서화한다.
- deprecated endpoint는 deprecation metadata와 대체 endpoint를 함께 적는다.
- 신규 version이 존재하면 v1과 v2의 차이를 문서에 드러낸다.

## 금지 규칙

- public endpoint를 OpenAPI 문서 없이 추가하지 않는다.
- `operationId`를 자동 생성값에 맡기지 않는다.
- Request DTO nullable field의 의미를 문서화하지 않은 채 노출하지 않는다.
- 오류 응답을 성공 schema만으로 대체하지 않는다.
- endpoint별 error response를 서로 다른 임의 JSON 예시로 작성하지 않는다.
- 보안이 필요한 endpoint를 anonymous endpoint처럼 문서화하지 않는다.
- deprecated endpoint를 문서에서 조용히 삭제하지 않는다.

## 예외와 경계

- internal actuator, health check, static resource는 business API OpenAPI 문서 대상에서 제외할 수 있다.
- provider callback은 provider 문서가 원천 계약일 수 있지만 내부 운영 문서에는 최소한의 endpoint 설명을 남긴다.
- OpenAPI annotation이 과도해지면 common OpenAPI component나 custom annotation으로 중복을 줄인다.

## 완료 기준

- 신규 endpoint는 URI, method, request, response, error, security, version 정보를 OpenAPI에서 확인할 수 있다.
- DTO schema의 required와 nullable 정보가 실제 serialization 계약과 일치한다.
- 공통 error response와 response envelope가 OpenAPI component로 재사용된다.
