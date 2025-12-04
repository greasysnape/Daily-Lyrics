//
//  DailyLyricsWidget.swift
//  Daily Lyrics Widget - iOS
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
            errorMessage: nil
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
            return LyricsEntry(
                date: Date(),
                lyrics: lyricsData,
                errorMessage: nil
            )
        case .failure(let error):
            return LyricsEntry(
                date: Date(),
                lyrics: nil,
                errorMessage: error.localizedDescription
            )
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
    @Environment(\.widgetFamily) var family

    var body: some View {
        if entry.isError {
            // 에러 상태
            ErrorView(message: entry.errorMessage ?? "알 수 없는 오류", family: family)
        } else if let lyrics = entry.lyrics {
            // 정상 상태
            LyricsView(lyrics: lyrics, family: family)
        }
    }
}

/// 가사 뷰
struct LyricsView: View {
    let lyrics: LyricsData
    let family: WidgetFamily

    var body: some View {
        ZStack {
            // 앨범 커버 배경
            if let coverURL = lyrics.coverImageURL {
                AsyncImage(url: coverURL) { phase in
                    switch phase {
                    case .success(let image):
                        image
                            .resizable()
                            .aspectRatio(contentMode: .fill)
                    case .failure(_), .empty:
                        // 이미지 로드 실패 시 기본 배경
                        LinearGradient(
                            colors: [Color(white: 0.95), Color(white: 0.98)],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    @unknown default:
                        LinearGradient(
                            colors: [Color(white: 0.95), Color(white: 0.98)],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    }
                }
            } else {
                // 앨범 커버가 없을 경우 기본 배경
                LinearGradient(
                    colors: [Color(white: 0.95), Color(white: 0.98)],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
            }

            // 텍스트 가독성을 위한 어두운 오버레이
            if lyrics.coverImageURL != nil {
                LinearGradient(
                    colors: [
                        Color.black.opacity(0.4),
                        Color.black.opacity(0.3)
                    ],
                    startPoint: .top,
                    endPoint: .bottom
                )
            }

            VStack(alignment: .leading, spacing: 12) {
                // 가사 라인들
                VStack(alignment: .leading, spacing: 6) {
                    ForEach(displayLines, id: \.self) { line in
                        Text(line)
                            .font(lyricsFont)
                            .fontWeight(.medium)
                            .foregroundColor(lyrics.coverImageURL != nil ? .white : .primary)
                            .shadow(color: .black.opacity(lyrics.coverImageURL != nil ? 0.3 : 0), radius: 2, x: 0, y: 1)
                            .lineLimit(1)
                    }
                }

                Spacer()

                // 곡 정보
                VStack(alignment: .leading, spacing: 2) {
                    Text(lyrics.title)
                        .font(.caption)
                        .fontWeight(.semibold)
                        .foregroundColor(lyrics.coverImageURL != nil ? .white.opacity(0.9) : .secondary)
                        .shadow(color: .black.opacity(lyrics.coverImageURL != nil ? 0.3 : 0), radius: 1, x: 0, y: 1)
                        .lineLimit(1)

                    Text("\(lyrics.album) (\(lyrics.year))")
                        .font(.caption2)
                        .foregroundColor(lyrics.coverImageURL != nil ? .white.opacity(0.8) : .secondary.opacity(0.7))
                        .shadow(color: .black.opacity(lyrics.coverImageURL != nil ? 0.3 : 0), radius: 1, x: 0, y: 1)
                        .lineLimit(1)
                }
            }
            .padding()
        }
    }

    // 위젯 크기에 따라 표시할 라인 수 조정
    private var displayLines: [String] {
        switch family {
        case .systemMedium:
            return Array(lyrics.lines.prefix(3))
        case .systemLarge:
            return Array(lyrics.lines.prefix(5))
        default:
            return Array(lyrics.lines.prefix(3))
        }
    }

    // 위젯 크기에 따른 폰트
    private var lyricsFont: Font {
        return .body
    }
}

/// 에러 뷰
struct ErrorView: View {
    let message: String
    let family: WidgetFamily

    var body: some View {
        ZStack {
            Color(white: 0.95)

            VStack(spacing: 8) {
                Image(systemName: "wifi.slash")
                    .font(.title2)
                    .foregroundColor(.orange)

                Text("서버 연결 필요")
                    .font(.caption)
                    .fontWeight(.semibold)

                Text("Daily Lyrics 서버를\n실행해주세요")
                    .font(.caption2)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
                    .lineLimit(3)
            }
            .padding()
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
        .description("태연 가사를 홈 화면에 표시합니다")
        .supportedFamilies([.systemMedium, .systemLarge])
    }
}

/// 프리뷰
struct DailyLyricsWidget_Previews: PreviewProvider {
    static var previews: some View {
        Group {
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
                errorMessage: nil
            ))
            .previewContext(WidgetPreviewContext(family: .systemMedium))
            .previewDisplayName("Medium")

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
                errorMessage: nil
            ))
            .previewContext(WidgetPreviewContext(family: .systemLarge))
            .previewDisplayName("Large")
        }
    }
}
