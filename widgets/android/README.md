# Daily Lyrics Widget - Android

Android 홈 화면에 표시되는 태연 가사 위젯입니다.

## 요구사항

- Android 5.0 (API 21) 이상
- Android Studio (최신 버전 권장)
- PC와 Android 기기가 같은 Wi-Fi 네트워크에 연결되어 있어야 함
- Daily Lyrics API 서버가 PC에서 실행 중 (localhost:58384)

## 설치 방법

### 1. Android Studio 프로젝트 생성

1. Android Studio 실행
2. `File` > `New` > `New Project...`
3. `Empty Activity` 템플릿 선택
4. 프로젝트 정보 입력:
   - Name: `Daily Lyrics Widget`
   - Package name: `com.example.dailylyrics`
   - Language: `Kotlin`
   - Minimum SDK: API 21 (Android 5.0)
5. `Finish` 클릭

### 2. 의존성 추가

#### `build.gradle.kts` (Project level)

```kotlin
plugins {
    // ... 기존 설정
    kotlin("plugin.serialization") version "1.9.0" apply false
}
```

#### `build.gradle.kts` (Module: app)

파일 최상단의 plugins 블록에 추가:
```kotlin
plugins {
    // ... 기존 플러그인들
    kotlin("plugin.serialization")
}
```

dependencies 블록에 추가:
```kotlin
dependencies {
    // ... 기존 의존성들

    // Kotlin Coroutines
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")

    // Kotlin Serialization
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.0")
}
```

`Sync Now` 클릭하여 의존성 동기화

### 3. 파일 추가

#### A. Kotlin 파일 추가

`app/src/main/java/com/example/dailylyrics/` 폴더에 다음 파일 추가:
- `LyricsModels.kt`
- `LyricsAPIService.kt`
- `LyricsWidget.kt`

#### B. 레이아웃 파일 추가

`app/src/main/res/layout/` 폴더에 추가:
- `widget_lyrics.xml`

`app/src/main/res/drawable/` 폴더에 추가:
- `widget_background.xml`

`app/src/main/res/xml/` 폴더 생성 후 추가:
- `widget_info.xml`

### 4. AndroidManifest.xml 수정

`app/src/main/AndroidManifest.xml` 파일 수정:

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <!-- 권한 추가 -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:usesCleartextTraffic="true"
        ...>

        <!-- 기존 Activity -->
        <activity
            android:name=".MainActivity"
            ...>
        </activity>

        <!-- 위젯 Provider 추가 -->
        <receiver
            android:name=".LyricsWidget"
            android:exported="true">
            <intent-filter>
                <action android:name="android.appwidget.action.APPWIDGET_UPDATE" />
            </intent-filter>
            <meta-data
                android:name="android.appwidget.provider"
                android:resource="@xml/widget_info" />
        </receiver>

    </application>

</manifest>
```

### 5. 문자열 리소스 추가

`app/src/main/res/values/strings.xml`에 추가:

```xml
<resources>
    <string name="app_name">Daily Lyrics</string>
    <string name="widget_description">태연 가사를 홈 화면에 표시합니다</string>
</resources>
```

### 6. 네트워크 설정

#### A. PC의 IP 주소 확인

**Mac/Linux:**
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

**Windows:**
```cmd
ipconfig
```

예시: `192.168.0.10`

#### B. LyricsAPIService.kt 수정

```kotlin
// 에뮬레이터 사용 시
private const val BASE_URL = "http://10.0.2.2:58384"

// 실제 기기 사용 시 (PC의 IP 주소로 변경)
private const val BASE_URL = "http://192.168.0.10:58384"
```

### 7. 빌드 및 실행

1. Android 기기를 USB로 연결하거나 에뮬레이터 시작
2. `Run` > `Run 'app'` (또는 Shift+F10)
3. 앱이 설치됩니다

### 8. 위젯 추가

1. 홈 화면 빈 곳을 길게 누름
2. `위젯` 메뉴 선택
3. `Daily Lyrics` 위젯 찾기
4. 위젯을 홈 화면에 드래그

## 네트워크 설정 상세

### 에뮬레이터 vs 실제 기기

#### 에뮬레이터:
- `10.0.2.2`는 호스트 PC의 localhost를 가리킴
- PC의 IP 주소 불필요

#### 실제 기기:
- PC의 실제 IP 주소 필요
- PC와 같은 Wi-Fi 네트워크에 연결되어 있어야 함

### 연결 테스트

**Chrome 브라우저에서:**
1. Chrome 열기
2. 주소창에 `http://[PC-IP]:58384/health` 입력
3. JSON 응답이 나오면 정상

**예시:**
```
http://192.168.0.10:58384/health
```

응답:
```json
{
  "status": "healthy",
  "timestamp": "2025-12-04T...",
  "chunks_count": 784
}
```

### 방화벽 설정

PC의 방화벽에서 포트 58384 접근 허용 필요:

**Mac:**
- 시스템 설정 > 네트워크 > 방화벽
- Python 허용

**Windows:**
- 제어판 > Windows Defender 방화벽
- 인바운드 규칙에서 포트 58384 허용

## 설정

### 가사 변경 주기 변경

`LyricsWidget.kt` 파일에서 `interval` 값 변경:

```kotlin
private val interval = "3h"  // 1h, 3h, 6h, 12h, 24h
```

변경 후 앱 재빌드 및 위젯 재추가

### 위젯 업데이트 주기

`widget_info.xml`의 `updatePeriodMillis` 값:

```xml
android:updatePeriodMillis="10800000"
```

- `3600000`: 1시간 (1h)
- `10800000`: 3시간 (3h) - 기본값
- `21600000`: 6시간 (6h)
- `43200000`: 12시간 (12h)
- `86400000`: 24시간 (24h)

**주의:** 안드로이드는 최소 30분(1800000ms) 미만은 설정 불가

## 트러블슈팅

### "서버 연결 필요" 표시

1. **PC의 API 서버 확인**:
   ```bash
   curl http://localhost:58384/health
   ```

2. **Android에서 PC로 연결 테스트**:
   - Chrome 열기
   - `http://[PC-IP]:58384/health` 접속
   - JSON 응답 확인

3. **같은 Wi-Fi 네트워크 확인**:
   - PC와 Android 기기가 같은 네트워크에 연결되어 있는지 확인

4. **LyricsAPIService.kt의 BASE_URL 확인**:
   - 에뮬레이터: `10.0.2.2`
   - 실제 기기: PC의 IP 주소

### 위젯이 업데이트되지 않음

- 위젯 길게 누르기 > 제거
- 다시 위젯 추가
- 또는 기기 재시작

### 빌드 에러

- `Sync Project with Gradle Files` 실행
- `Build` > `Clean Project` > `Rebuild Project`
- Android Studio 재시작

### Cleartext HTTP 에러

AndroidManifest.xml에서 확인:
```xml
android:usesCleartextTraffic="true"
```

## 프로젝트 구조

```
app/
├── src/main/
│   ├── java/com/example/dailylyrics/
│   │   ├── MainActivity.kt              # 메인 액티비티 (설정 등)
│   │   ├── LyricsModels.kt              # 데이터 모델
│   │   ├── LyricsAPIService.kt          # API 통신
│   │   └── LyricsWidget.kt              # 위젯 Provider
│   └── res/
│       ├── layout/
│       │   └── widget_lyrics.xml        # 위젯 레이아웃
│       ├── drawable/
│       │   └── widget_background.xml    # 위젯 배경
│       └── xml/
│           └── widget_info.xml          # 위젯 메타데이터
└── AndroidManifest.xml
```

## 개선 사항

- [ ] 위젯 크기별 레이아웃 최적화 (2x2, 3x3, 4x4)
- [ ] 다크모드 지원
- [ ] 위젯 설정 Activity (간격 설정 UI)
- [ ] 오프라인 모드 (캐시 사용)
- [ ] 위젯 터치 시 새로고침

## 참고 사항

- Android 위젯은 홈 화면에만 추가 가능 (배경화면 아님)
- 위젯은 백그라운드에서 주기적으로 자동 업데이트
- 배터리 절약을 위해 업데이트 주기는 최소 30분 이상 권장
