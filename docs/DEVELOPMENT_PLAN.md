# FlyTS 단계별 개발 계획

문서 기준일: 2026-09-24

이 문서는 FlyTS의 현재 구현에서 출발하여 **FlyTS-Mini v0.1**을 완성하기 위한
작업 순서, 단계별 산출물, 검토 체크포인트와 저장 위치를 정의한다.

FlyTS의 장기 목표는 서로 다른 도메인, 채널 수, 채널 순서와 의미를 가진 다변량
시계열을 하나의 공통 backbone으로 처리하는 범용 representation model을 만들고,
공개 데이터에서 검증한 뒤 회사 폐쇄망의 반도체 생산 설비 데이터로 전이하는 것이다.

이번 개발 주기의 목표는 거대한 foundation model을 한 번에 만드는 것이 아니다.

> 공개 데이터만으로 FlyTS-Mini를 학습하고, 가변 채널·채널 순서 변경·채널 누락에
> 대응하면서 fly-inspired topology가 동일 조건의 비교군보다 가치가 있는지를
> 재현 가능한 실험으로 판단할 수 있는 상태를 만든다.

## 1. 작업 원칙

1. 한 단계에서는 하나의 주된 가설 또는 기반 기능만 다룬다.
2. 각 단계는 원칙적으로 별도 브랜치와 Draft PR로 진행한다.
3. 이전 단계의 체크포인트를 확인한 뒤 다음 단계로 넘어간다.
4. 코드 변경과 장시간 실제 학습 실험을 분리한다.
5. 코드, 설정, 작은 결과표와 문서는 Git에 기록한다.
6. 원본 데이터, 대용량 checkpoint와 실행 산출물은 Git에 커밋하지 않는다.
7. 비교 실험에서는 front-end, 데이터, optimizer, 학습 step과 parameter budget을
   최대한 고정하여 topology 이외의 효과가 섞이지 않게 한다.
8. 예상과 다른 결과도 숨기지 않고 실패 조건과 원인을 기록한다.
9. CPU와 CUDA를 모두 지원하되, 검증하지 않은 장치 성능을 주장하지 않는다.
10. 공개망의 다운로드 단계와 폐쇄망에서도 가능한 prepare/train 단계를 분리한다.

## 2. 산출물 저장 규칙

| 종류 | 기본 위치 | Git 커밋 |
|---|---|---|
| 설계·운영 문서 | `docs/` | 예 |
| 재사용 가능한 실험 설정 | `configs/`, `experiments/` | 예 |
| 테스트 | `tests/` | 예 |
| 작은 요약 결과와 표 | `reports/` | 예 |
| 원본·전처리 데이터 | `data/` | 아니요 |
| 학습 로그·checkpoint | `outputs/<experiment-id>/` | 아니요 |
| 최종 오프라인 전달 bundle | `artifacts/` 또는 Release asset | 아니요 |

모든 장시간 실험은 최소한 다음 정보를 남긴다.

- Git commit SHA
- training config
- dataset manifest SHA-256
- seed
- Python/PyTorch와 장치 정보
- parameter 수
- 주요 metric과 실행 시간
- best/last checkpoint

## 3. 전체 단계와 의사결정 지점

| 단계 | 목표 | 주요 산출물 | 다음 단계 진입 조건 |
|---:|---|---|---|
| 0 | 현재 `main` 재현 | 기준 검증 기록 | 테스트와 smoke path 통과 |
| 1 | 연구·실험 규약 고정 | 컨센서스와 실험 프로토콜 | 성공·실패 기준 합의 |
| 2 | channel masking/dropout | masking 모듈과 테스트 | 누출 없이 채널 누락 학습 가능 |
| 3 | Foundation 특성 평가 | robustness 평가 CLI | 요구사항을 수치로 측정 가능 |
| 4 | topology 모듈화 | 공통 graph interface | topology만 교체 가능 |
| 5 | topology 비교군 | fly-like/rewired/random | 공정 비교 조건 충족 |
| 6 | 공개 corpus v1 확장 | 저·고채널 corpus | 실제 채널 수 차이 포함 |
| 7 | conventional baseline | GRU/dense 비교군 | 동일 예산 비교 가능 |
| 8 | FlyTS-Mini pilot | 작은 예산 end-to-end 결과 | 정식 실험 위험 제거 |
| 9 | 정식 비교 실험 | 반복 실험과 통계 보고서 | 연구 질문에 답할 근거 확보 |
| 10 | FlyTS-Mini v0.1 확정 | 재현 가능한 release bundle | 1차 개발 주기 완료 |

---

## 4. 단계별 작업 계획

### 단계 0 — 현재 기준점 재현

현재 `main`에 병합된 구현을 기능 추가 없이 다시 실행하여 이후 비교의 기준점을 만든다.

작업:

- Python 환경과 프로젝트 설치
- 전체 `pytest` 실행
- synthetic corpus 생성
- CPU smoke pretraining
- checkpoint 저장과 epoch 경계 resume 확인
- embedding export와 frozen probe 경로 확인
- 가능한 환경에서는 CUDA 최소 backward/checkpoint 테스트
- parameter 수, 실행 시간과 peak memory 기록

산출물:

- `docs/BASELINE_VALIDATION.md`
- 로컬 `outputs/phase0-baseline/`
- GitHub Actions 결과

체크포인트:

- 단위·통합 테스트가 통과한다.
- 동일 seed와 설정으로 재현할 수 있다.
- resume와 embedding export가 정상 동작한다.
- 실패 항목은 기능 개발 전에 원인과 처리 방향을 기록한다.

### 단계 1 — 연구·실험 규약 고정

모델을 더 바꾸기 전에 연구 질문, 비교 조건과 성공 기준을 저장소의 공식 문서로 고정한다.

산출물:

- `docs/PROJECT_CONSENSUS.md`
- 이 문서 `docs/DEVELOPMENT_PLAN.md`
- `docs/EXPERIMENT_PROTOCOL.md`
- `docs/research/stages/stage-01/CHARTER.md`
- `docs/research/stages/stage-01/QA_REPORT.md`
- `docs/research/stages/stage-01/RESULT.md`

`EXPERIMENT_PROTOCOL.md`에는 다음을 포함한다.

- dataset split과 held-out domain 규칙
- seed와 반복 횟수
- parameter와 compute budget 매칭 규칙
- model selection에 사용할 validation metric
- test set 최종 사용 원칙
- foundation 특성별 평가 metric
- 단계별 중단·재검토 조건

Stage 1의 승인된 세부 결정은 `docs/research/DECISION_LOG.md`의 DEC-007을 기준으로 하며,
운영 규약은 `docs/EXPERIMENT_PROTOCOL.md`를 따른다. Stage 01의 원래 계획은 final test를
보지 않은 Stage 3 개발 evidence로 수치 pass/fail threshold를 calibration·동결하는 것이었다.
DEC-014에 따라 Stage 03은 candidate evidence만 수용하고 수치 guard·threshold·uncertainty 동결을 연기한다.
별도 승인된 calibration 재개와 동결 전에는 후속 비교의 pass/fail 또는 최종 주장을 하지 않는다.

주요 평가 항목:

- masked reconstruction
- channel permutation distance
- channel dropout robustness
- unseen channel-count generalization
- frozen linear probe
- held-out domain transfer
- parameter 수, 학습 시간, memory, inference latency

체크포인트:

- Fly topology 효과와 router/encoder 효과를 분리할 수 있다.
- validation과 test의 역할이 명확하다.
- 결과가 좋지 않을 때도 판단 가능한 기준이 있다.

### 단계 2 — channel masking과 channel dropout

진행 상태 (2026-09-25): Stage 02 implementation and independent QA `PASS` were accepted with user `GO`; PR #8 was merged at `461f1fc`. Stage 03은 independent final QA `PASS` 후 수치 미동결 범위에서 종료됐다.

현재 temporal patch masking에 채널 축 자기지도 학습과 robustness 학습을 추가한다.

구현 범위:

- temporal patch masking
- channel 전체 masking
- temporal + channel 혼합 masking
- 입력 channel dropout
- 최소 한 채널과 한 시간 구간을 visible로 유지
- 실제 결측, padding과 학습 corruption mask를 계속 분리
- hidden target이 normalization 통계에 들어가지 않도록 보장

예상 설정 형태:

```json
{
  "masking": {
    "temporal_ratio": 0.4,
    "channel_ratio": 0.2,
    "channel_dropout_ratio": 0.1
  }
}
```

산출물:

- 독립 masking 모듈
- config validation
- 누출 방지 및 극단 조건 테스트
- `docs/MASKING.md`

체크포인트:

- 단일 채널 입력도 처리한다.
- 입력 채널의 50%를 제거해도 forward가 가능하다.
- 숨긴 값 변경이 visible input representation에 누출되지 않는다.
- 기존 temporal-only 설정도 재현한다.

### 단계 3 — Foundation 특성 평가기

FlyTS의 핵심 요구사항을 모델별로 동일하게 측정하는 평가 도구를 만든다.

평가 항목:

1. channel permutation invariance
2. 10/30/50% channel dropout
3. 학습 범위 밖 channel count
4. time/channel padding 일관성
5. missing-value robustness

channel permutation은 다음과 같은 representation distance로 기록한다.

```text
D_perm = 1 - cosine(Z(X), Z(PermuteChannels(X)))
```

산출물:

- `flyts evaluate-robustness` CLI
- `reports/robustness/*.json`
- 사람에게 읽기 쉬운 Markdown/CSV 요약
- 수치 미동결 candidate 결과와 descriptive Markdown/CSV/JSON; threshold 기반 pass/fail은 별도 승인된 calibration 재개·동결 이후

체크포인트:

- channel permutation distance가 기대한 수치 오차 범위인가?
- dropout 비율에 따른 degradation을 일관되게 측정하는가?
- 동일한 evaluator를 모든 backbone에 적용할 수 있는가?
- final held-out/test를 보지 않고 후보 evidence를 만들었는가? 수치 threshold·guard·uncertainty는 DEC-014에 따라 미동결이며, pass/fail 사용은 별도 승인된 calibration 재개·동결까지 보류한다.

### 단계 4 — topology 모듈화

현재 합성 topology 생성 로직을 모델에서 분리한다. 이 단계에서는 의도적인 성능 변경을
하지 않는다.

예상 구조:

```text
src/flyts/topology/
├── base.py
├── fly_like.py
├── random_sparse.py
├── rewired.py
└── validation.py
```

공통 graph artifact에는 최소한 다음을 포함한다.

- source/destination edge
- node type 또는 population
- module ID
- edge type
- topology seed와 생성 metadata

산출물:

- topology builder interface
- graph 통계 추출기
- 현재 fly-like graph의 backward-compatible 구현
- 리팩터링 전후 동등성 테스트

체크포인트:

- 동일 seed에서 기존 graph를 재현한다.
- 기존 checkpoint 호환 여부를 명시한다.
- config만으로 topology를 교체할 수 있다.

### 단계 5 — topology 비교군

Fly topology 가설을 시험하기 위한 최소 비교군을 구현한다.

초기 비교군:

- `fly_like`
- `degree_preserving_rewired`
- `random_sparse`

가능한 한 다음을 일치시킨다.

- node와 edge 수
- in/out degree distribution
- population 수
- 학습 parameter 수
- temporal encoder와 router
- optimizer와 학습 step

산출물:

- 세 topology generator
- sparsity, degree, reciprocity, modularity 통계
- 고정 seed graph artifact와 검증 테스트
- topology 비교 문서

체크포인트:

- fly-like와 rewired가 degree 조건을 만족하는가?
- random graph가 계산 구현 때문에 불필요하게 불리하지 않은가?
- topology 이외 조건이 동일한가?

### 단계 6 — 공개 corpus v1 확장

현재 starter corpus를 실제 저채널·고채널 조건을 포함하도록 확장한다. dataset은 원본
schema와 이용 조건을 확인한 뒤 하나씩 추가한다.

우선 후보:

- ETT: 저채널 시계열
- Electricity: 약 321채널
- Traffic: 약 862채널
- 현재 Appliances/Bike/Beijing 유지

후보라는 이유만으로 자동 포함하지 않는다. 명확한 출처, 라이선스와 올바른 시간축을
확인하지 못하면 제외하거나 보류한다.

산출물:

- dataset별 downloader/converter
- source URL, notice와 checksum
- channel 수, 결측률과 sampling interval 통계
- split/gap 검증 테스트
- `docs/DATASETS.md` 업데이트
- 로컬 `data/public-v1/manifest.json`

체크포인트:

- 동일 checkpoint가 저채널과 고채널 데이터를 처리한다.
- 시간 분할 후 window를 생성한다.
- train/val/test source range가 겹치지 않는다.
- 이용 조건이 불명확한 데이터가 기본 corpus에 들어가지 않는다.
- 성능 결과를 보기 전에 development와 final held-out domain 역할을 registry에 동결한다.

### 단계 7 — conventional baseline

topology 비교 외에 일반적인 recurrent backbone을 같은 front-end에서 비교한다.

첫 범위:

- shared encoder + Set Router + Fly sparse recurrent backbone
- shared encoder + Set Router + dense recurrent backbone
- shared encoder + Set Router + GRU

Transformer/SSM 계열은 이 비교 체계가 안정된 뒤 후속 단계로 추가한다.

산출물:

- 공통 backbone interface
- parameter budget matching 도구
- baseline config
- 계산량과 parameter 비교표

체크포인트:

- 모든 모델이 같은 tokenizer/router와 입력을 사용한다.
- parameter 수와 학습 예산이 합의한 허용 범위 안이다.
- 특정 baseline에만 불리한 입력 처리나 구현 병목이 없다.

### 단계 8 — FlyTS-Mini pilot

정식 실험 전에 작은 예산으로 전체 파이프라인을 관통한다.

예상 범위:

- seed 1개
- 작은 model
- 각 topology/backbone 1회
- 제한된 training step
- 2~3개 dataset
- CPU 또는 사용 가능한 단일 GPU

로컬 산출물 예:

```text
outputs/pilot/
├── fly-like/
├── rewired/
├── random/
├── gru/
└── summary.json
```

커밋 산출물:

- `reports/PILOT_RESULTS.md`
- 실험 config
- 실패 사례와 정식 실험 시간·메모리 추정

체크포인트:

- 모든 비교군이 동일한 경로로 끝까지 실행된다.
- metric과 provenance가 자동 수집된다.
- NaN, OOM, 잘못된 split 또는 명백한 성능 불균형 원인이 없다.
- 정식 실험 전 수정할 문제와 유지할 설정이 정리된다.

### 단계 9 — 정식 비교 실험

핵심 연구 질문에 답할 수 있는 반복 실험을 수행한다.

최소 실험 구성:

- 사전 등록한 paired seed 5개
- fly-like / rewired / random / GRU
- 동일 parameter 및 optimizer-step budget
- multi-domain self-supervised pretraining
- held-out domain 평가
- channel permutation/dropout/count 평가
- frozen linear probe
- 계산 효율 측정
- 동결된 protocol 아래 final held-out/test 1회 공개

산출물:

- 실험별 `run.json`, `history.json`, `best.pt`
- raw metric CSV/JSON
- 평균·표준편차 결과표와 그래프
- `reports/FOUNDATION_STUDY_V1.md`

핵심 판단 질문:

- fly-like가 rewired/random보다 여러 seed에서 반복적으로 우세한가?
- 차이가 seed 변동보다 큰가?
- GRU 대비 성능 또는 효율 장점이 있는가?
- channel dropout과 held-out domain에서 유의미한 장점이 있는가?

### 단계 10 — 1차 최종 산출물: FlyTS-Mini v0.1

단계 9 결과를 바탕으로 1차 개발 주기를 확정한다.

최종 산출물:

```text
FlyTS-Mini v0.1
├── model source
├── selected public checkpoint
├── exact training config
├── dataset manifest와 source hashes
├── model card
├── evaluation report
├── raw metric tables
├── offline training/transfer instructions
└── limitations와 next-decision document
```

저장 위치:

- 코드·설정·문서: GitHub `main`
- source version: Git tag `flyts-mini-v0.1`
- 대용량 checkpoint: GitHub Release 또는 승인된 artifact storage
- 로컬 실험 결과: `outputs/flyts-mini-v0.1/`
- 최종 보고서: `reports/FLYTS_MINI_V0_1.md`
- 오프라인 전달물: `artifacts/flyts-mini-v0.1-offline.zip`

최종 체크포인트는 다음 중 어떤 결론인지 근거와 함께 결정하는 것이다.

1. Fly topology가 유의미하므로 모델과 corpus 규모를 확대한다.
2. channel-agnostic front-end는 유효하지만 Fly topology 우위는 확인되지 않았다.
3. 데이터나 평가가 부족하여 제한된 추가 검증이 필요하다.
4. 가설이 지지되지 않아 backbone 방향을 수정한다.

부정적인 결과라도 재현 가능하고 원인을 구분할 수 있다면 유효한 연구 산출물로 본다.

## 5. FlyTS-Mini 이후의 장기 단계

FlyTS-Mini v0.1에서 가능성을 확인한 뒤에만 다음을 진행한다.

1. 실제 Fly connectome과 구조 통계 분석
2. connectome 통계 기반 compressed topology
3. 더 큰 multi-domain public corpus
4. forecasting/anomaly adapter
5. 공개 데이터 continued pretraining
6. checkpoint와 환경의 폐쇄망 반입 검증
7. unlabeled semiconductor data continued pretraining
8. semiconductor anomaly/forecast adapter

장기 최종 산출물은 반도체 생산 설비 데이터에 적응한 FlyTS이지만, 현재의 첫 완결
목표는 단계 10의 **FlyTS-Mini v0.1**이다.

## 6. 현재 진행 위치

- [x] 초기 FlyRNN PoC
- [x] variable-channel foundation encoder MVP
- [x] 공개 starter corpus와 offline-first pipeline
- [x] 단계 0 — 현재 기준점 재현
- [x] 단계 1 — 연구·실험 규약 고정
- [x] 단계 2 — channel masking과 channel dropout
- [x] 단계 3 — evaluator와 development-only candidate evidence 수용; final QA `PASS`로 수치 미동결 종료
- [ ] 단계 4 이후 — Stage 03 사용자 gate 이후 순서에 따라 진행

단계 1의 연구 규약과 단계 2의 channel masking/dropout은 각각 사용자 `GO`로 완료되었다.
단계 3 evaluator와 candidate evidence는 사용자 `GO`로 수용되었고, independent final QA `PASS` 후 수치 threshold·guard·uncertainty를 동결하지 않은 범위에서 종료됐다. Draft PR 작성은 승인됐으나 병합은 별도 결정이다. 지표는 기술적·서술적 결과만 제공하고 robustness pass/fail 또는 최종 주장을 하지 않는다. Stage 04 진입은 별도 승인 대상이다.
