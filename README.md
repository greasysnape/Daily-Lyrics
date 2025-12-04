# Daily Lyrics - 일일 랜덤 가사

노래 가사를 랜덤으로 출력해주는 프로그램입니다.
개인적/비상업적 용도만 허용합니다.
가사 데이터베이스는 원하는 곡들로 직접 생성해야 합니다.
(* 가수 태연의 솔로곡 가사 데이터베이스는 직접 제작 중입니다. 개인적으로 요청주시면 완성 후 공유해 드리겠습니다.) 

## ✨ 특징

- 📅 **일일 가사**: 매일 다른 가사를 자동으로 선택
- 🎲 **랜덤 모드**: 원할 때 완전 랜덤 가사 보기
- 📁 **체계적 관리**: 앨범별, 트랙별로 가사 데이터 구조화

## 🚀 시작하기

### 필요 사항

- Python 3.8 이상

### 설치

```bash
# 저장소 클론 후 경로 이동
cd "Daily Lyrics"

# Python 버전 확인
python3 --version
```

### 가사 데이터 추가

#### 방법 1: 텍스트 파일로 쉽게 추가

1. **`lyrics_input/` 폴더에 가사 작성**

앨범별 폴더를 만들고 텍스트 파일로 가사 작성:
```
lyrics_input/
├── 001_I/
│   ├── 01_I.txt
│   ├── 02_U R.txt
│   ├── 03_쌍둥이자리 (Gemini).txt
│   ├── 04_스트레스 (Stress).txt
│   └── 05_먼저 말해줘 (Farewell).txt
└── 002_Rain/
│   ├── 01_Rain.txt
│   └── 02_비밀 Secret.txt
```
텍스트 파일의 포맷은 lyrics_input/example_album/example_track.txt 참고

2. **JSON으로 변환**

```bash
# 모든 폴더 변환
python3 convert_lyrics.py

# 특정 폴더만 변환
python3 convert_lyrics.py --folder 016_INVU

# 여러 폴더 변환
python3 convert_lyrics.py --folder 016_INVU 009_사계 "015_Can't Control Myself"
```

자동으로 `data/` 폴더에 JSON 파일이 생성됩니다

---

#### 방법 2: JSON 파일 직접 작성

`data/` 폴더에 앨범별로 JSON 파일을 직접 작성:

```
data/
├── 001_I/
│   ├── 01_I.json
│   ├── 02_U R.json
│   ├── 03_쌍둥이자리 (Gemini).json
│   ├── 04_스트레스 (Stress).json
│   └── 05_먼저 말해줘 (Farewell).json
└── 002_Rain/
│   ├── 01_Rain.json
│   └── 02_비밀 Secret.json
```
JSON 파일의 포맷은 data/example_album/example_track.json 참고


## 📖 사용법

### 오늘의 가사 보기

```bash
python3 cli.py
```

### 완전 랜덤 가사

```bash
python3 cli.py --random
```

### 특정 날짜의 가사

```bash
python3 cli.py --date 2025-12-01
```

### 통계 보기

```bash
python3 cli.py --stats
```

### 도움말

```bash
python3 cli.py --help
```

## 📂 프로젝트 구조

```
Daily Lyrics/
├── cli.py                  # CLI 실행 파일
├── convert_lyrics.py       # 가사 변환 도구 (txt → json)
├── src/
│   ├── __init__.py
│   ├── lyrics_database.py  # 가사 데이터베이스 관리
│   └── daily_selector.py   # 날짜 기반 선택 로직
├── lyrics_input/           # 가사 텍스트 파일 (앨범별 폴더)
├── data/                   # 변환된 JSON 가사 데이터
├── requirements.txt        # Python 패키지 의존성
└── README.md               
```

## 🎯 로드맵

- [x] **Phase 1**: CLI 기본 기능 (현재)
- [ ] **Phase 2**: GUI 인터페이스 (tkinter)
- [ ] **Phase 3**: 모바일/크로스 플랫폼 확장 (Kivy 또는 웹)

## 💡 팁

### 매일 자동 실행 (macOS/Linux)

cron을 사용하여 매일 특정 시간에 가사 표시:

```bash
# crontab 편집
crontab -e

# 매일 오전 9시에 실행
0 9 * * * cd "/Users/{username}/Path/to/Daily Lyrics" && /usr/bin/python3 cli.py
```

### 별칭 만들기

`~/.zshrc` 또는 `~/.bashrc`에 추가:

```bash
alias lyrics="python3 '/Users/{username}/Path/to/Daily Lyrics/cli.py'"
```

이후 터미널에서 `lyrics` 명령어로 간단히 실행 가능!

## 📝 저작권 고려사항

- 이 프로젝트는 개인적, 비상업적 사용을 위한 것입니다
- 가사는 1-5줄 내로 발췌합니다
- 예시로 제시한 모든 가사의 저작권은 TAEYEON 및 소속사에 있습니다

## 📜 라이선스

Kyuyeon Choi
개인 사용 목적의 프로젝트입니다.
