# 모델 설계와 한계

현재는 사전학습 가능한 encoder 후보이며, 실제 connectome이나 pretrained 범용 TSFM이 아니다.
module/hub/reciprocal 합성 graph를 사용한다. 향후 실제 connectome 및 degree-preserving
rewiring 대조군이 필요하다. 채널·길이의 범용 처리는 이 프로젝트의 요구사항이지 모든
foundation model이 갖춰야 하는 절대적인 정의는 아니다.

| 계층 | 입출력 | 역할 |
|---|---|---|
| 공유 tokenizer | B,T,C → B,P,C,D | K개 sample을 평균내지 않고 모두 사용; 관측 mask 포함 |
| channel mixer | B,P,C,D → B,P,M,D | M개 learned query로 가변 채널을 고정 latent로 압축 |
| population graph | B,P,M,D → B,P,D | 고정 합성 배선 + type-pair weight + population τ |
| contextual head | B,P,C,D | 채널 token, 시간 embedding, visible channel context 결합 |
| 출력 | global / time / channel / patch_channel | 검색·분류·진단에 재사용 가능한 표현 |

센서 번호별 embedding이 없으므로 채널 순서를 바꾸면 global은 같고 channel 출력은 함께
재배열된다. 채널별 visible context로 특징을 구별하지만 명시적 센서 의미/단위 metadata는
아직 없다. 따라서 의미만 다른 동일 파형을 구분하지 못한다.

## 입력, 시간과 loss

- NaN/Inf는 결측이며 0 관측으로 취급하지 않는다. lengths로 padding을 별도 구분한다.
- K-sample time patch를 전 채널에서 가리고 최소 한 patch는 visible로 남긴다.
- 평균/표준편차는 visible 관측으로만 계산한다. 숨긴 정답은 통계에 들어가지 않는다.
- visible mean의 signed-log와 scale의 log를 추가해 크기 정보를 일부 남긴다.
- hidden AND observed 위치에서만 Huber reconstruction loss를 계산한다. label은 쓰지 않는다.
- dt는 record별 scalar. patch duration은 K×dt이고 마지막 partial patch는 짧아진다.
- 내부 결측 시간은 elapsed time에 포함하고 padded time은 상태 업데이트를 멈춘다.
- 불규칙 sampling은 import 전에 gap별 segment 분리 또는 명시적 resampling이 필요하다.
- 시간정보가 없는 UCR은 `time_unit=samples`, dt=1, time_known=false이다. 이 경우 τ를 초로
  해석하면 안 된다. 서로 다른 시간 관례의 혼합 성능은 아직 검증되지 않았다.
- 학습된 τ는 곧 물리적 고유 시간척도가 아니다. recurrence와 readout도 기억 길이에 영향을 준다.

전체 visible window 통계/channel summary를 사용하므로 **비인과적 offline encoder**이다.
online forecasting에 그대로 적용하면 미래가 섞일 수 있다. streaming에는 causal normalizer와
stateful API를 별도로 설계해야 한다. Patching은 계산 절약이며 1-point 이상 보존을 보장하지
않는다. K=1/4/8 등으로 정보 손실을 비교해야 한다.

## 계산과 학습

파라미터는 실제 초기화 후 run.json에 기록된다. smoke 약 18K, CPU 기본 약 69K.
작은 모델로 시작하되 범용 표현력이 충분하다는 주장은 하지 않는다. 실제 neuron 수/edge 수/
time step 수가 계산량을 좌우한다. dense/scatter를 동일 가중치·gradient로 테스트하며,
작은 graph에서 dense가 빠를 수 있으므로 기본은 dense다.

recurrent edge weight는 tanh 후 incoming degree로 나눠 행별 L1 norm ≤ 1로 제약한다.
positive τ, dt의 leaky update는 alpha∈[0,1]이다. 이는 안정화를 위한 공학적 제약이지
생물학적 E/I 비율이나 Dale's law 재현이 아니다. 연결 위치는 고정되고 type-pair별 가중치가
공유된다. 유효 τ 범위는 실험 설정으로 바꿀 수 있다.

FP32 CPU/CUDA 지원. AMP, multi-GPU, TBPTT는 **미구현**이다. 유한 window 내 full BPTT를
사용한다. 입력은 memory-mapped NPY, batch별 padding. 극단적으로 다른 채널 수가 섞이면
padding 비용이 커지며 추후 size bucketing이 필요하다.

train은 domain 균등, domain 내 dataset 균등 replacement sampling이다. epoch은 전체 data
1회가 아니라 optimizer-step 예산이다. validation은 전체 val의 domain 평균 loss를 다시
평균한다. smoke만 val batch 수를 제한한다. Test는 훈련에 사용하지 않는다.

epoch 경계 resume는 동일 CPU/환경에서 연속 실행과 정확히 같은 state_dict인지 테스트한다.
장치·버전 간 bitwise 재현성은 보장하지 않는다. best는 validation 기준으로만 선택한다.

## 후속 검증

frozen ridge probe를 제공하지만 multi-task 범용성 검증을 대체하지 않는다. 다음에는
random frozen baseline, 동일 예산 GRU/SSM/Transformer, shuffled graph, 전체 domain holdout,
forecasting/imputation/retrieval을 비교해야 한다. Contrastive augmentation은 spike/진폭
정보를 지울 수 있어 이번 MVP에서는 보류했다. τ·graph 효과는 독립 ablation이 필요하다.
