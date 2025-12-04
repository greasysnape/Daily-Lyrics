# Daily Lyrics Widget - macOS

macOS 배경화면에 표시되는 랜덤 가사 위젯

## 요구사항

- macOS 14.0 (Sonoma) 이상
- Xcode 15.0 이상
- Daily Lyrics API 서버 실행 중 (localhost:58384)

## 설치 방법

### 1. Xcode 프로젝트 생성

1. Xcode 실행
2. `File` > `New` > `Project...`
3. `macOS` 탭 선택
4. `App` 템플릿 선택 > `Next`
5. 프로젝트 정보 입력:
   - Product Name: `DailyLyricsWidget`
   - Team: 본인 개발자 계정
   - Organization Identifier: `com.yourname` (원하는 식별자)
   - Interface: `SwiftUI`
   - Language: `Swift`
   - Include Tests: 체크 해제 가능
6. 저장 위치 선택 > `Create`

### 2. Widget Extension 추가

1. 프로젝트 네비게이터에서 프로젝트 선택
2. `File` > `New` > `Target...`
3. `macOS` 탭 선택
4. `Widget Extension` 선택 > `Next`
5. 정보 입력:
   - Product Name: `DailyLyricsWidgetExtension`
   - Include Configuration Intent: 체크 해제
6. `Finish` 클릭
7. "Activate 'DailyLyricsWidgetExtension' scheme?" 팝업 > `Activate` 클릭

### 3. 생성된 Swift 코드 교체

Widget Extension 폴더(`DailyLyricsWidgetExtension`)에 자동 생성된 파일들을 삭제하고, 이 폴더의 파일들로 교체:

1. 자동 생성된 `DailyLyricsWidgetExtension.swift` 파일 삭제
2. 다음 파일들을 Widget Extension 타겟에 추가:
   - `LyricsModels.swift`
   - `LyricsAPIService.swift`
   - `DailyLyricsWidget.swift`

**파일 추가 방법:**
- Xcode 프로젝트 네비게이터에서 `DailyLyricsWidgetExtension` 폴더에 우클릭
- `Add Files to "DailyLyricsWidget"...` 선택
- 위 3개 파일 선택
- `Copy items if needed` 체크
- `Add to targets`에서 `DailyLyricsWidgetExtension` 체크
- `Add` 클릭

### 4. 네트워크 권한 설정

Widget Extension이 로컬 서버에 접근하려면 권한 설정이 필요합니다:

1. 프로젝트 네비게이터에서 `DailyLyricsWidgetExtension` 타겟 선택
2. `Signing & Capabilities` 탭
3. `+ Capability` 클릭
4. `App Sandbox` 검색 후 추가
5. `Network` 섹션에서:
   - ✅ `Outgoing Connections (Client)` 체크

또는 `Info.plist`에 직접 추가:
```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsLocalNetworking</key>
    <true/>
</dict>
```

### 5. 빌드 및 실행

1. Xcode 상단 스킴에서 `DailyLyricsWidgetExtension` 선택
2. `Product` > `Run` (또는 ⌘R)
3. 위젯 시뮬레이터가 실행됩니다

### 6. macOS에 위젯 추가

1. 위젯이 정상 동작하면, 앱을 종료
2. macOS 바탕화면에서 우클릭 > `Edit Widgets...`
3. 왼쪽 위젯 목록에서 `Daily Lyrics` 찾기
4. 원하는 크기 선택 (Small, Medium, Large)
5. 위젯을 바탕화면에 드래그

## 설정

### 가사 변경 주기 변경

`DailyLyricsWidget.swift` 파일에서 `LyricsProvider` 클래스의 `interval` 값을 변경:

```swift
private let interval = "3h"  // 1h, 3h, 6h, 12h, 24h 중 선택
```

- `1h`: 1시간마다 변경
- `3h`: 3시간마다 변경 (기본값)
- `6h`: 6시간마다 변경
- `12h`: 12시간마다 변경
- `24h`: 24시간마다 변경

변경 후 프로젝트를 다시 빌드하세요.

## 트러블슈팅

### "서버 연결 오류" 표시

1. Daily Lyrics API 서버가 실행 중인지 확인:
   ```bash
   curl http://localhost:58384/health
   ```

2. launchd 서비스 상태 확인:
   ```bash
   launchctl list | grep dailylyrics
   ```

3. 서비스 재시작:
   ```bash
   launchctl unload ~/Library/LaunchAgents/com.dailylyrics.widget.plist
   launchctl load ~/Library/LaunchAgents/com.dailylyrics.widget.plist
   ```

### 위젯이 업데이트되지 않음

- 위젯 우클릭 > `Reload Widget`
- 또는 위젯을 제거했다가 다시 추가

### 빌드 에러 발생

- Xcode 버전이 15.0 이상인지 확인
- macOS 버전이 14.0 이상인지 확인
- Deployment Target이 macOS 14.0으로 설정되어 있는지 확인

## 프로젝트 구조

```
DailyLyricsWidget/
├── DailyLyricsWidget/              # 메인 앱 (필요 시 설정 UI 추가)
└── DailyLyricsWidgetExtension/     # 위젯 Extension
    ├── LyricsModels.swift          # 데이터 모델
    ├── LyricsAPIService.swift      # API 통신
    └── DailyLyricsWidget.swift     # 위젯 UI 및 로직
```

## 다음 단계

- iOS 위젯: 동일한 코드를 iOS 프로젝트에서 재사용 가능
- 위젯 크기별 레이아웃 최적화
- 다크모드 지원 개선
- 위젯 설정 UI (메인 앱)
