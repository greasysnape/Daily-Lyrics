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
