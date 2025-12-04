# Daily Lyrics Widget - iOS

iOS 홈 화면과 잠금 화면에 표시되는 태연 가사 위젯입니다.

## 요구사항

- iOS 14.0 이상
- Xcode 15.0 이상
- Mac과 iPhone이 같은 Wi-Fi 네트워크에 연결되어 있어야 함
- Daily Lyrics API 서버가 Mac에서 실행 중 (localhost:58384)

## 설치 방법

### 1. Xcode 프로젝트 생성

1. Xcode 실행
2. `File` > `New` > `Project...`
3. `iOS` 탭 선택
4. `App` 템플릿 선택 > `Next`
5. 프로젝트 정보 입력:
   - Product Name: `DailyLyricsWidget`
   - Team: 본인 개발자 계정
   - Organization Identifier: `com.yourname`
   - Interface: `SwiftUI`
   - Language: `Swift`
6. 저장 위치 선택 > `Create`

### 2. Widget Extension 추가

1. 프로젝트 네비게이터에서 프로젝트 선택
2. `File` > `New` > `Target...`
3. `iOS` 탭 선택
4. `Widget Extension` 선택 > `Next`
5. 정보 입력:
   - Product Name: `DailyLyricsWidgetExtension`
   - Include Configuration Intent: 체크 해제
6. `Finish` 클릭
7. "Activate scheme?" 팝업 > `Activate` 클릭

### 3. Swift 코드 추가

Widget Extension 폴더에 자동 생성된 파일 삭제 후, 다음 파일들 추가:

- `LyricsModels.swift`
- `LyricsAPIService.swift`
- `DailyLyricsWidget.swift`

**파일 추가 방법:**
- Xcode에서 `DailyLyricsWidgetExtension` 폴더에 우클릭
- `Add Files to...` 선택
- 위 3개 파일 선택
- `Copy items if needed` 체크
- `Add to targets`에서 `DailyLyricsWidgetExtension` 체크

### 4. 네트워크 설정

#### A. Info.plist 설정

`DailyLyricsWidgetExtension` 타겟의 Info.plist에 추가:

1. Info.plist 파일 우클릭 > `Open As` > `Source Code`
2. `<dict>` 태그 안에 다음 추가:

```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsLocalNetworking</key>
    <true/>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>
```

#### B. API 서버 접근 설정

iPhone이 Mac의 로컬 서버에 접근하려면:

**방법 1: Mac의 로컬 IP 사용 (권장)**

1. Mac의 IP 주소 확인:
   ```bash
   ifconfig | grep "inet " | grep -v 127.0.0.1
   ```
   예: `192.168.0.10`

2. `LyricsAPIService.swift` 파일에서 `baseURL` 수정:
   ```swift
   private let baseURL = "http://192.168.0.10:58384"  // Mac의 IP로 변경
   ```

**방법 2: Xcode Simulator 사용 (개발/테스트용)**

Simulator에서는 `localhost`가 Mac을 가리키므로 코드 변경 불필요.

### 5. 빌드 및 실행

1. iPhone을 Mac에 연결하거나 Simulator 선택
2. 상단 스킴에서 `DailyLyricsWidgetExtension` 선택
3. `Product` > `Run` (⌘R)
4. 위젯이 실행됩니다

### 6. iPhone에 위젯 추가

#### 홈 화면에 추가:
1. 홈 화면 빈 곳을 길게 누름
2. 왼쪽 상단 `+` 버튼
3. `Daily Lyrics` 검색
4. 위젯 크기 선택 (Small, Medium, Large)
5. `Add Widget` 탭

#### 잠금 화면에 추가 (iOS 16+):
1. 잠금 화면 길게 누름
2. `Customize` 탭
3. 위젯 영역 탭
4. `Daily Lyrics` 선택
5. `Done`

## 네트워크 설정 상세

### 로컬 네트워크에서 서버 접근

1. **Mac과 iPhone이 같은 Wi-Fi에 연결**되어 있어야 합니다

2. **Mac의 방화벽 설정 확인**:
   - 시스템 설정 > 네트워크 > 방화벽
   - Python이 수신 연결을 허용하도록 설정

3. **서버가 0.0.0.0에 바인딩되어 있는지 확인**:
   ```bash
   # 이미 설정되어 있음
   launchctl list | grep dailylyrics
   ```

4. **연결 테스트**:
   - Safari에서 `http://[Mac-IP]:58384/health` 접속
   - 성공하면 JSON 응답 표시

### 실제 iPhone 기기 사용 시 (Simulator 아님)

반드시 Mac의 IP 주소로 `LyricsAPIService.swift`의 `baseURL`을 변경해야 합니다:

```swift
// localhost (X) - 실제 기기에서 작동 안 함
// private let baseURL = "http://localhost:58384"

// Mac의 IP 주소 사용 (O)
private let baseURL = "http://192.168.0.10:58384"
```

## 설정

### 가사 변경 주기 변경

`DailyLyricsWidget.swift`의 `interval` 값 변경:

```swift
private let interval = "3h"  // 1h, 3h, 6h, 12h, 24h
```

## 트러블슈팅

### "서버 연결 필요" 표시

1. **Mac의 API 서버 확인**:
   ```bash
   curl http://localhost:58384/health
   ```

2. **iPhone에서 Mac IP로 접근 테스트**:
   - Safari 열기
   - `http://[Mac-IP]:58384/health` 입력
   - JSON 응답이 나오면 정상

3. **같은 Wi-Fi 네트워크 확인**:
   - Mac: Wi-Fi 설정에서 네트워크 이름 확인
   - iPhone: 설정 > Wi-Fi에서 같은 네트워크 확인

4. **방화벽 확인**:
   - Mac 시스템 설정 > 네트워크 > 방화벽
   - Python 허용 확인

### 위젯이 업데이트되지 않음

- 위젯 길게 누르기 > `Edit Widget` > 다시 추가
- 홈 화면 편집 모드에서 위젯 제거 후 재추가
- iPhone 재시작

### Xcode에서 빌드 에러

- iOS Deployment Target이 14.0 이상인지 확인
- Widget Extension의 Bundle ID가 메인 앱 ID의 하위인지 확인
  - 예: 메인 `com.example.app`, 위젯 `com.example.app.widget`

## 개발 팁

### Simulator vs 실제 기기

- **Simulator**: `localhost` 사용 가능 (Mac을 가리킴)
- **실제 기기**: Mac의 IP 주소 필수

### 위젯 디버깅

1. Xcode에서 위젯 scheme 선택
2. Breakpoint 설정
3. Run하면 위젯이 디버그 모드로 실행

### 위젯 갤러리 프리뷰 보기

코드 하단의 `DailyLyricsWidget_Previews`에서:
- `.systemSmall`, `.systemMedium`, `.systemLarge` 모두 미리보기 가능

## 다음 단계

- [ ] 위젯 크기별 레이아웃 최적화
- [ ] 다크모드 색상 개선
- [ ] 잠금 화면 위젯 지원 (iOS 16+)
- [ ] 위젯 설정 앱 추가
- [ ] 오프라인 모드 (캐시 사용)
