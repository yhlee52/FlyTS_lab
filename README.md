# FlyTS Lab — foundation encoder MVP

CPU / CUDA 공용, **다채널 시계열 자기지도 표현학습**을 위한 실행 가능한 연구 MVP.
이미 학습된 foundation model이나 검증된 범용 성능을 제공하는 릴리스는 아닙니다.
현재 topology는 **fly-inspired 합성 graph**이며 실제 FlyWire connectome이 아닙니다.

단계별 연구·구현 순서, 산출물과 검토 기준은
[FlyTS 단계별 개발 계획](docs/DEVELOPMENT_PLAN.md)에 정리되어 있습니다. 현재 첫 완결 목표는
공개 데이터 기반의 재현 가능한 **FlyTS-Mini v0.1**입니다.

Codex 작업은 [AI 연구팀 헌장](docs/research/TEAM_CHARTER.md)과
[공용 연구노트](docs/research/CURRENT_STATE.md)를 기준으로 진행합니다. 저장소 범위 custom agent와
research-stage/lab-notebook skill이 역할 분리, 단계 승인, 독립 QA와 토큰 예산을 적용합니다.

## 구현 범위

- `[B,T,C]` 가변 길이·가변 채널을 동일 가중치로 처리
- 공유 patch tokenizer → learned slot channel mixer → population graph → embedding
- population별 τ와 type-pair별 recurrent weight 공유, dense/scatter 동등 구현
- 결측·padding·학습 masking 구분, visible-only 정규화로 정답 누출 방지
- masked reconstruction 사전학습, CPU/CUDA 선택, gradient clipping
- 출처/해시/분할을 기록한 로컬 corpus, domain/dataset 균형 sampling
- best/last checkpoint, epoch 경계 resume, embedding export, frozen linear probe
- 다운로드와 학습 완전 분리: **pretrain은 네트워크를 사용하지 않음**

MVP는 recording 내부의 규칙적 sampling을 지원합니다. 모든 단위·채널 의미를 자동으로
이해한다는 뜻은 아닙니다. [설계와 한계](docs/ARCHITECTURE.md)를 참고하세요.

## 1. 설치·CPU smoke test

Python 3.10 이상. PyTorch는 실행 환경에 맞는 CPU/CUDA 배포판을 먼저 설치하세요.

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m flyts synthetic --output data/synthetic
python -m flyts pretrain --manifest data/synthetic/manifest.json --config configs/smoke.json --output outputs/smoke --device cpu
```

출력은 새 폴더를 지정합니다. 기존 실험은 덮어쓰지 않습니다. synthetic은 테스트용이며
실제 도메인 데이터나 반도체 물리 시뮬레이터가 아닙니다.

## 2. 일반망: 공개 데이터 준비·학습

[데이터 카드·이용 조건](docs/DATASETS.md)을 먼저 확인하세요. 공개 다운로드와 회사 사용
승인은 별개입니다. 처음에는 아래 3종으로 시작할 수 있습니다.

```bash
python -m flyts fetch --raw data/raw --datasets appliances bike beijing
python -m flyts prepare --raw data/raw --output data/public-v1 --datasets appliances bike beijing
python -m flyts verify --manifest data/public-v1/manifest.json
python -m flyts pretrain --manifest data/public-v1/manifest.json --config configs/cpu.json --output outputs/public-cpu --device cpu
```

HAR는 원본 README의 상업적 이용 금지와 현재 UCI 라이선스 표시가 충돌하므로 **기본 제외**입니다.
권리 확인·사용 허락 확보 후에만 추가하세요. 내부 승인 문자열만으로 외부 권리가 생기지 않습니다.
실제 허락을 기록한 경우 561개 요약 feature가 아니라 9개 waveform을 사용합니다.

```bash
python -m flyts fetch --raw data/raw --datasets appliances bike beijing har
python -m flyts prepare --raw data/raw --output data/public-four-domains --datasets appliances bike beijing har --approval-reference RIGHTS-CLEARANCE-REFERENCE
```

기본 3-domain corpus의 full pretraining:

```bash
python -m flyts pretrain --manifest data/public-v1/manifest.json --config configs/full_pretrain.json --output outputs/full-v1 --device auto
```

`full_pretrain.json`은 MVP 모델 전체 가중치를 처음부터 학습하는 **예산 preset**입니다.
50 epochs × 1,000 steps이며, 논문 규모의 corpus/성능을 보장하지 않습니다. CPU에서도
실행되지만 먼저 작은 preset으로 처리량을 측정하세요. `--device cuda`는 CUDA가 없으면
명시적으로 실패하고, `auto`는 CUDA가 없을 때 CPU를 선택합니다.

## 3. 폐쇄망: 동일한 학습 명령

일반망 준비 PC에서:

```bash
python -m flyts pack --manifest data/public-v1/manifest.json --output data/public-v1.zip
```

승인된 절차로 ZIP와 `.sha256`, Python/PyTorch wheelhouse, 소스/설정을 반입한 뒤:

```bash
python -m flyts unpack --archive data/public-v1.zip --output data/public-imported
python -m flyts pretrain --manifest data/public-imported/manifest.json --config configs/cpu.json --output outputs/offline --device auto
```

원본 ZIP과 `sources.lock.json`을 미리 반입했다면 `prepare`부터 시작해도 됩니다.
[오프라인 운영 절차](docs/OFFLINE.md)에 무네트워크 설치와 반입 검증을 정리했습니다.

## 4. 재시작·embedding·평가

```bash
python -m flyts pretrain --manifest data/public-v1/manifest.json --config configs/cpu.json --output outputs/public-cpu --device cpu --resume outputs/public-cpu/last.pt --epochs 20
python -m flyts embed --manifest data/public-v1/manifest.json --checkpoint outputs/public-cpu/best.pt --output outputs/public-embeddings.npz --device cpu
# 아래 probe는 권리가 확인된 HAR corpus를 별도로 준비한 경우에만 실행
python -m flyts probe --manifest data/public-four-domains/manifest.json --checkpoint outputs/full-v1/best.pt --dataset har --device auto
```

Resume는 동일한 corpus hash·설정이어야 하고 epochs/device만 바꿀 수 있습니다.
probe는 train label로 ridge 선형 분류기를 학습하고 val로 regularization을 선택합니다.
test는 마지막 평가에만 사용하고 사전학습에는 label을 사용하지 않습니다.

```python
import torch
from flyts.training import load_encoder

model, metadata = load_encoder("outputs/full-v1/best.pt", device="cpu")
x = torch.randn(2, 301, 23)  # 학습 때와 다른 길이/채널 수
with torch.no_grad():
    z = model.encode(x, dt=1.0)
# global: [2,D], time: [2,ceil(301/K),D], channel: [2,23,D]
```

## 5. 회사·반도체 데이터

`configs/local_data.example.json`에 recording별 파일·센서·dt·split·group을 지정합니다.
서로 다른 wafer/lot은 이어 붙이지 않습니다.

```bash
python -m flyts prepare-local --spec configs/local_data.example.json --output data/company-v1
python -m flyts merge --manifests data/public-v1/manifest.json data/company-v1/manifest.json --output data/mixed-v1
```

UCR Wafer는 승인 후 로컬 TSV importer를 사용할 수 있습니다. SECOM은 raw waveform이
아니므로 제외했습니다. PHM 2016 CMP는 후보이며 자동 다운로드/전용 converter는 아직 없습니다.
[데이터 전략](docs/DATASETS.md)을 참고하세요.

회사 데이터·회사 학습 checkpoint·민감한 metadata는 **public GitHub에 올리지 마세요**.
원래 PoC `FlyRNN`과 `examples/train_synthetic.py`는 비교·호환용으로 유지했습니다.
