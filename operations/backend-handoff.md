# 백엔드 공유와 프론트 연동 인수인계

- 상태: `In Review`
- 기준일: 2026-09-13
- 공유 범위: 문서는 작업 브랜치로만 공유한다. 백엔드 PR #2는 main에 병합했고 검증한 ARM64 이미지를 게시했다. 실제 맥미니 교체는 명령별 승인 전이며 실행하지 않았다. 새 docs PR 생성과 기존 PR #7 답글 게시는 이번 문서 변경에서 제외한다.
- 기획 기준: docs main `8d07ff3`의 요구사항과 설계. 미승인 제안은 기준 문서에 반영하지 않는다.

## 먼저 확인할 곳

사용자는 백엔드 배포를 본인이 담당하며 제3자 승인 없이 main 병합 후 개발계 자동 배포를 요청했다. [BE PR #4](https://github.com/Dynamic-Juo/be/pull/4)의 자동 pull 코드와 완료 결과 영속 복원을 main `cf550f95c0dd6fc49631a2e824bc88bffc140fde`로 병합했다. 통합 모의 회귀 722개 및 [실제 PR ARM64 빌드·격리 테스트](https://github.com/Dynamic-Juo/be/actions/runs/34736248321)가 통과했다. launchd·전용 인증정보·최초 서버 전환은 미실행이므로 현재 자동 배포가 켜졌다는 뜻은 아니다. 새 main 이미지 게시 결과도 PR 빌드와 별도로 확인해야 한다. 상세 계약은 [자동 배포 런북](https://github.com/Dynamic-Juo/be/blob/cf550f95c0dd6fc49631a2e824bc88bffc140fde/docs/development-cd-runbook.md)을 따른다. 아래 PR #3의 제3자 승인형 구현은 기존 이력이며 신규 자동 모드의 사용자 결정과 구분한다.

2026-09-13 [BE PR #3](https://github.com/Dynamic-Juo/be/pull/3)을 main `513f53668ad633bb2de2360cb924645ce8318a58`로 병합했다. CI/CD 컨트롤러, 자막 기본 off와 선택 옵션, 소스 감사·파이프라인 문서를 통합했다. 병합은 서버 배포 완료를 뜻하지 않는다. 아래 PR #2와 서버 조회 수치는 9월 12일 기록이다.

| 통합 항목 | 확인 결과 | 남은 확인 |
| --- | --- | --- |
| 코드 통합 | CI/CD `43eae84`, 자막 정책 `1b58097`, 소스 문서 `6c795ab`을 통합했다. 새 CD Compose도 자막 기본값을 off로 수정했다. PR #3 최신 HEAD의 실제 CI 성공 후 main에 병합했다. | 신규 이미지 배포 |
| 로컬 회귀 | 통합 코드 `e306349`에서 모의 테스트 691개가 통과했다. | 실영상·실제 제공자 검증은 별도 |
| 실제 GitHub Actions | 첫 실행의 테스트 이미지 누락을 수정한 뒤 PR 검증이 성공했다. 병합 후 [main 실행](https://github.com/Dynamic-Juo/be/actions/runs/34733471394)에서도 ARM64 빌드·격리 테스트·동일 이미지 GHCR 게시·이미지와 릴리스 서명이 모두 성공했다. | 호스트의 서명 검증·새 이미지 실행은 별도 |
| 개발계 자동 배포 | 사용자 요청에 따라 PR #4에서 제3자 승인 대신 성공한 main CI와 릴리스 서명을 확인하는 자동 모드로 전환한다. 완료 결과를 보존하고 진행 작업 drain 후 단일 서비스를 교체한다. | 전용 Actions/Contents read 인증, 호스트 설치·최초 전환·실제 교체 및 복원 검증 필요 |
| 실제 영상·FE | 승인 후 기존 이미지에서 [실영상 1건](../evaluations/2026-09-13-deployed-video-check.md)이 25초에 종료됐다. STT 3단어·주장 0건이므로 검증 품질이나 제공자 성공을 확인한 것은 아니다. | 새 이미지 실영상·STT 품질·FE 연동 검수 |

최신 [소스 감사](https://github.com/Dynamic-Juo/be/blob/7ae042a/docs/source-audit.md)와 [처리 흐름·프롬프트](https://github.com/Dynamic-Juo/be/blob/7ae042a/docs/pipeline.md)는 백엔드에서 관리한다. 감사의 당시 코드 기준과 통합 이후 변경을 구분한다. 원문 근거 수집, 영상 전체 AI 생성 모델, 공개 API 남용 방지와 강제 시간 제한의 미흡 사항은 이번 배포 코드 통합으로 해결되지 않았다. 논의는 [프로젝트 계획](../project/project-plan.md#리뷰-후속-추적)에서 추적한다.

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
| 기존 개발계 | 승인된 조회에서 `conan-staging`, 이미지 `conan-be:472aff7` | healthy·재시작 0·OOM false, 이미지 교체는 하지 않음 |
| 일반 사용자 운영계 | 생성·공개 여부를 이번에 변경하지 않음 | 공개 전 보안·품질 검증과 별도 승인 필요 |

과거 배포 기록의 개발 API는 `https://conan-api-dev.dotseven.cloud`다. Cloudflare Access는 소유자 이메일만 허용한 것으로 기록돼 있다. 현재 서버 환경변수와 Access 정책 전체를 이번 작업에서 조회한 것은 아니다.

게시 로그에서 확인한 고정 이미지는 `ghcr.io/dynamic-juo/be@sha256:c6e1091c982e528140b06a708573756f6598ace6f43eed6a6b83bf5b5419bec0`이다. `sha-38bd16263afbf79daffd67878277c3af0a4a5d51` 태그도 게시됐지만 실제 배포 승인은 digest 기준으로 받는다. 레지스트리 게시 성공이 맥미니의 이미지 확보·실행 성공을 뜻하지 않는다.

2026-09-12 API·Swagger 보완 때의 로컬 모의 검증은 `328 passed, 2 warnings`다. 자막 기본값을 기존 manual로 복원한 be `5ed4441`에서는 전체 `329 passed, 2 warnings (7.53초)`를 확인했다. Python DNS/TCP 차단 fixture를 사용했으며 실제 영상·외부 제공자·맥미니 컨테이너 검증이 아니다. 별도의 [PR ARM64 CI](https://github.com/Dynamic-Juo/be/actions/runs/34625294517)는 성공했고, main에서도 ARM64 이미지 빌드와 `--network none` 테스트가 통과했다. 이미지 게시 결과는 위 표를 따른다. 기존 점검 보고서의 314건은 2026-09-11 당시 수치로 보존한다.

## 2026-09-12 개발계 확인 범위

승인받은 읽기 전용 점검에서 서버 HEAD `472aff7`, Compose v5.1.2와 기존 Compose 설정 검증 성공을 확인했다. 내부 `/ready`는 ready이며 진행·대기 작업은 0건이었다. CORS는 `http://localhost:3000`만 허용한다. 기존 다른 7개 서비스도 실행 중이었다. 이 결과는 실제 영상 분석이나 새 릴리스 검증이 아니다.

서버의 `.env.example` 삭제 변경은 보존하며 `git pull`하지 않는다. 외부 네트워크 `conan-staging-ingress`와 모델 캐시 볼륨을 유지하고, 별도 override에 검증 이미지와 Vercel Origin만 지정하는 교체안을 제시했다. 실제 파일 생성·이미지 pull·컨테이너 교체는 승인 대기 중이다. 비밀값·기존 환경 파일·Tunnel은 변경하지 않았다.

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
| 자막 | [기획 본문](../design/ai-pipeline.md)은 MVP 자막 미사용이다. 2026-09-13 사용자는 팀장 기획을 따르며 기본 off와 선택 옵션 유지를 지시했다. | PR #3은 기본 off이며 manual·any 선택을 유지한다. 수동 CC도 발화 전문이나 정확성을 보증하지 않는다. | 기존 서버 환경값은 이번에 변경하지 않았다. 명시적 manual 설정이 있으면 승인된 배포에서 별도로 확인한다. |
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
| Vercel 고정 프론트 Origin | 조정준 팀장 | `https://kimjeonil.vercel.app` 확인, 서버 CORS 반영 전 | 2026-09-12 |
| 프론트 실 API 클라이언트 | 조정준 팀장 | 사용자 지정 담당. `Dynamic-Juo/fe` main `8c3bb9c`의 접수·폴링 미구현 확인, FE 코드·PR·배포는 수정하지 않음 | 연동 전 |
| 로그인 후 Swagger 열기와 schema 확인 | 나정균 팀원 | 루트 404만 확인, Swagger 미확인 | 실제 배포 후 |
| 접수·부분 응답·종료·404·429 처리 검수 | 조정준 팀장, 나정균 팀원 | API 계약 공유, 개발계 통합 검증 미완료 | 실제 배포 후 |
| 자막 옵션과 기존 #7 답변 | 나정균 팀원 | 기본 off·선택 옵션을 PR #3에 반영, #7 댓글은 사용자가 직접 정리 | 서버 배포 및 PR #7 후속 정리 시 |

API 키와 Access 서비스 토큰은 프론트 코드나 공개 문서에 넣지 않는다. 담당자 정보·일정을 확인하지 않은 항목은 추정해 확정하지 않는다.

프론트 공개 배포 번들에서도 실 API 미구현 오류 문구를 확인했다. CORS 추가만으로 연결 완료가 되지는 않는다. 팀장님에게 전달할 Vite 설정은 `VITE_API_BASE_URL=https://conan-api-dev.dotseven.cloud`, `VITE_USE_MOCK=false`다. 접수·폴링 구현과 환경변수 반영 후 Vercel 재배포는 팀장님이 진행한다. 최신 전달 항목은 [BE 작업 브랜치의 연동 안내](https://github.com/Dynamic-Juo/be/blob/fix/midpoint-hardening/docs/frontend-integration.md)를 참고한다. 이 링크는 배포된 코드 버전을 뜻하지 않는다.

## 다음 공유 순서

문서 변경은 `docs/midpoint-review` 브랜치로만 공유하고 새 docs PR을 만들지 않는다. 기존 PR #7 답글은 사용자가 다음 날 별도로 마무리하며 이번 변경에서는 게시하거나 수정하지 않는다.

백엔드 [PR #2](https://github.com/Dynamic-Juo/be/pull/2)는 main에 병합했다. 실제 개발계 배포는 아직 실행하지 않았다. 서버 조회·교체는 명령별 대상·영향을 알리고 승인받은 뒤 진행한다. 실제 배포 뒤 정확한 커밋과 이미지 기준을 기록하고, 인증된 `/health`·`/docs`·`/openapi.json`과 프론트의 접수·폴링 흐름을 검증한다. 키·환경값·기존 이미지·볼륨·Tunnel을 보존하고 기존 `conan-staging`의 `deepcheck-api`만 교체한다.
