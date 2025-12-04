//
//  LyricsAPIService.swift
//  Daily Lyrics Widget - macOS
//
//  API 통신 로직
//

import Foundation

class LyricsAPIService {
    static let shared = LyricsAPIService()

    // API 베이스 URL (로컬호스트)
    private let baseURL = "http://localhost:58384"

    private init() {}

    /// 현재 가사 가져오기
    func getCurrentLyrics(interval: String = "24h") async -> Result<LyricsData, Error> {
        let urlString = "\(baseURL)/current-lyric?interval=\(interval)"

        guard let url = URL(string: urlString) else {
            return .failure(APIError.invalidURL)
        }

        do {
            let (data, response) = try await URLSession.shared.data(from: url)

            guard let httpResponse = response as? HTTPURLResponse,
                  httpResponse.statusCode == 200 else {
                return .failure(APIError.serverError)
            }

            let decoder = JSONDecoder()
            let lyricsResponse = try decoder.decode(LyricsResponse.self, from: data)

            if lyricsResponse.success, let lyricsData = lyricsResponse.data {
                return .success(lyricsData)
            } else {
                return .failure(APIError.noData)
            }
        } catch {
            return .failure(error)
        }
    }

    /// 랜덤 가사 가져오기
    func getRandomLyrics() async -> Result<LyricsData, Error> {
        let urlString = "\(baseURL)/random-lyric"

        guard let url = URL(string: urlString) else {
            return .failure(APIError.invalidURL)
        }

        do {
            let (data, response) = try await URLSession.shared.data(from: url)

            guard let httpResponse = response as? HTTPURLResponse,
                  httpResponse.statusCode == 200 else {
                return .failure(APIError.serverError)
            }

            let decoder = JSONDecoder()
            let lyricsResponse = try decoder.decode(LyricsResponse.self, from: data)

            if lyricsResponse.success, let lyricsData = lyricsResponse.data {
                return .success(lyricsData)
            } else {
                return .failure(APIError.noData)
            }
        } catch {
            return .failure(error)
        }
    }

    /// 서버 상태 확인
    func checkHealth() async -> Bool {
        let urlString = "\(baseURL)/health"

        guard let url = URL(string: urlString) else {
            return false
        }

        do {
            let (_, response) = try await URLSession.shared.data(from: url)
            guard let httpResponse = response as? HTTPURLResponse else {
                return false
            }
            return httpResponse.statusCode == 200
        } catch {
            return false
        }
    }
}

/// API 에러 타입
enum APIError: LocalizedError {
    case invalidURL
    case serverError
    case noData
    case networkError

    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "잘못된 URL"
        case .serverError:
            return "서버 오류"
        case .noData:
            return "데이터 없음"
        case .networkError:
            return "네트워크 오류"
        }
    }
}
