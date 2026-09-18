# FlyTS Lab

FlyTS Lab은 다변량 시계열에 사용할 **초파리 신경회로 착안(fly-inspired)**
희소 재귀 신경망을 작은 코드부터 검증하는 연구용 저장소입니다.

첫 버전의 목표는 한 가지입니다.

> 고정된 희소·모듈형 연결과 학습 가능한 여러 시간상수(`tau`)를 가진 RNN이
> `[batch, time, sensor]` 시계열을 정상적으로 학습하는지 확인한다.

현재 구현은 실제 FlyWire connectome을 사용하지 않습니다. `module`, `reciprocal
edge`, `hub`를 포함하는 합성 topology이며, 실제 connectome 적용 전의 기준 PoC입니다.

## 모델

각 hidden neuron은 population에 속하고, 같은 population은 하나의 시간상수를
공유합니다.

```text
alpha_i = 1 - exp(-dt / tau_i)
h_i(t+1) = h_i(t) + alpha_i * (candidate_i(t) - h_i(t))
```

- `dt`: 입력 샘플 간 실제 시간. 권장 단위는 초입니다.
- `tau_i`: population별로 학습되며 `tau_min`과 `tau_max` 사이에 제한됩니다.
- recurrent topology: 학습 중 연결의 유무는 고정되고, 존재하는 edge의 weight만
  학습됩니다.

## 설치 및 실행

Python 3.10 이상을 권장합니다.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
pytest
python examples/train_synthetic.py --epochs 8 --dt 1.0
```

0.1초 sampling 데이터라면 `--dt 0.1`로 실행합니다.

## 실제 데이터 연결

입력 텐서를 `[batch, time, sensor]`로 준비하면 됩니다.

```python
import torch
from flyts import FlyRNN, FlyRNNConfig

model = FlyRNN(
    FlyRNNConfig(
        input_size=120,
        hidden_size=64,
        output_size=2,
        num_populations=8,
        tau_min=0.5,
        tau_max=300.0,
    )
)

x = torch.randn(32, 300, 120)
logits, embedding = model(x, dt=1.0)
```

센서별 scaling, 결측값 처리, padding/mask, 실제 anomaly label 규약은 데이터가
정해진 뒤 별도 계층으로 추가할 예정입니다.

## 현재 범위와 다음 비교

이 합성 데이터는 학습 파이프라인 점검용일 뿐 성능 benchmark가 아닙니다. 다음
단계에서는 동일한 데이터 분할과 parameter budget으로 아래 모델을 비교합니다.

1. Dense RNN
2. Random sparse RNN
3. Fly-inspired RNN (현재 모델)
4. 실제 FlyWire topology를 사용한 RNN
