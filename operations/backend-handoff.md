# 백엔드 공유와 프론트 연동 인수인계

- 상태: `In Review`
- 기준일: 2026-09-12
- 공유 범위: 문서는 작업 브랜치로만 공유한다. 백엔드 PR #2는 main에 병합했고 검증한 ARM64 이미지를 게시했다. 실제 맥미니 교체는 명령별 승인 전이며 실행하지 않았다. 새 docs PR 생성과 기존 PR #7 답글 게시는 이번 문서 변경에서 제외한다.
- 기획 기준: docs main `8d07ff3`의 요구사항과 설계. 미승인 제안은 기준 문서에 반영하지 않는다.

## 먼저 확인할 곳

| 목적 | 기준 문서 |
| --- | --- |
| 프론트의 요청·폴링·오류 처리 | [프론트 연동 안내](https://github.com/Dynamic-Juo/be/blob/38bd16263afbf79daffd67878277c3af0a4a5d51/docs/frontend-integration.md) |
| 요청·응답 필드와 상태 | [백엔드 API 계약](https://github.com/Dynamic-Juo/be/blob/38bd16263afbf79daffd67878277c3af0a4a5d51/docs/api-reference.md) |
| Swagger와 OpenAPI 구현 | [FastAPI 경로](https://github.com/Dynamic-Juo/be/blob/38bd16263afbf79daffd67878277c3af0a4a5d51/backend/app.py), [응답 스키마](https://github.com/Dynamic-Juo/be/blob/38bd16263afbf79daffd67878277c3af0a4a5d51/backend/schemas.py) |
| 배포 준비 당시의 상세 기록 | [백엔드 인수인계](https://github.com/Dynamic-Juo/be/blob/38bd16263afbf79daffd67878277c3af0a4a5d51/docs/handoff.md) |
| 보안·정확성 점검과 남은 제한 | [2026-09-11 중간 점검](../evaluations/2026-09-11-midpoint-review.md) |
| 기획 변경 승인 요청 | [공개 MVP 검토안](../rfcs/public-mvp-readiness.md) |

위 GitHub 링크는 main에 병합한 커밋 `38bd162`를 고정해 가리킨다. 실행 서버에 배포됐다는 뜻은 아니다. 백엔드 인수인계의 준비 시점 기록과 아래 실제 병합·CI 결과를 구분한다. 상세 API 명세는 be에 두고 이 문서에서는 복사하지 않는다.

## 코드와 배포를 구분한다

| 대상 | 기준 | 상태 |
| --- | --- | --- |
| 문서 공유 | docs `docs/midpoint-review` | 작업 브랜치로 공유, 새 PR·기존 PR 수정 없음 |
| 백엔드 변경 | be main `38bd16263afbf79daffd67878277c3af0a4a5d51` | [BE PR #2](https://github.com/Dynamic-Juo/be/pull/2) 병합 완료, 실제 서버 배포 미실행 |
| 배포 이미지 | [main CI](https://github.com/Dynamic-Juo/be/actions/runs/34625602926) | ARM64 빌드·격리 테스트·GHCR 게시 성공 |
| 기존 개발계 | 과거 기록의 `conan-staging`, 이미지 `conan-be:472aff7` | 브라우저 확인만 수행, 서버 명령과 이미지 교체는 하지 않음 |
| 일반 사용자 운영계 | 생성·공개 여부를 이번에 변경하지 않음 | 공개 전 보안·품질 검증과 별도 승인 필요 |

과거 배포 기록의 개발 API는 `https://conan-api-dev.dotseven.cloud`다. Cloudflare Access는 소유자 이메일만 허용한 것으로 기록돼 있다. 현재 서버 환경변수와 Access 정책 전체를 이번 작업에서 조회한 것은 아니다.

게시 로그에서 확인한 고정 이미지는 `ghcr.io/dynamic-juo/be@sha256:c6e1091c982e528140b06a708573756f6598ace6f43eed6a6b83bf5b5419bec0`이다. `sha-38bd16263afbf79daffd67878277c3af0a4a5d51` 태그도 게시됐지만 실제 배포 승인은 digest 기준으로 받는다. 레지스트리 게시 성공이 맥미니의 이미지 확보·실행 성공을 뜻하지 않는다.

2026-09-12 API·Swagger 보완 때의 로컬 모의 검증은 `328 passed, 2 warnings`다. 자막 기본값을 기존 manual로 복원한 be `5ed4441`에서는 전체 `329 passed, 2 warnings (7.53초)`를 확인했다. Python DNS/TCP 차단 fixture를 사용했으며 실제 영상·외부 제공자·맥미니 컨테이너 검증이 아니다. 별도의 [PR ARM64 CI](https://github.com/Dynamic-Juo/be/actions/runs/34625294517)는 성공했고, main에서도 ARM64 이미지 빌드와 `--network none` 테스트가 통과했다. 이미지 게시 결과는 위 표를 따른다. 기존 점검 보고서의 314건은 2026-09-11 당시 수치로 보존한다.

## 2026-09-12 개발계 확인 범위

| 확인 | 관찰 결과 | 확인하지 못한 것 |
| --- | --- | --- |
| 사용자의 이메일 인증 후 `GET /` 요청 보고 | 사용자 보고는 404 응답이다. 작업 복사본에서 확인한 배포 기준 코드에도 `GET /` 경로가 등록돼 있지 않다. | 수정 브랜치 배포 여부, Swagger와 API 정상 동작 |
| 인증하지 않은 외부 `GET /health` 요청 | Cloudflare Access 로그인 화면이 먼저 나타난다. | 백엔드 `/health` 응답 |
| 인증 뒤 `/health`, `/docs`, `/openapi.json` 요청 | 수행하지 않음 | 헬스 체크, Swagger UI와 배포 스키마 |

루트 404는 등록되지 않은 경로의 응답이며 API 전체 장애 근거가 아니다. Access 로그인 화면도 앞단 인증 동작만 확인하므로 백엔드 헬스 체크 성공으로 해석하지 않는다.

## Swagger는 어디에서 보는가

- [Swagger UI](https://conan-api-dev.dotseven.cloud/docs)
- [OpenAPI JSON](https://conan-api-dev.dotseven.cloud/openapi.json)
- [ReDoc](https://conan-api-dev.dotseven.cloud/redoc)

FastAPI 코드에 구성된 경로를 개발 API 주소와 조합한 접근 주소다. 이번 수정안은 배포하지 않았으므로 현재 도메인의 문서가 수정 브랜치와 같다고 가정하지 않는다. 루트 경로의 인증 후 응답은 사용자 보고이며, 인증 뒤 Swagger와 헬스 체크는 직접 확인하지 않았다. 수정 스키마 반영 확인은 실제 배포 후 수행한다.

Swagger를 프론트 담당자에게 보여주기 위해 Access를 전체 공개로 바꾸지 않는다. 담당 이메일을 확인해 기존 앱의 허용 대상을 제한적으로 추가하는 작업이 필요하며 아직 실행하지 않았다. 같은 API origin에서 Swagger를 읽고 요청을 시험하는 것과 Vercel 프론트에서 교차 출처 요청을 보내는 것은 별도 검증이다. 자세한 로그인·CORS·OPTIONS 조건은 프론트 연동 안내를 따른다.

## 공유 내용이 갈라진 항목

| 항목 | 기획·리뷰 근거 | 구현·기록 | 확인 사항 |
| --- | --- | --- | --- |
| 자막 | [기획 본문](../design/ai-pipeline.md)은 MVP 자막 미사용이다. [PR #7 수동 CC 의견](https://github.com/Dynamic-Juo/docs/pull/7#discussion_r3958898775)은 직접 작성한 CC 도입을 긍정적으로 검토하지만 전문과 다를 수 있다고 지적한다. | 기존 동작과 공유 대상 기본값은 manual이다. 작성자가 등록한 수동 CC가 있으면 사용하고, 없으면 STT로 전환한다. 수동 CC도 발화 전문이나 정확성을 보증하지 않는다. | 기존 동작은 유지한다. 기획 본문과의 차이는 PR #7 후속 정리에서 다루며, 이 문서를 정책 승인으로 사용하지 않는다. |
| 주장 개수 | [PRD R-03](../project/prd.md)은 검증 가능한 주장을 모두 처리한다. | 기본 max_claims=0은 개수 제한 없음이다. 시간 예산은 있으며 추출 완전성이 검증됐다는 뜻은 아니다. | 실제 정답 영상의 누락·중복과 시간 초과를 측정한다. |
| 주장 추출 | [기존 PR의 LLM 사용 기록](https://github.com/Dynamic-Juo/docs/pull/7#discussion_r3989716198)이 있다. | LLM 경로와 배포 예시가 구현돼 있다. 공통 코드 기본값은 rule이며 실제 실행은 환경 설정에 따른다. | 로컬 모의 검증과 실제 제공자 호출 검증을 구분한다. 현재 서버 값을 미확인 상태에서 LLM 실호출 성공으로 표현하지 않는다. |
| 판정과 근거 | [근거 정책](../design/evidence-policy.md)은 근거와 일치·근거와 불일치·근거 부족으로 구분한다. | supported·refuted·unverified의 세 판정, 근거 출처와 판정 이유가 구현돼 있다. 실패·시간 초과는 별도 처리 상태다. | 실제 검색·제공자 근거 품질은 검증되지 않았다. FE는 판정과 처리 상태를 섞지 않는다. |
| 결과 폴링 | [결과 UI](../design/result-ui.md)는 진행 상태와 순차 결과를 구분한다. | 접수 뒤 상태와 부분·최종 결과를 조회하는 API 계약이 구현돼 있다. | 로컬 모의 검증은 통과했지만 개발계 인증 후 접수부터 종료까지의 통합 검증은 하지 않았다. |

## 승인·완료로 다루지 않는 항목

| 항목 | 현재 상태 |
| --- | --- |
| 주장 하나 안의 검색 제공자 병렬화 | 미구현이며 성능 개선 제안이다. 주장 간 최대 3건 병렬 구현과 구분한다. |
| 여러 얼굴 처리 | 미구현 후속 항목이며 현재 결과를 다중 얼굴 전체에 대한 판정으로 해석하지 않는다. |
| 영상 전체 AI 생성 탐지 제외 | [PR #7의 제외 의견](https://github.com/Dynamic-Juo/docs/pull/7#discussion_r3958912896)은 검토 제안이다. 확정된 범위 변경이 아니며, 현재 미구현인 영상 전체 AI 생성 축의 완료를 뜻하지 않는다. |

상세 제안과 승인은 [공개 MVP 검토안](../rfcs/public-mvp-readiness.md)에서 추적한다. 이 문서는 기획의 요구사항·일정·역할을 변경하지 않는다.

## 프론트 담당자와 확인할 것

| 확인 항목 | 담당자 | 상태 | 확인 시점 |
| --- | --- | --- | --- |
| 프론트 담당자의 개발계 Access 허용 이메일 | 조정준 팀장 | 로그인 확인에 사용한 계정 외 추가 대상 미확인 | 연동 전 |
| Vercel 고정 프론트 Origin | 조정준 팀장 | 사용자 답변 대기 | 미정 |
| 로그인 후 Swagger 열기와 schema 확인 | 나정균 팀원 | 루트 404만 확인, Swagger 미확인 | 실제 배포 후 |
| 접수·부분 응답·종료·404·429 처리 검수 | 조정준 팀장, 나정균 팀원 | API 계약 공유, 개발계 통합 검증 미완료 | 실제 배포 후 |
| 자막 기준의 기획 반영과 기존 #7 답변 | 미정 | manual 동작은 유지, 기획 정합성 정리는 이번 공유 밖 | PR #7 후속 정리 시 |

API 키와 Access 서비스 토큰은 프론트 코드나 공개 문서에 넣지 않는다. 담당자 정보·일정을 확인하지 않은 항목은 추정해 확정하지 않는다.

## 다음 공유 순서

문서 변경은 `docs/midpoint-review` 브랜치로만 공유하고 새 docs PR을 만들지 않는다. 기존 PR #7 답글은 사용자가 다음 날 별도로 마무리하며 이번 변경에서는 게시하거나 수정하지 않는다.

백엔드 [PR #2](https://github.com/Dynamic-Juo/be/pull/2)는 main에 병합했다. 실제 개발계 배포는 아직 실행하지 않았다. 서버 조회·교체는 명령별 대상·영향을 알리고 승인받은 뒤 진행한다. 실제 배포 뒤 정확한 커밋과 이미지 기준을 기록하고, 인증된 `/health`·`/docs`·`/openapi.json`과 프론트의 접수·폴링 흐름을 검증한다. 키·환경값·기존 이미지·볼륨·Tunnel을 보존하고 기존 `conan-staging`의 `deepcheck-api`만 교체한다.
