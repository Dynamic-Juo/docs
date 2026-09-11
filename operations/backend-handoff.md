# 백엔드 공유와 프론트 연동 인수인계

- 상태: `In Review`
- 기준일: 2026-09-12
- 공유 범위: 코드·문서를 작업 브랜치로 올린다. 새 PR 생성, 기존 PR 답글, main 병합과 배포는 이번 범위에서 제외한다.
- 기획 기준: docs main `8d07ff3`의 요구사항과 설계. 미승인 제안은 기준 문서에 반영하지 않는다.

## 먼저 확인할 곳

| 목적 | 기준 문서 |
| --- | --- |
| 프론트의 요청·폴링·오류 처리 | [프론트 연동 안내](https://github.com/Dynamic-Juo/be/blob/fix/midpoint-hardening/docs/frontend-integration.md) |
| 요청·응답 필드와 상태 | [백엔드 API 계약](https://github.com/Dynamic-Juo/be/blob/fix/midpoint-hardening/docs/api-reference.md) |
| Swagger와 OpenAPI 구현 | [FastAPI 경로](https://github.com/Dynamic-Juo/be/blob/fix/midpoint-hardening/backend/app.py), [응답 스키마](https://github.com/Dynamic-Juo/be/blob/fix/midpoint-hardening/backend/schemas.py) |
| 구현·검증·배포 공유 상태 | [백엔드 인수인계](https://github.com/Dynamic-Juo/be/blob/fix/midpoint-hardening/docs/handoff.md) |
| 보안·정확성 점검과 남은 제한 | [2026-09-11 중간 점검](../evaluations/2026-09-11-midpoint-review.md) |
| 기획 변경 승인 요청 | [공개 MVP 검토안](../rfcs/public-mvp-readiness.md) |

위 GitHub 링크는 작업 브랜치를 가리킨다. main이나 실행 서버에 반영됐다는 뜻이 아니다. 상세 API 명세는 be에 두고 이 문서에서는 복사하지 않는다.

## 코드와 배포를 구분한다

| 대상 | 기준 | 상태 |
| --- | --- | --- |
| 문서 공유 | docs `docs/midpoint-review` | 작업 브랜치로 공유, 새 PR·기존 PR 수정 없음 |
| 백엔드 변경 | be `fix/midpoint-hardening` | 수정 코드·API 계약·Swagger 설명을 작업 브랜치로 공유 |
| 기존 개발계 | 과거 기록의 `conan-staging`, 이미지 `conan-be:472aff7` | 이번에 조회하거나 교체하지 않음 |
| 일반 사용자 운영계 | 생성·공개 여부를 이번에 변경하지 않음 | 공개 전 보안·품질 검증과 별도 승인 필요 |

과거 배포 기록의 개발 API는 `https://conan-api-dev.dotseven.cloud`다. Cloudflare Access는 소유자 이메일만 허용한 것으로 기록돼 있다. 현재 서버 상태·환경변수·정책을 이번 작업에서 조회한 것은 아니다.

2026-09-12 추가 검증은 API·Swagger 계약을 포함해 로컬 모의 테스트 `328 passed, 2 warnings`다. Python DNS/TCP 차단 fixture를 사용했으며 실제 영상·외부 제공자·배포 컨테이너·GitHub Actions를 실행한 결과가 아니다. 코드 변경은 be `e8176d8`, CI 변경은 `729be26`이다. 기존 점검 보고서의 314건은 2026-09-11 당시 수치로 보존한다.

## Swagger는 어디에서 보는가

- [Swagger UI](https://conan-api-dev.dotseven.cloud/docs)
- [OpenAPI JSON](https://conan-api-dev.dotseven.cloud/openapi.json)
- [ReDoc](https://conan-api-dev.dotseven.cloud/redoc)

FastAPI 코드에 구성된 경로를 개발 API 주소와 조합한 접근 주소다. 이번 수정안은 배포하지 않았으므로 현재 도메인의 문서가 수정 브랜치와 같다고 가정하지 않는다. 실제 로그인 후 접속과 수정 스키마 반영 확인은 배포 승인 후 수행한다.

Swagger를 프론트 담당자에게 보여주기 위해 Access를 전체 공개로 바꾸지 않는다. 담당 이메일을 확인해 기존 앱의 허용 대상을 제한적으로 추가하는 작업이 필요하며 아직 실행하지 않았다. 같은 API origin에서 Swagger를 읽고 요청을 시험하는 것과 Vercel 프론트에서 교차 출처 요청을 보내는 것은 별도 검증이다. 자세한 로그인·CORS·OPTIONS 조건은 프론트 연동 안내를 따른다.

## 공유 내용이 갈라진 항목

| 항목 | 기획·리뷰 근거 | 구현·기록 | 확인 사항 |
| --- | --- | --- | --- |
| 자막 | [기획 본문](../design/ai-pipeline.md)은 MVP 자막 미사용이다. [PR #7 수동 CC 의견](https://github.com/Dynamic-Juo/docs/pull/7#discussion_r3958898775)은 직접 작성한 CC 도입을 긍정적으로 검토하지만 전문과 다를 수 있다고 지적한다. | 수정 브랜치 기본은 off, 과거 서버 기록은 manual이다. 환경을 덮어쓰지 않았다. | STT 기본과 수동 CC 우선 중 최종 정책을 확인하고 기획·설정·API 설명을 함께 맞춘다. |
| 주장 개수 | [PRD R-03](../project/prd.md)은 검증 가능한 주장을 모두 처리한다. | 기본 max_claims=0은 개수 제한 없음이다. 시간 예산은 있으며 추출 완전성이 검증됐다는 뜻은 아니다. | 실제 정답 영상의 누락·중복과 시간 초과를 측정한다. |
| 주장 추출 | [기존 PR의 LLM 사용 기록](https://github.com/Dynamic-Juo/docs/pull/7#discussion_r3989716198)이 있다. | LLM 경로와 배포 예시가 구현돼 있다. 공통 코드 기본값은 rule이며 실제 실행은 환경 설정에 따른다. | 현재 서버 값을 미확인 상태에서 LLM 실호출 성공으로 표현하지 않는다. |
| 판정 이름 | [근거 정책](../design/evidence-policy.md)은 근거와 일치·근거와 불일치·근거 부족으로 구분한다. | 코드의 unverified 표시는 근거 부족이다. 실패·시간 초과는 별도 처리 상태다. | FE는 판정과 처리 상태를 섞지 않는다. |

PR #7의 전체 AI 생성 탐지 제외 의견도 [기존 리뷰](https://github.com/Dynamic-Juo/docs/pull/7#discussion_r3958912896)에 있지만 확정된 범위 변경으로 간주하지 않는다. 상세 제안과 승인은 공개 MVP 검토안에서 추적한다. 이 문서는 기획의 요구사항·일정·역할을 변경하지 않는다.

## 프론트 담당자와 확인할 것

| 확인 항목 | 담당자 | 상태 | 확인 시점 |
| --- | --- | --- | --- |
| 개발계 Access 허용 이메일 | 조정준 팀장 | 사용자 답변 대기 | 미정 |
| Vercel 고정 프론트 Origin | 조정준 팀장 | 사용자 답변 대기 | 미정 |
| 로그인 후 Swagger 열기와 schema 확인 | 나정균 팀원 | 배포 미실행 | 배포 승인 후 |
| 접수·부분 응답·종료·404·429 처리 검수 | 조정준 팀장, 나정균 팀원 | API 계약 공유 단계 | 미정 |
| 자막 최종 정책과 기존 #7 답변 | 미정 | 결정 대기 | 미정 |

API 키와 Access 서비스 토큰은 프론트 코드나 공개 문서에 넣지 않는다. 담당자 정보·일정을 확인하지 않은 항목은 추정해 확정하지 않는다.

## 다음 공유 순서

현재 브랜치 내용을 검토하고 기존 PR #7의 질문·미답변을 정리한다. 사용자가 답변 게시를 요청하면 그때 기존 PR에 답변한다. 이후 문서 PR·코드 반영·개발계 배포를 각각 승인된 범위에서 진행한다. 이번 요청은 브랜치 공유까지만이며 자동 배포하지 않는다.
