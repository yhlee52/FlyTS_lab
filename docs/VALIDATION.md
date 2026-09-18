# MVP 검증 기록

이 기록은 실제 실행 결과이며 범용 TSFM 성능 주장이나 회사 PC의 속도 보장이 아니다.

## 실행 환경·모델

- Python 3.12, PyTorch 2.14.0+cu130; **CUDA hardware 없음**, CPU 실행.
- smoke 17,936 parameters; cpu 68,760; full_pretrain 268,312.
- epoch 경계 resume와 연속 학습의 state_dict 동일성을 unit test로 확인.
- dense/scatter forward 및 gradient 동등성, τ/graph gradient, 채널 permutation,
  time/channel padding, masked-target 통계 누출, 결측 제외를 확인.
- socket.connect를 금지한 상태에서 synthetic 생성, train, resume, export 통합 테스트 통과.
- CUDA backward/checkpoint 테스트는 hardware 부재로 skip. 실제 GPU 검증은 남아 있음.
- wheel `flyts-0.2.0-py3-none-any.whl` 빌드 성공. OS별 전체 wheelhouse 반입 설치는 미수행.

## 실제 공개 corpus

| Dataset | 분할·gap 처리 후 records | 보존 time rows | 보존 scalar values |
|---|---:|---:|---:|
| Appliances | 3 | 19,671 | 511,446 |
| Bike | 74 | 17,274 | 69,096 |
| Beijing | 36 | 420,000 | 4,620,000 |

총 113 records, 456,945 time rows, 5,200,542 scalar positions (일부 결측 포함).
원본 값에서 split purge, 짧은 gap fragment 제거, 비사용 column 제외가 적용된 수치다.
전체 무가공 원본 수치나 독립 sample 수로 인용하면 안 된다.

prepared manifest SHA-256:
`e538e9cbf761577740f43f6930ac4653834fdc00f9d0ee567b02b52e2d0d14eb`

CPU preset, epochs=2, batch=8, steps_per_epoch=200, context=256, stride=128, threads=4.
train windows 2,497 / val windows 261. validation은 세 domain 모두 사용.

| Epoch | Train Huber loss | Val domain-mean loss | Visible-mean 복원 baseline |
|---|---:|---:|---:|
| 1 | 0.49856 | 0.47509 | 0.47626 |
| 2 | 0.47556 | 0.46680 | 0.47626 |

각 epoch은 이 runtime에서 약 11~13초. 작은 설정의 동작 검증이며 full preset의 throughput은
아니다. Accuracy/AUROC로 해석하지 않는다. Test 성능, cross-domain transfer 및 비교모델 우위는
아직 검증하지 않았다. full pretraining 50,000 steps를 완료했다고 주장하지 않는다.

ZIP pack → 새 폴더 unpack → hash verify → 동일한 offline trainer 실행을 확인했다.
반입용 public starter ZIP은 세 domain만 포함하며 코드·PyTorch 설치 파일은 별도 준비해야 한다.

## 조건 확인이 필요한 데이터

HAR 공식 archive의 9-channel waveform 변환 경로를 확인했으나, 원본 README의 commercial-use
prohibition을 발견했다. 학습/전달 기본 corpus에는 포함하지 않았고 이후 converter에 명시적
권리 확인 gate를 추가했다. Unit test는 생성한 HAR 형식 fixture만 사용한다.

UCR Wafer importer/probe는 생성 fixture로 테스트했다. 실제 Wafer나 PHM CMP를 다운로드하거나
pretraining에 포함했다고 주장하지 않는다. 권리·schema 확인이 선행되어야 한다.
