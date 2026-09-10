# 백엔드 구현 감사와 맥미니 배포 사전 점검

- 기록일: 2026-09-10
- 상태: `In Review`
- 구현 기준: [be main 472aff7](https://github.com/Dynamic-Juo/be/tree/472aff7201a834102d6ec2c27096dabb22a5ae4f)
- 요구사항 기준: [docs/mvp-review 35df85c](https://github.com/Dynamic-Juo/docs/tree/35df85c985cddee485db71fe6501edacbf98515d), [PR #6 최종 확인](https://github.com/Dynamic-Juo/docs/pull/6#issuecomment-5614626750)
- 후속 추적: [프로젝트 계획](../project/project-plan.md#미결-사항과-일정-확인)

## 목적과 판단 범위

문서를 먼저 읽고 현재 백엔드를 대조한 감사 결과를 기록한다. 이후 사용자가 맥미니와 기존 Cloudflare Zero Trust 인프라를 이용한 배포 의사를 밝혀 서버 상태와 배포 구성도 확인했다. 제품 요구사항 변경이나 배포 완료를 선언하는 문서는 아니다.

job polling, 점진적 결과, 미디어와 주장 결과 분리, 주장 최대 3건 병렬 처리, 분석 ID와 근거 스키마는 구현됐다. 다만 아래 결함 때문에 공개 운영과 MVP 정확성 검수는 완료로 판단할 수 없다. 제한된 내부 시험 배포는 환경 준비 후 진행할 수 있다는 것이 이번 점검의 판단이다.

docs/main은 점검 당시 `89007bb`로 검토 브랜치보다 오래됐다. PR #6과 [이전 구현 감사 PR #7](https://github.com/Dynamic-Juo/docs/pull/7)의 제안·리뷰 댓글을 병합된 제품 기준과 구분했다. 이 문서는 main에서 분기한 독립 기록이며 PR #6의 내용을 복사하거나 대신 확정하지 않는다.

## 우선 수정 항목

우선순위는 이번 감사의 제안이다. 담당자와 기한의 새 합의를 뜻하지 않는다. 코드 링크는 감사 당시 커밋에 고정했다.

| ID | 우선순위 | 확인한 사실과 영향 | 필요한 조치와 근거 |
| --- | --- | --- | --- |
| A-01 | 공개 전 | HTTP(S)와 netloc만 검사하고 임의 URL을 yt-dlp에 전달한다. YouTube·Shorts·공개 상태·내부 IP·redirect·크기 제한이 없으며 길이도 다운로드 후 검사한다. 인증서 검증도 비활성화돼 있다. 실제 내부 주소 공격은 실행하지 않았다. | 지원 URL과 다운로드 전 메타데이터 검증, 목적지·redirect 제한, 크기 제한, TLS 검증 복구. [API](https://github.com/Dynamic-Juo/be/blob/472aff7201a834102d6ec2c27096dabb22a5ae4f/backend/app.py#L141), [다운로더](https://github.com/Dynamic-Juo/be/blob/472aff7201a834102d6ec2c27096dabb22a5ae4f/deepcheck/downloader.py#L94) |
| A-02 | 공개 전 | 인증·소유권 검사 없이 전체 job 목록과 임의 job/session의 URL·결과·오류를 조회할 수 있다. | 전체 목록의 관리자 격리와 job 접근 정책. CORS를 인증으로 사용하지 않는다. [API](https://github.com/Dynamic-Juo/be/blob/472aff7201a834102d6ec2c27096dabb22a5ae4f/backend/app.py#L179) |
| A-03 | 판정 검수 전 | 원문 수집 없이 검색 제목과 snippet으로 검증한다. 1차 출처·독립 자료 2개·재전송 기사 중복·출처 충돌을 코드에서 강제하지 않는다. | 원문 수집 결과와 출처 독립성을 검증하고 불충분하면 유보한다. [판정 입력](https://github.com/Dynamic-Juo/be/blob/472aff7201a834102d6ec2c27096dabb22a5ae4f/deepcheck/claims.py#L936), [Accepted 근거 정책](https://github.com/Dynamic-Juo/docs/blob/35df85c985cddee485db71fe6501edacbf98515d/design/evidence-policy.md#L38) |
| A-04 | 해당 provider 활성화 전 | FactCheck rating이 있으면 주장 관련성 검사를 건너뛰고 첫 rating을 즉시 채택한다. 무관한 자료로 refuted가 되는 경우와 No evidence가 refuted로 매핑되는 경우를 재현했다. 운영 예시에서는 factcheck를 제외한다. | 동일 주장·시점·대상·충돌을 확인한 뒤 판정한다. [관련성](https://github.com/Dynamic-Juo/be/blob/472aff7201a834102d6ec2c27096dabb22a5ae4f/deepcheck/claims.py#L826), [직접 채택](https://github.com/Dynamic-Juo/be/blob/472aff7201a834102d6ec2c27096dabb22a5ae4f/deepcheck/claims.py#L1085) |
| A-05 | 판정 검수 전 | 얼굴 모델 실패 후 휴리스틱 점수로 대체해 뚜렷한 조작 징후 없음으로 표시될 수 있다. 얼굴이 없는 프레임 점수도 얼굴 crop 점수와 함께 집계한다. 여러 얼굴 중 가장 큰 하나만 사용한다. | 모델 실패는 unavailable로 표시하고 유효한 얼굴 분석만 집계한다. [대체·집계](https://github.com/Dynamic-Juo/be/blob/472aff7201a834102d6ec2c27096dabb22a5ae4f/deepcheck/deepfake.py#L223), [결과](https://github.com/Dynamic-Juo/be/blob/472aff7201a834102d6ec2c27096dabb22a5ae4f/deepcheck/report.py#L193) |
| A-06 | 범위 확정 필요 | 영상 전체 AI 생성 모델이 없다. 제목·설명 자가표기를 사용하고 그 외에는 unavailable이다. 이 축의 unavailable은 전체 제한 상태에 반영하지 않는다. 같은 키워드가 얼굴 조작에도 영향을 준다. | 모델 구현 또는 1차 출시 범위 조정과 UI·문서 반영. 일반적인 딥페이크 경고·패러디 언급을 확정 자가표기로 취급하지 않는다. [전체 생성](https://github.com/Dynamic-Juo/be/blob/472aff7201a834102d6ec2c27096dabb22a5ae4f/deepcheck/report.py#L271) |
| A-07 | 공개 전 | bounded queue를 dispatcher가 무제한 executor 내부 큐로 옮겨 접수 상한을 우회한다. backlog=1, worker=1 상태에서 8건이 접수됐고 executor에 6건이 대기하는 재현을 확인했다. | 실행 중+대기 전체에 입장 제한을 적용하고 실제 포화로 429와 ready를 시험한다. [dispatcher](https://github.com/Dynamic-Juo/be/blob/472aff7201a834102d6ec2c27096dabb22a5ae4f/backend/harness.py#L182) |
| A-08 | 공개 전 | 600초 제한은 실행 중 다운로드·STT·모델을 중단하지 않는다. 전체 반환 후 timed_out이 될 수 있다. evidence_budget_sec도 API의 verify_one_claim 직접 호출 경로에서는 강제되지 않는다. | 단계별 남은 시간 전달과 중단·취소 정책을 구현한다. [사후 상태](https://github.com/Dynamic-Juo/be/blob/472aff7201a834102d6ec2c27096dabb22a5ae4f/backend/harness.py#L218), [주장 시작 검사](https://github.com/Dynamic-Juo/be/blob/472aff7201a834102d6ec2c27096dabb22a5ae4f/deepcheck/pipeline.py#L488) |
| A-09 | 연동 전 | 개별 claim failed가 있어도 claim stage는 OK이고 최종 completed가 될 수 있다. 제공자 TimeoutError도 done/no_source로 처리되는 것을 재현했다. | 검색 실패와 정상 0건을 구분하고 부분 실패를 completed_with_limitations에 반영한다. [단계 종료](https://github.com/Dynamic-Juo/be/blob/472aff7201a834102d6ec2c27096dabb22a5ae4f/deepcheck/pipeline.py#L500), [검색 실패](https://github.com/Dynamic-Juo/be/blob/472aff7201a834102d6ec2c27096dabb22a5ae4f/deepcheck/claims.py#L1068) |
| A-10 | 연동 전 | URL 중복 제거가 옵션을 무시하며 세션 활성 검사보다 먼저 실행된다. 다른 옵션이 무시되거나 한 세션이 활성 job 2개에 참여할 수 있음을 재현했다. | 옵션을 포함한 중복 키와 재사용 전 세션 제한 검사. [접수](https://github.com/Dynamic-Juo/be/blob/472aff7201a834102d6ec2c27096dabb22a5ae4f/backend/harness.py#L143) |
| A-11 | 주장 검수 전 | 규칙 추출은 비수치 사실 주장을 누락한다. 토큰 중복 제거는 늘렸다/늘리지 않았다, 모든/일부처럼 의미가 다른 주장도 병합한다. 반복 위치·횟수와 우선순위를 충분히 보존하지 않는다. LLM 운영 설정에서도 추출 실패 시 규칙 fallback의 제한을 알려야 한다. | 의미·부정·범위가 같은 주장만 병합하고 모든 언급 위치와 우선순위를 검증한다. [추출·중복 제거](https://github.com/Dynamic-Juo/be/blob/472aff7201a834102d6ec2c27096dabb22a5ae4f/deepcheck/claims.py#L530), [위치](https://github.com/Dynamic-Juo/be/blob/472aff7201a834102d6ec2c27096dabb22a5ae4f/deepcheck/claims.py#L751) |

## 문서와 운영 후속 항목

- 자막 기본값은 구현에서 manual이지만 검토 문서 T-02는 STT 우선이다. PR #7의 자막 허용 의견과 전체 생성 제외 제안은 기준 변경 여부를 확인해 반영해야 한다.
- 실제 파이프라인은 미디어 분석 후 STT·주장 검증으로 진행한다. 주장 우선·독립 진행 요구와 차이가 있으며 최초 주장 1분 목표는 실측이 필요하다.
- README의 workers=3, max_claims=5와 health 응답 설명은 현재 설정·API와 다르다. 현재 설정은 workers=1, max_claims=0이다.
- 종료 시 executor 취소·대기가 없고 job은 메모리 저장이라 재시작 시 사라진다. FE의 404 복구와 종료 처리를 확인해야 한다.
- API 응답을 명시적인 모델로 고정하고 timezone 포함 시각, worker까지 이어지는 request ID, CORS 노출 헤더를 점검해야 한다.
- 의존성 고정, 모델·오픈소스 라이선스 확인, CI와 실제 영상 인수 검수가 남아 있다. 캐시는 선택 요구이므로 미구현만으로 필수 기능 누락으로 판정하지 않았다.

## 검증 범위와 한계

감사 당시 be 472aff7에서 임시 Python 환경으로 pytest를 실행해 167건이 통과했고 deprecation 경고 2건이 나왔다. 외부 제공자·모델을 모의 처리하는 단위 테스트 결과다. queue, 세션·옵션 중복 제거, provider 실패, 모델 실패, 판정 분기는 별도 인프로세스 재현으로 확인했다. 실제 외부 공격이나 운영 부하 시험은 실행하지 않았다.

기존 프롬프트 평가 11건과 미디어 집계 실험 영상 2편은 실제 Shorts 전체 정확도를 입증하지 않는다. M-08에 필요한 고정 영상, 기대 주장·미디어 결과·원문 출처, 완결성 결과가 없다. 이번 문서화 단계에서 테스트를 다시 실행한 것으로 기록하지 않는다.

## 맥미니 배포 판단

2026-09-10 실제 서버에서 ARM64, 물리 메모리 16GiB, OrbStack Docker 29.4.0, Compose 5.1.2를 확인했다. 기존 서비스 7개와 token 기반 cloudflared가 실행 중이다. Docker VM은 CPU 10개, 메모리 약 7.8GiB를 보고했으며 한 차례 stats의 기존 컨테이너 메모리 합계는 약 288MiB였다. 이 값은 OS·VM 전체 사용량이나 피크 부하가 아니다.

Conan Compose는 ARM64, 호스트 포트 없음, 별도 conan-ingress 네트워크, CPU 2개·메모리 3GiB로 정적 검증을 통과했다. 기존 Tunnel을 해당 네트워크에도 연결하는 구성은 가능하다. 네트워크 분리는 Conan이 기존 애플리케이션 네트워크에 직접 참여하는 것을 줄이지만 임의 URL의 내부 주소 접근을 차단하는 보안 장치는 아니다.

현재 서버에는 Conan 이미지·컨테이너·전용 네트워크와 실제 .env.home이 없다. API 도메인, Vercel Origin, Conan용 Access 정책은 미확인이다. 따라서 환경을 준비한 뒤 제한된 접근으로 기동·분석을 검증할 수 있으나, 지금 공개 서비스 배포가 검증됐다고 말할 수는 없다. Tunnel 연결만으로 Access 인증이 적용됐다고 가정하지 않는다.

실제 컨테이너명·네트워크·환경 준비·검증 명령·복구 조건은 [BE 배포 점검 기록](https://github.com/Dynamic-Juo/be/blob/docs/mac-mini-readiness/docs/deployment-log.md)에 관리한다. 해당 기록은 함께 공유하는 문서 브랜치이며 main 병합 여부는 별도다.

## 남은 결정과 완료 조건

| 항목 | 완료 조건 | 담당자 | 확인 시점 |
| --- | --- | --- | --- |
| 출시 범위 | 전체 생성·자막·한국어 지원 정책을 현재 기준에 반영한다. | 미정 | 출시 범위 확정 전 |
| 접근 정책 | API 도메인·Access 대상·FE Origin과 브라우저 인증 방식을 확정한다. | 미정 | Tunnel 라우트 추가 전 |
| 서버 준비 | 비밀값을 안전하게 설정하고 커밋 태그 이미지·전용 네트워크를 준비한다. | 미정 | 내부 기동 전 |
| 배포 검증 | 모델 초기화, 실제 Shorts, 최초/재실행 시간, 메모리, 기존 서비스 상태와 복구를 기록한다. | 미정 | 배포 완료 판정 전 |
| 공개 전 보완 | A-01·A-02·A-07·A-08과 판정·상태 오류를 수정하고 실제 인수 검수를 통과한다. | 미정 | 일반 사용자 공개 전 |

## 외부 운영 자료

- [Docker Compose 네트워크](https://docs.docker.com/compose/how-tos/networking/): external 네트워크 공유 방식. 문서 참조이며 코드를 가져오지 않았다. 소프트웨어 라이선스는 [Docker Compose Apache-2.0](https://github.com/docker/compose/blob/main/LICENSE)이다.
- [Cloudflare Access CORS](https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/authorization-cookie/cors/): 브라우저 preflight와 Access 인증 설정. 서비스 문서 참조이며 콘텐츠를 재배포하지 않는다. cloudflared 라이선스는 [Apache-2.0](https://github.com/cloudflare/cloudflared/blob/master/LICENSE)이다.
