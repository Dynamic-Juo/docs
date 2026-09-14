# 문서 PR과 리뷰 반영 이력

- 확인일: 2026-09-14
- 시간대: KST (UTC+09:00)
- 범위: docs PR #1 ~ #11의 커밋·일반 댓글·리뷰·inline 답변, 원격 main과 작업 브랜치

## PR 순서

번호가 아니라 실제 병합 시각으로 현재 기준을 판단한다. 열린 PR은 생성 시각과 head를 표시하며 병합된 기준으로 취급하지 않는다. 같은 시각의 commit은 부모 관계로 순서를 확인한다.

| 시각 | 사건 | 기준 commit | 제목 |
| --- | --- | --- | --- |
| 09-06 17:08 | [#1](https://github.com/Dynamic-Juo/docs/pull/1) 병합 | `8c11ce5` | docs(planning): 제품 요구사항과 AI 파이프라인 초안 정리 |
| 09-06 17:09 | [#2](https://github.com/Dynamic-Juo/docs/pull/2) 병합 | `e6ff906` | chore(repo): 문서 PR 템플릿과 작성 스킬 추가 |
| 09-07 06:29 | [#3](https://github.com/Dynamic-Juo/docs/pull/3) 병합 | `89007bb` | docs(planning): 프로젝트 계획 및 9월 5일 회의 결과 반영 |
| 09-08 07:32 | [#7](https://github.com/Dynamic-Juo/docs/pull/7) 생성·검토 중 | `e82a847` | docs(planning): 리뷰 합의와 최신 구현 점검 및 후속 작업 반영 |
| 09-11 06:50 | [#4](https://github.com/Dynamic-Juo/docs/pull/4) 병합 | `4e17a8b` | docs(evaluations): 딥페이크 판별 모델 비교와 파이프라인 검증 결과 기록 |
| 09-11 06:50 | [#5](https://github.com/Dynamic-Juo/docs/pull/5) 병합 | `81899c0` | docs(evaluations): 주장 사실성 검증 파이프라인 실측과 현재 방식 기록 |
| 09-11 06:51 | [#6](https://github.com/Dynamic-Juo/docs/pull/6) 병합 | `aedf161` | docs(planning): MVP 범위와 분석 결과 설계 확정 |
| 09-11 23:23 | [#8](https://github.com/Dynamic-Juo/docs/pull/8) 병합 | `8d07ff3` | chore(repo): 편집기 설정과 에이전트 Skill 경로 정리 |
| 09-14 00:39 | [#9](https://github.com/Dynamic-Juo/docs/pull/9) 병합 | `8ad452c` | docs(planning): 시안 작업에서 정한 UI 기준과 지원 범위 반영 |
| 09-14 00:40 | [#10](https://github.com/Dynamic-Juo/docs/pull/10) 병합 | `06f6962` | docs(evaluations): MVP 인수 점검표 추가 |
| 09-14 00:47 | [#11](https://github.com/Dynamic-Juo/docs/pull/11) 생성·검토 중 | `c9c06ef` | docs(planning): 영상 전체 AI 생성 탐지를 MVP 범위에서 제외 |

## #7에서 확인한 변경 순서

- 9월 8일 리뷰는 당시 평가 코드 cfe37fc를 대상으로 했다. 이후 LLM·네이버·자막·집계 변경이 있어 당시 미구현 목록을 최신 상태로 사용할 수 없다.
- 9월 10일 PR #6 답변에 LLM 추출·판정과 네이버 검색 도입이 기록됐다. 같은 날의 절사평균 실측은 be 작업 로그에 남아 있었고 docs에 연결되지 않았다.
- 9월 11일 #4·#5·#6 병합 후 #7 리뷰에서 미결 사항을 기존 프로젝트 계획으로 모으라는 요청이 있었다.
- 9월 13일 23:30의 e82a847은 별도 후속 표를 추가했다. 9월 14일 00:39 ~ 00:40에 #9·#10이 병합되면서 #7의 두 프로젝트 문서에 충돌이 발생했다.
- 9월 14일 팀장 리뷰는 중복 미결 표, 사용 조건 추적 누락, 현재 기준과 과거 이력 혼합, 실측 문서 위치와 병렬 구조 설명을 지적했다. 작성자 답변은 문서 통합·결과 연결을 약속했다.
- 이번 반영은 d740d5f에서 #9·#10 병합 충돌을 해소한 뒤 기존 미결 표를 직접 갱신했다. #11의 업로더 표기 변경은 별도 PR로 유지하며 병합을 대신하지 않았다.

원문: [문서 책임 요청](https://github.com/Dynamic-Juo/docs/pull/7#issuecomment-5637145547), [충돌·추적 리뷰](https://github.com/Dynamic-Juo/docs/pull/7#pullrequestreview-5193156618), [병렬 설명 약속](https://github.com/Dynamic-Juo/docs/pull/7#discussion_r4005847786), [측정 기록 약속](https://github.com/Dynamic-Juo/docs/pull/7#discussion_r4005848068).

## 이전 작업 브랜치의 처리

`docs/midpoint-review`에는 평가·공개 MVP 제안·백엔드 인수인계가 별도로 남아 있다. 미병합 기록이므로 이번 main 기준으로 합의됐다고 취급하지 않았다. 원문 근거·자가표기 분리·전사 부족·공개 요청 보호·자막 정책의 제안은 최신 댓글 및 be 감사와 대조했다. 해당 과거 브랜치의 “미승인”·“배포 대기”를 현재 사용자 승인·운영 상태로 덮어 적용하지 않는다.

이 문서는 이력 확인 기록이다. 남은 작업의 담당·상태·확인 시점은 [프로젝트 계획의 기존 미결 표](project-plan.md#미결-사항과-일정-확인) 한 곳에서 갱신한다.
