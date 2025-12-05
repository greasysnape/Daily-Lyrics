# Daily Lyrics - 일일 랜덤 가사

노래 가사를 랜덤으로 표시하는 위젯 시스템입니다.

- 개인적/비상업적 용도만 허용합니다.
- 가사 데이터베이스는 원하는 곡들로 직접 생성해야 합니다.
- (* 가수 태연의 솔로곡 가사 데이터베이스는 직접 제작 중입니다. 개인적으로 요청주시면 완성 후 공유해 드리겠습니다.)

## ✨ 특징

- 🖼️ **앨범 커버 배경**: 가사와 함께 해당 곡의 앨범 커버를 배경으로 표시
- 📱 **멀티플랫폼 위젯**: macOS, iOS, Android, Windows 지원
- 📅 **자동 업데이트**: 설정한 시간 간격마다 새로운 가사로 자동 변경
- ⏰ **시간 주기 설정**: 1시간, 3시간, 6시간, 12시간, 24시간 단위로 가사 변경
- 🎲 **랜덤 모드**: 원할 때 완전 랜덤 가사 보기 (API 엔드포인트)
- 📁 **체계적 관리**: 앨범별, 트랙별로 가사 데이터 구조화
- 🌐 **REST API**: FastAPI 기반 경량 서버

## 🚀 시작하기

### 필요 사항

- Python 3.8 이상
- macOS 14+ (macOS 위젯)
- iOS 16+ (iOS 위젯)
- Android 8.0+ (Android 위젯)
- Windows 11 (Windows 위젯)

### 설치

```bash
# 저장소 클론 후 경로 이동
cd "Daily Lyrics"

# Python 버전 확인
python3 --version

# Python 패키지 설치 (FastAPI, uvicorn 등)
pip3 install -r requirements.txt
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
텍스트 파일의 포맷은 `lyrics_input/example_album/example_track.txt` 참고

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
JSON 파일의 포맷은 `data/example_album/example_track.json` 참고

### 앨범 커버 이미지 추가

위젯 배경으로 사용할 앨범 커버 이미지를 `data/covers/` 폴더에 추가:

```
data/covers/
├── 001_I.jpeg
├── 002_Rain.jpeg
├── 003_Why.jpeg
└── ...
```

- 파일명은 앨범 폴더명과 동일하게 (예: `001_I.jpeg`)
- WebP 또는 JPEG 형식
- 권장 크기: 1000×1000px 이상

## 📖 사용법

### 1. 서버 실행

위젯이 작동하려면 먼저 백엔드 서버를 실행해야 합니다:

```bash
# 개발 모드 (수동 실행)
python3 -m uvicorn src.widget_service:app --host 0.0.0.0 --port 58384

# 또는 백그라운드 실행
python3 -m uvicorn src.widget_service:app --host 0.0.0.0 --port 58384 &
```

서버가 실행되면 `http://127.0.0.1:58384`에서 API를 사용할 수 있습니다.

#### macOS 자동 실행 설정 (launchd)

서버를 macOS 시작 시 자동으로 실행하려면:

1. `setup_launchd.sh` 스크립트 실행:
```bash
bash setup_launchd.sh
```

2. 서비스 상태 확인:
```bash
launchctl list | grep dailylyrics
```

3. 로그 확인:
```bash
tail -f ~/Library/Logs/DailyLyricsWidget.log
```

### 2. 위젯 설치

#### macOS 위젯

1. Xcode에서 `Daily Lyrics.xcodeproj` 열기
2. 타겟을 "Daily Lyrics WidgetExtension"으로 선택
3. Run (▶️) 버튼 클릭
4. 위젯 선택 후 Notification Center에 추가

**또는**

1. Xcode에서 Archive 후 앱 설치
2. Notification Center 열기 (트랙패드 2본 손가락으로 오른쪽 끝에서 스와이프)
3. 하단의 "Edit Widgets" 클릭
4. "Daily Lyrics" 위젯 추가

**지원 크기**: Medium, Large

#### iOS 위젯

1. Xcode에서 iOS 디바이스 선택
2. "Daily Lyrics iOS WidgetExtension" 타겟으로 실행
3. 홈 화면 롱프레스 → 왼쪽 상단 + 버튼
4. Daily Lyrics 위젯 추가

**지원 크기**: Medium, Large

#### Android 위젯

1. Android Studio에서 프로젝트 열기 (`widgets/android/`)
2. 앱 빌드 및 설치
3. 홈 화면 롱프레스 → 위젯 → Daily Lyrics 선택

#### Windows 위젯

1. Visual Studio에서 프로젝트 열기 (`widgets/windows/`)
2. WinUI 3 앱 빌드 및 실행
3. 데스크톱에 자동으로 위젯 표시

### 3. CLI 사용법 (옵션)

서버를 통하지 않고 직접 CLI로도 가사를 볼 수 있습니다:

```bash
# 오늘의 가사
python3 cli.py

# 시간 주기별 가사
python3 cli.py --interval 3h

# 완전 랜덤 가사
python3 cli.py --random

# 특정 날짜의 가사
python3 cli.py --date 2025-12-01

# 통계 보기
python3 cli.py --stats
```

### 4. API 엔드포인트

서버가 실행 중일 때 사용 가능:

- `GET /` - 서버 정보
- `GET /current-lyric?interval=3h` - 현재 시간 주기의 가사
- `GET /random-lyric` - 완전 랜덤 가사
- `GET /stats` - 데이터베이스 통계
- `GET /health` - 서버 상태 확인
- `GET /covers/{filename}` - 앨범 커버 이미지

## 📂 프로젝트 구조

```
Daily Lyrics/
├── cli.py                      # CLI 실행 파일
├── convert_lyrics.py           # 가사 변환 도구 (txt → json)
├── setup_launchd.sh            # macOS 자동 실행 설정 스크립트
├── src/
│   ├── __init__.py
│   ├── lyrics_database.py      # 가사 데이터베이스 관리
│   ├── daily_selector.py       # 날짜 기반 선택 로직
│   └── widget_service.py       # FastAPI 백엔드 서버
├── widgets/
│   ├── macos/                  # macOS 위젯 (SwiftUI)
│   │   ├── DailyLyricsWidget.swift
│   │   ├── LyricsModels.swift
│   │   └── LyricsAPIService.swift
│   ├── ios/                    # iOS 위젯 (SwiftUI)
│   ├── android/                # Android 위젯 (Kotlin)
│   └── windows/                # Windows 위젯 (WinUI 3 / C#)
├── lyrics_input/               # 가사 텍스트 파일 (앨범별 폴더)
├── data/                       # 변환된 JSON 가사 데이터
│   └── covers/                 # 앨범 커버 이미지
├── requirements.txt            # Python 패키지 의존성
└── README.md
```

## ⚙️ 설정

### 위젯 업데이트 간격 변경

각 플랫폼의 위젯 파일에서 `interval` 값을 수정:

**macOS/iOS**: `widgets/macos/DailyLyricsWidget.swift:14`
```swift
private let interval = "3h"  // 1h, 3h, 6h, 12h, 24h 중 선택
```

**Android**: `widgets/android/LyricsWidget.kt`
```kotlin
private const val DEFAULT_INTERVAL = "3h"
```

**Windows**: `widgets/windows/MainWindow.xaml.cs:19`
```csharp
private const string DEFAULT_INTERVAL = "3h";
```

## 🎯 로드맵

- [x] **Phase 1**: CLI 기본 기능
- [x] **Phase 2**: REST API 백엔드 (FastAPI)
- [x] **Phase 3**: 멀티플랫폼 위젯 (macOS, iOS, Android, Windows)
- [x] **Phase 4**: 앨범 커버 배경 이미지
- [ ] **Phase 5**: 위젯 설정 UI (간격 변경, 테마 선택)
- [ ] **Phase 6**: 가사 공유 기능

## 💡 팁

### 별칭 만들기 (CLI 사용 시)

`~/.zshrc` 또는 `~/.bashrc`에 추가:

```bash
alias lyrics="python3 '/Path/to/Daily Lyrics/cli.py'"
```

이후 터미널에서 `lyrics` 명령어로 간단히 실행 가능

### 서버 포트 변경

기본 포트 58384를 변경하려면:

1. `src/widget_service.py`의 uvicorn 실행 명령에서 `--port` 변경
2. 각 위젯의 API 서비스 파일에서 baseURL 포트 변경
   - macOS/iOS: `LyricsAPIService.swift`
   - Android: `LyricsAPIService.kt`
   - Windows: `LyricsAPIService.cs`

### 네트워크 디버깅

서버 로그를 방법:

```bash
# 실시간 로그 확인 (macOS launchd 사용 시)
tail -f ~/Library/Logs/DailyLyricsWidget.log

# 서버 수동 실행 시 콘솔에서 직접 확인
```

위젯이 서버에 요청을 보낼 때마다 로그에 표시됩니다.

## 🐛 문제 해결

### 위젯에 가사가 표시되지 않음

1. 서버가 실행 중인지 확인:
   ```bash
   curl http://127.0.0.1:58384/health
   ```

2. launchd 서비스 상태 확인 (macOS):
   ```bash
   launchctl list | grep dailylyrics
   ```

3. 위젯을 제거하고 다시 추가

### 앨범 커버가 표시되지 않음

1. `data/covers/` 폴더에 이미지 파일이 있는지 확인
2. 파일명이 앨범 폴더명과 일치하는지 확인 (예: `001_I.webp`)
3. 서버 로그에서 `/covers/` 엔드포인트 요청 확인

### iOS 위젯에서 연결 오류

iOS는 localhost를 지원하지 않으므로:
1. Mac과 iPhone이 같은 Wi-Fi에 연결
2. Mac의 로컬 IP 주소 확인: `ifconfig | grep inet`
3. 위젯의 baseURL을 Mac의 IP로 변경 (예: `http://192.168.1.100:58384`)

## 📝 저작권 고려사항

- 이 프로젝트는 개인적, 비상업적 사용을 위한 것입니다
- 가사는 1-5줄 내로 발췌합니다
- 예시로 제시한 모든 가사의 저작권은 TAEYEON 및 소속사에 있습니다
- 앨범 커버 이미지의 저작권은 SM Entertainment에 있습니다

## 📜 라이선스

- Kyuyeon Choi (cky0312@g.skku.edu)
- 개인적/비상업적 사용 목적의 프로젝트입니다
