//
//  DailyLyricsWidget.swift
//  Daily Lyrics Widget - macOS
//
//  위젯 메인 구현
//

import WidgetKit
import SwiftUI

/// 위젯 Timeline Provider
struct LyricsProvider: TimelineProvider {
    // 위젯 설정 값 (간격 설정)
    private let interval = "3h"  // 1h, 3h, 6h, 12h, 24h 중 선택

    // 플레이스홀더 (위젯 갤러리에서 표시)
    func placeholder(in context: Context) -> LyricsEntry {
        LyricsEntry(
            date: Date(),
            lyrics: LyricsData(
                lines: ["익숙함에 수줍어", "네게 하지 못한 말", "노랫말에 가득 담아"],
                title: "Playlist",
                album: "What Do I Call You",
                year: 2020,
                artist: "태연 (TAEYEON)",
                timestamp: ISO8601DateFormatter().string(from: Date()),
                interval: "3h",
                albumFolder: "013_What Do I Call You"
            ),
            errorMessage: nil,
            coverImageData: nil
        )
    }

    // 스냅샷 (위젯 미리보기)
    func getSnapshot(in context: Context, completion: @escaping (LyricsEntry) -> Void) {
        Task {
            let entry = await fetchLyrics()
            completion(entry)
        }
    }

    // 타임라인 (위젯 업데이트 스케줄)
    func getTimeline(in context: Context, completion: @escaping (Timeline<LyricsEntry>) -> Void) {
        Task {
            let entry = await fetchLyrics()

            // 다음 업데이트 시간 계산 (간격에 따라)
            let nextUpdate = calculateNextUpdate(for: interval)
            let timeline = Timeline(entries: [entry], policy: .after(nextUpdate))

            completion(timeline)
        }
    }

    // API에서 가사 가져오기
    private func fetchLyrics() async -> LyricsEntry {
        let result = await LyricsAPIService.shared.getCurrentLyrics(interval: interval)

        switch result {
        case .success(let lyricsData):
            // 앨범 커버 이미지 다운로드
            let coverImageData = await downloadCoverImage(from: lyricsData.coverImageURL)

            return LyricsEntry(
                date: Date(),
                lyrics: lyricsData,
                errorMessage: nil,
                coverImageData: coverImageData
            )
        case .failure(let error):
            return LyricsEntry(
                date: Date(),
                lyrics: nil,
                errorMessage: error.localizedDescription,
                coverImageData: nil
            )
        }
    }

    // 앨범 커버 이미지 다운로드
    private func downloadCoverImage(from url: URL?) async -> Data? {
        guard let url = url else { return nil }

        do {
            let (data, _) = try await URLSession.shared.data(from: url)
            return data
        } catch {
            print("앨범 커버 다운로드 실패: \(error)")
            return nil
        }
    }

    // 다음 업데이트 시간 계산
    private func calculateNextUpdate(for interval: String) -> Date {
        let calendar = Calendar.current
        let now = Date()

        switch interval {
        case "1h":
            return calendar.date(byAdding: .hour, value: 1, to: now) ?? now
        case "3h":
            return calendar.date(byAdding: .hour, value: 3, to: now) ?? now
        case "6h":
            return calendar.date(byAdding: .hour, value: 6, to: now) ?? now
        case "12h":
            return calendar.date(byAdding: .hour, value: 12, to: now) ?? now
        case "24h":
            return calendar.date(byAdding: .day, value: 1, to: now) ?? now
        default:
            return calendar.date(byAdding: .day, value: 1, to: now) ?? now
        }
    }
}

/// 위젯 UI
struct DailyLyricsWidgetView: View {
    let entry: LyricsEntry

    var body: some View {
        // 뷰 계층 구조에 따라 배경 적용
        Group {
            if entry.isError {
                // 에러 상태
                ErrorView(message: entry.errorMessage ?? "알 수 없는 오류")
            } else if let lyrics = entry.lyrics {
                // 정상 상태
                LyricsView(lyrics: lyrics, coverImageData: entry.coverImageData)
            } else {
                // 로딩 중이거나 데이터 없음
                Text("가사를 불러오는 중...")
            }
        }
    }
}

/// 가사 뷰
struct LyricsView: View {
    let lyrics: LyricsData
    let coverImageData: Data?

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            // 가사 라인들
            VStack(alignment: .leading, spacing: 6) {
                ForEach(lyrics.lines, id: \.self) { line in
                    Text(line)
                        .font(.body)
                        .fontWeight(.medium)
                        .foregroundColor(.white)
                        .shadow(color: .black.opacity(0.3), radius: 2, x: 0, y: 1)
                }
            }

            Spacer()

            // 곡 정보
            VStack(alignment: .leading, spacing: 2) {
                Text(lyrics.title)
                    .font(.caption)
                    .fontWeight(.semibold)
                    .foregroundColor(.white.opacity(0.9))
                    .shadow(color: .black.opacity(0.3), radius: 1, x: 0, y: 1)

                Text("\(lyrics.album) (\(String(lyrics.year)))")
                    .font(.caption2)
                    .foregroundColor(.white.opacity(0.8))
                    .shadow(color: .black.opacity(0.3), radius: 1, x: 0, y: 1)
            }
        }
        .padding()
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .topLeading)
        // macOS 14 Sonoma 대응: 위젯 배경 설정
        .containerBackground(for: .widget) {
            if let imageData = coverImageData,
               let nsImage = NSImage(data: imageData) {
                // 앨범 커버 배경
                GeometryReader { geometry in
                    Image(nsImage: nsImage)
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                        .frame(width: geometry.size.width, height: geometry.size.height)
                        .clipped()
                        .overlay(
                            LinearGradient(
                                colors: [
                                    Color.black.opacity(0.4),
                                    Color.black.opacity(0.3)
                                ],
                                startPoint: .top,
                                endPoint: .bottom
                            )
                        )
                }
            } else {
                // 앨범 커버가 없을 경우 기본 배경
                Color.white
            }
        }
    }
}

/// 에러 뷰
struct ErrorView: View {
    let message: String

    var body: some View {
        VStack(spacing: 8) {
            Image(systemName: "exclamationmark.triangle")
                .font(.title)
                .foregroundColor(.orange)

            Text("연결 오류")
                .font(.headline)

            Text(message)
                .font(.caption)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)

            Text("서버가 실행 중인지 확인하세요")
                .font(.caption2)
                .foregroundColor(.secondary)
        }
        .padding()
        // 에러 화면에도 배경 설정
        .containerBackground(for: .widget) {
            Color(nsColor: .windowBackgroundColor) // 시스템 기본 배경색
        }
    }
}

/// 위젯 설정
@main
struct DailyLyricsWidget: Widget {
    let kind: String = "DailyLyricsWidget"

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: LyricsProvider()) { entry in
            DailyLyricsWidgetView(entry: entry)
        }
        .configurationDisplayName("Daily Lyrics")
        .description("매일 다른 태연 가사를 배경화면에 표시합니다")
        .supportedFamilies([.systemMedium, .systemLarge])
        // 콘텐츠 마진 비활성화 (배경 꽉 차게)
        .contentMarginsDisabled()
    }
}

/// 프리뷰
struct DailyLyricsWidget_Previews: PreviewProvider {
    static var previews: some View {
        DailyLyricsWidgetView(entry: LyricsEntry(
            date: Date(),
            lyrics: LyricsData(
                lines: ["익숙함에 수줍어", "네게 하지 못한 말", "노랫말에 가득 담아"],
                title: "Playlist",
                album: "What Do I Call You",
                year: 2020,
                artist: "태연 (TAEYEON)",
                timestamp: ISO8601DateFormatter().string(from: Date()),
                interval: "3h",
                albumFolder: "013_What Do I Call You"
            ),
            errorMessage: nil,
            coverImageData: nil
        ))
        .previewContext(WidgetPreviewContext(family: .systemMedium))
    }
}
