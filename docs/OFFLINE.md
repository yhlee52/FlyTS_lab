# 일반망·폐쇄망 공용 운영 절차

## 원칙

네트워크 작업은 `flyts fetch`로만 실행한다. prepare, verify, pack/unpack, pretrain, resume,
embed, probe는 로컬 전용이다. Hugging Face 자동 다운로드, 원격 tokenizer, 원격 logging,
telemetry, 외부 tracking service가 없다. 최초 가중치는 로컬에서 무작위 초기화한다.

일반망도 download → prepare → verify → pretrain 순서이며, 폐쇄망은 같은 명령에서
download만 생략한다. 원 archive+lock 또는 prepared bundle 중 하나를 승인 절차로 반입한다.
원본 dataset의 readme/notice, 출처, checksum, preprocessing version을 함께 보존한다.

## 환경 패키징: 데이터만 가져오면 충분하지 않다

준비 PC/VM은 **목표 OS, CPU 아키텍처, Python major/minor**와 같게 맞춘다.
Linux wheel을 Windows에 설치할 수 없다. CUDA wheel과 호환 NVIDIA driver도 확인한다.
CPU용/CUDA용 wheelhouse를 분리하고 driver/OS 패키지는 회사 절차로 별도 반입한다.
PyTorch 배포판 선택은 [공식 설치 안내](https://pytorch.org/get-started/locally/)를 따른다.

일반망의 목표 환경과 일치하는 Python 가상환경에서:

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m pip wheel . --no-deps --wheel-dir wheelhouse
python -m pip download --only-binary=:all: --dest wheelhouse numpy torch pytest
```

마지막 명령은 예시이며 기본 PyPI torch가 큰 CUDA 의존성을 포함할 수 있다. 승인 환경에서는
**검증한 정확한 버전과 CPU/CUDA index URL로 고정**한다. CPU라면 공식 CPU wheel index에서
torch를 먼저 지정하고 numpy/pytest 등은 별도로 준비한다. 사용한 명령과 version list를
반입 기록에 남긴다. 위 명령은 target과 다른 OS에서 cross-download를 대신해 주지 않는다.

가장 중요한 검증은 새 가상환경에서 실제 오프라인 설치가 되는지 확인하는 것이다:

```bash
python -m pip install --no-index --find-links wheelhouse flyts==0.2.0 pytest
python -m pip check
python -m pytest
python -m flyts synthetic --output data/offline-install-check
python -m flyts pretrain --manifest data/offline-install-check/manifest.json --config configs/smoke.json --output outputs/offline-install-check --device cpu
```

회사 PC에 Python 자체가 없다면 승인된 Python 설치 프로그램도 필요하다. 라이브러리를 미리
설치한 개발 환경에서만 테스트하지 말고 **network를 차단한 깨끗한 VM**에서 재현한다.
코드의 socket-blocked 테스트는 이 환경 검증을 완전히 대체하지 않는다.

## 반입 파일 구성과 검증

의도적으로 만든 `transfer/`에 wheelhouse, code/configs/docs, dataset ZIP+checksum,
승인서·출처 기록을 넣는다. 회사 자료를 일반망으로 보내는 작업은 없다.

```bash
python tools/offline_bundle.py seal --root transfer
python tools/offline_bundle.py verify --root transfer
```

이 helper는 표준 라이브러리만 쓰므로 torch 설치 전에도 실행된다. 출력된
`bundle_manifest_sha256`은 별도 승인 기록에 남긴다. 체크섬 파일까지 함께 바뀌면 checksum만으로
진위를 검증할 수 없으므로 승인된 경로와 외부 digest 기록이 중요하다. 회사 절차에 따른
악성코드 검사 및 라이선스 검토를 생략하지 않는다.

폐쇄망 반입 후 같은 verify를 실행하고 `pip --no-index`, `flyts unpack`, `flyts verify` 순서로
설치/데이터 검증을 마친다. ZIP unpack은 경로 이탈을 막고 신규 폴더만 생성한다. 기존 파일을
자동 덮어쓰지 않는다. 대용량 corpus는 분할 bundle 또는 승인된 공유 드라이브에서 직접 읽는다.

## 실행, checkpoint 및 정보보호

- `--device auto|cpu|cuda`; FP32 기본. CUDA 미설치인데 cuda를 요청하면 조용히 CPU로 바꾸지 않는다.
- `run.json`: config, actual parameter count, device, torch version, manifest hash.
- `history.json`: loss, domain별 validation, epoch 시간, τ.
- `last.pt`: 마지막 완료 epoch; `best.pt`: validation 최저 epoch.
- 안전한 재시작은 epoch 경계다. 중간 종료 epoch의 일부 step은 다시 수행한다.
- checkpoint는 `weights_only=True`로 로드한다. 출처 불명의 checkpoint를 반입하지 않는다.
- 같은 manifest/config로 epochs와 device만 바꿔 resume할 수 있다. CPU↔CUDA 수치 동일성은
  보장하지 않으며 CUDA optimizer state는 로딩 과정에서 해당 parameter 장치로 배치된다.
- 회사 raw·checkpoint·embedding·manifest(설비 ID 등 포함 가능)는 내부 산출물로 관리한다.
  `.gitignore`가 보안 통제를 대신하지 않는다. 외부 업로드 기능은 제공하지 않는다.
- 실제 GPU 시간/메모리는 카드와 입력에 따라 다르다. 8GB에 항상 맞는다는 보장은 하지 않는다.
  작은 batch/context부터 측정하고, OOM이면 줄이되 새 실험으로 기록한다.
