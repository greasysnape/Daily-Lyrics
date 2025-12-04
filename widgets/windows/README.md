# Daily Lyrics Widget - Windows

Windows 바탕화면에 항상 표시되는 태연 가사 위젯입니다.

## 요구사항

- Windows 10 (1809) 이상 또는 Windows 11
- Visual Studio 2022 (Community 이상)
  - .NET Desktop Development 워크로드
  - Windows App SDK 설치
- Daily Lyrics API 서버가 실행 중 (localhost:58384)

## 설치 방법

### 1. Visual Studio 설치

1. [Visual Studio 2022](https://visualstudio.microsoft.com/downloads/) 다운로드
2. 설치 시 워크로드 선택:
   - ✅ `.NET Desktop Development`
   - ✅ `Universal Windows Platform development`
3. 설치 완료

### 2. Windows App SDK 설치

Visual Studio에서:
1. `Tools` > `Get Tools and Features...`
2. `Individual components` 탭
3. `Windows App SDK C# Templates` 검색 및 설치

또는 명령줄에서:
```powershell
dotnet new install Microsoft.WindowsAppSDK.Templates
```

### 3. 프로젝트 생성

1. Visual Studio 실행
2. `Create a new project` 클릭
3. `WinUI 3 App in Desktop (C#)` 템플릿 검색 및 선택
4. 프로젝트 정보 입력:
   - Project name: `DailyLyricsWidget`
   - Location: 원하는 위치
   - Framework: `.NET 8.0` (또는 최신 버전)
5. `Create` 클릭

### 4. 파일 추가

프로젝트에 다음 파일 추가:

#### A. Models 폴더 생성 후 추가:
- `LyricsModels.cs`

#### B. Services 폴더 생성 후 추가:
- `LyricsAPIService.cs`

#### C. 기존 파일 교체:
- `MainWindow.xaml`
- `MainWindow.xaml.cs`

**파일 추가 방법:**
- Solution Explorer에서 프로젝트 우클릭
- `Add` > `Existing Item...`
- 파일 선택 후 `Add`

### 5. NuGet 패키지 설치

`Tools` > `NuGet Package Manager` > `Package Manager Console`:

```powershell
Install-Package System.Text.Json
```

### 6. 프로젝트 파일 수정

`DailyLyricsWidget.csproj` 파일을 편집하여 다음 추가:

```xml
<PropertyGroup>
    <TargetFramework>net8.0-windows10.0.19041.0</TargetFramework>
    <TargetPlatformMinVersion>10.0.17763.0</TargetPlatformMinVersion>
    <WindowsSdkPackageVersion>10.0.19041.38</WindowsSdkPackageVersion>
</PropertyGroup>
```

### 7. App.xaml 수정 (시스템 트레이 지원)

`App.xaml.cs`에서 `OnLaunched` 메서드 수정:

```csharp
protected override void OnLaunched(Microsoft.UI.Xaml.LaunchActivatedEventArgs args)
{
    m_window = new MainWindow();
    m_window.Activate();

    // 최소화 시 숨기기
    m_window.AppWindow.Hiding += (sender, e) =>
    {
        e.Cancel = true;
        m_window.Hide();
    };
}
```

### 8. 빌드 및 실행

1. `Build` > `Build Solution` (Ctrl+Shift+B)
2. `Debug` > `Start Debugging` (F5)
3. 위젯이 화면 오른쪽 하단에 표시됩니다

## 사용 방법

### 위젯 조작

- **드래그**: 위젯을 클릭하고 드래그하여 위치 변경
- **우클릭**: 컨텍스트 메뉴 표시
  - 새로고침: 가사 즉시 업데이트
  - 설정: 위젯 설정 (개발 예정)
  - 종료: 위젯 종료

### 자동 시작 설정

Windows 시작 시 자동 실행:

1. 빌드된 실행 파일 위치 찾기:
   ```
   DailyLyricsWidget\bin\x64\Debug\net8.0-windows10.0.19041.0\
   ```

2. 실행 파일의 바로가기 생성

3. 시작 프로그램 폴더에 복사:
   - `Win + R` 누르기
   - `shell:startup` 입력
   - 바로가기 붙여넣기

## 설정

### 가사 변경 주기 변경

`MainWindow.xaml.cs` 파일에서 `DEFAULT_INTERVAL` 변경:

```csharp
private const string DEFAULT_INTERVAL = "3h";  // 1h, 3h, 6h, 12h, 24h
```

### 자동 업데이트 주기 변경

`StartAutoUpdate()` 메서드에서:

```csharp
// 3시간마다 업데이트
updateTimer.Interval = TimeSpan.FromHours(3);
```

### 위젯 크기 변경

`MainWindow.xaml`에서:

```xml
<Window
    ...
    Width="400"
    Height="300"
    ...>
```

### 위젯 위치 변경

`SetInitialPosition()` 메서드 수정:
- 오른쪽 하단 (기본값)
- 왼쪽 상단
- 중앙
- 사용자 지정 위치

## 트러블슈팅

### "서버 연결 필요" 표시

1. **API 서버 확인**:
   ```powershell
   curl http://localhost:58384/health
   ```

2. **방화벽 확인**:
   - Windows Defender 방화벽 설정
   - Python 허용 확인

3. **서비스 재시작**:
   ```bash
   # Mac/Linux에서
   launchctl unload ~/Library/LaunchAgents/com.dailylyrics.widget.plist
   launchctl load ~/Library/LaunchAgents/com.dailylyrics.widget.plist
   ```

### 빌드 에러

**"Windows App SDK not found":**
- `Tools` > `Get Tools and Features...`
- Windows App SDK 설치 확인

**NuGet 복원 실패:**
```powershell
dotnet restore
```

**런타임 에러:**
- Visual Studio를 관리자 권한으로 실행
- Windows 업데이트 확인

### 위젯이 사라짐

- 작업 관리자에서 프로세스 확인
- 실행 파일 재실행

## 고급 설정

### 투명도 조절

`MainWindow.xaml`에서:

```xml
<Border
    Background="#F5F5F5"  <!-- 불투명도 조절: #CCFFFFFF (80% 투명) -->
    ...>
```

### 항상 위에 표시

`MainWindow.xaml`에서:

```xml
<Window
    ...
    Topmost="True"
    ...>
```

`False`로 변경하면 다른 창에 가려질 수 있음

### 시스템 트레이 아이콘 추가

추가 라이브러리 필요:
```powershell
Install-Package Hardcodet.NotifyIcon.Wpf
```

## 프로젝트 구조

```
DailyLyricsWidget/
├── Models/
│   └── LyricsModels.cs           # 데이터 모델
├── Services/
│   └── LyricsAPIService.cs       # API 통신
├── MainWindow.xaml               # UI 레이아웃
├── MainWindow.xaml.cs            # UI 로직
├── App.xaml                      # 앱 설정
└── App.xaml.cs                   # 앱 초기화
```

## 배포

### 릴리스 빌드

1. `Build` > `Configuration Manager`
2. `Active solution configuration`: `Release`
3. `Build` > `Build Solution`

### 실행 파일 위치

```
bin\x64\Release\net8.0-windows10.0.19041.0\win-x64\
```

### MSIX 패키지 생성 (스토어 배포용)

1. Solution Explorer에서 프로젝트 우클릭
2. `Publish` > `Create App Packages`
3. 마법사 따라 진행

## 알려진 제한사항

- Windows 11 위젯 패널에는 통합되지 않음 (별도 앱)
- 배경화면에 완전히 고정되지 않음 (항상 위에 표시)
- 시스템 리소스 사용 (최소화 권장)

## 대안: PowerShell 스크립트

간단한 데스크톱 오버레이를 원한다면 PowerShell 스크립트 사용 가능 (별도 제공)

## 다음 단계

- [ ] 시스템 트레이 아이콘
- [ ] 설정 UI (간격, 폰트, 색상)
- [ ] 다중 위젯 지원
- [ ] 드래그 앤 드롭 위치 저장
- [ ] 테마 (다크모드, 투명도)
