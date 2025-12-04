//
//  LyricsModels.swift
//  Daily Lyrics Widget - macOS
//
//  데이터 모델 정의
//

import Foundation

/// API 응답 모델
struct LyricsResponse: Codable {
    let success: Bool
    let data: LyricsData?
    let error: String?
}

/// 가사 데이터
struct LyricsData: Codable {
    let lines: [String]
    let title: String
    let album: String
    let year: Int
    let artist: String
    let timestamp: String
    let interval: String?
    let albumFolder: String?

    /// 앨범 커버 URL 생성
    var coverImageURL: URL? {
        guard let albumFolder = albumFolder, !albumFolder.isEmpty else {
            return nil
        }

        // URL 인코딩 (세미콜론 등 특수문자 처리)
        let filename = "\(albumFolder).webp"
        guard let encodedFilename = filename.addingPercentEncoding(withAllowedCharacters: .urlPathAllowed) else {
            return nil
        }

        let urlString = "http://127.0.0.1:58384/covers/\(encodedFilename)"
        return URL(string: urlString)
    }
}

/// 위젯에 표시할 엔트리
struct LyricsEntry: TimelineEntry {
    let date: Date
    let lyrics: LyricsData?
    let errorMessage: String?

    var isError: Bool {
        lyrics == nil
    }
}
