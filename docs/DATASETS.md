# 공개 corpus 전략 및 데이터 카드

## MVP full-pretrain corpus

많은 파일 수보다 waveform 의미와 분할 신뢰성을 우선한다. 아래는 **완전한 원본을 변환하는
3-domain starter corpus + 권리 확인이 필요한 HAR 옵션**이며, 산업 전체를 대표하는 web-scale dataset은 아니다.
`full_pretrain.json`은 이 corpus를 사용해 모델 전체를 처음부터 학습하는 시작 예산이다.

| ID | 도메인 / 사용 데이터 | 시간 | 분할 / 가공 |
|---|---|---|---|
| appliances | 건물 에너지·온습도, 약 19.7K 시점 | 600초 | 시간순 70/15/15; 임의 생성 rv1/rv2 제거 |
| bike | 교통 수요·날씨, 시간별 데이터 | 3600초 | 시간순 70/15/15; 빈 시간에서 segment 분리; ID·달력 categorical 제외 |
| beijing | 12 지점 대기질·기상, 약 420K 시점 | 3600초 | 지점별 시간순 70/15/15; NA 유지; wind-direction categorical 제외 |
| har (기본 제외) | 인체 동작, 9개 inertial waveform, 10,299 windows | 0.02초 | 권리 확인 후 사용; official test subject 유지; train subject 중 마지막 4명은 val |

각 연속 recording에서 **먼저 시간 분할**하고 경계 이후 32 points를 purge한 뒤 window를 만든다.
정상적인 관측 0과 결측을 구분한다. interpolation으로 미래 정보를 채워 넣지 않는다.
HAR의 50%-overlap 원본 window는 subject 단위로 분리하므로 서로 다른 split에 겹친 sample이
섞이지 않는다. 기존 561-feature 표를 time axis로 오인하지 않는다. HAR manifest의 start/stop은
window 식별용 가상 offset이며 실제 연속 시간이나 활동 사이 간격을 의미하지 않는다.

Bike는 cnt=casual+registered 합계의 복원 shortcut을 피하려고 temp/hum/windspeed/cnt만 사용한다.
Beijing은 station 간 지리 전이 평가가 아니라 시간 holdout이다. held-out domain 평가를 하려면
그 domain을 pretrain manifest에서 아예 제외해야 한다.

### 원출처와 attribution

- [Appliances, UCI](https://archive.ics.uci.edu/dataset/374/appliances+energy+prediction):
  Candanedo, L. (2017), DOI 10.24432/C5VC8G. CC BY 4.0 표기.
- [Bike Sharing, UCI](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset):
  Fanaee-T, H. (2013), DOI 10.24432/C5W894. CC BY 4.0 표기.
- [Beijing Multi-Site, UCI](https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data):
  Chen, S. (2017), DOI 10.24432/C5RK5G. CC BY 4.0 표기.
- [HAR, UCI](https://archive.ics.uci.edu/dataset/240/human+activity+recognition+using+smartphones):
  Reyes-Ortiz et al. (2013), DOI 10.24432/C54S4K. 현재 UCI 페이지 CC BY 4.0이지만,
  실제 원본 `UCI HAR Dataset/README.txt`에 상업적 사용 금지 문구가 있어 기본 묶음에서 제외.
  단순 회사 내부 승인이 원권리자의 제한을 무효화하지 않으며 실제 사용 권한 확인이 필요하다.
  `prepare --datasets ... har --approval-reference RIGHTS-CLEARANCE-REFERENCE`로 추적한다.
- [CC BY 4.0 원문](https://creativecommons.org/licenses/by/4.0/): 반입 시 원저자·출처·변경사항을
  유지한다. 회사 정책, 원본 README와 기타 조건의 충돌 여부는 별도 검토 대상이다.

위 목록은 데이터 이용조건에 대한 법률 보증이 아니다. 특히 원본 압축파일의 README/notice도
함께 검토해야 한다. converter가 `source_notices.json`에 동봉 문서를 보존하고 pack에도 포함한다.
회사 반입 전 자료 소유자/보안/법무 정책에 따른 승인을 기록한다. 조건이 모호하면 제외한다.

## 반도체 데이터

### UCR Wafer — 선택적 로컬 importer 제공

[원본 설명](https://www.timeseriesclassification.com/description.php?Dataset=Wafer)에 따르면
반도체 wafer 공정의 sensor별 waveform이며 train 1,000/test 6,164, 길이 152, **단일 채널**이다.
서로 다른 sensor trace를 동시 관측된 다채널처럼 쌓지 않는다. 물리 sampling rate가 없으므로
sample clock으로 기록한다. 공식 페이지에서 명확한 사용 허락을 확정하지 못해 기본 자동
다운로드 묶음에는 넣지 않았다. 승인 후 다음과 같이 TSV를 반입할 수 있다.

```bash
python -m flyts prepare-wafer --train-file private_data/Wafer_TRAIN.tsv --test-file private_data/Wafer_TEST.tsv --approval-reference INTERNAL-REVIEW-ID --output data/wafer-v1
python -m flyts merge --manifests data/public-v1/manifest.json data/wafer-v1/manifest.json --output data/with-wafer
```

공식 test는 그대로 유지하고 원 train 중 seed=7로 20%를 val로 분리한다. 제공된 wafer/tool
식별자가 없어 장비/lot 단위 독립성을 보장할 수 없다는 한계가 있다. 입력 label은 분리 보관한다.

### PHM 2016 CMP — 우선순위 높은 확장 후보, 자동 수집 미포함

[관련 연구](https://arxiv.org/abs/2503.01176)는 wafer chemical-mechanical polishing의 다채널
시계열을 사용한다. 본 작업에서는 원 배포 페이지 접근/이용조건을 확정하지 못했으므로
데이터 확보나 전용 converter 검증을 완료했다고 주장하지 않는다. 승인된 원본을 확보하면:

1. 실제 header·단위·시간열·wafer/chamber/stage 경계를 확인한다.
2. ID, 제거율/품질 target, 사후 측정값을 입력에서 제외한다.
3. wafer/stage별 recording을 만들고 중복 timestamp와 sampling gap을 처리한다.
4. 시간·lot·장비 기준으로 train/val/test를 지정하고 로컬 CSV 규격으로 변환한다.
5. `prepare-local`과 `merge`로 동일 학습 경로에 넣는다.

이 계획은 전용 CMP adapter가 이미 있다는 뜻은 아니다. 공개 availability와 회사 사용 허용은
별개이며 승인 없는 mirror에서 데이터를 가져오지 않는다.

### SECOM — waveform 사전학습에서 제외

[UCI SECOM](https://archive.ics.uci.edu/dataset/179/secom)은 생산 entity별 feature와 pass/fail
label이다. 591개 feature 축을 591개 time step처럼 재해석하면 잘못된 시간 관계를 학습한다.
이번 waveform corpus에서는 제외하고 나중에 wafer-level representation 보조 과제로 검토한다.

### 기타 확장 우선순위

산업 회전체/터빈, 생체신호, 날씨·전력·교통을 늘려야 한다. NASA C-MAPSS, PhysioNet,
UCR/UEA 전체, 대형 TSFM corpus 등은 원본 schema와 dataset별 license/benchmark contamination을
검토한 뒤 전용 converter를 추가한다. 현재 CLI가 이들 전체를 지원한다고 간주하면 안 된다.
UCI Air Quality(360)는 페이지에 CC BY 표기와 별도로 research-only/commercial-excluded 설명이
공존하여 기본 묶음에서 제외했다. [출처](https://archive.ics.uci.edu/dataset/360/air+quality)

## 품질/재현성과 scaling

- `sources.lock.json`은 원본 URL·DOI·해시를 기록한다. 첫 다운로드 해시는 publisher signature가
  아니라 신뢰한 공식 URL에서 받은 bytes의 snapshot이다. 변경되면 자동 수용하지 않는다.
- prepared manifest는 각 NPY shape/channel/dt/domain/dataset/split/group/range/hash를 기록한다.
- `verify`는 파일 손상·경로 이탈·source range split 중첩을 검사한다. 잘못 입력된 group ID나
  원 데이터의 의미 오류까지 증명할 수는 없으므로 source-level 리뷰가 필요하다.
- full dataset의 모든 파일은 변환하지만 학습은 균형 sampling 예산 내 windows를 사용한다.
- synthetic은 debug corpus로 분리하며 실데이터 pretrain에 자동 혼합하지 않는다.
- 더 큰 corpus에서는 총 sample 수뿐 아니라 domain별 validation, missing 비율, channel 수,
  sampling rate, downstream frozen probe를 함께 추적한다. 데이터 양만 늘려 성능을 주장하지 않는다.
