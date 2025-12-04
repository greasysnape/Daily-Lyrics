package com.example.dailylyrics

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.serialization.json.Json
import java.net.HttpURLConnection
import java.net.URL

/**
 * API 통신 서비스
 */
class LyricsAPIService {
    companion object {
        // API 베이스 URL
        // 실제 기기: PC의 IP 주소로 변경 필요 (예: "http://192.168.0.10:58384")
        // 에뮬레이터: "http://10.0.2.2:58384" 사용 (10.0.2.2는 호스트 PC를 가리킴)
        private const val BASE_URL = "http://10.0.2.2:58384"

        private val json = Json {
            ignoreUnknownKeys = true
            isLenient = true
        }

        /**
         * 현재 가사 가져오기
         */
        suspend fun getCurrentLyrics(interval: String = "24h"): Result<LyricsData> {
            return withContext(Dispatchers.IO) {
                try {
                    val url = URL("$BASE_URL/current-lyric?interval=$interval")
                    val connection = url.openConnection() as HttpURLConnection
                    connection.requestMethod = "GET"
                    connection.connectTimeout = 5000
                    connection.readTimeout = 5000

                    if (connection.responseCode == HttpURLConnection.HTTP_OK) {
                        val response = connection.inputStream.bufferedReader().use { it.readText() }
                        val lyricsResponse = json.decodeFromString<LyricsResponse>(response)

                        if (lyricsResponse.success && lyricsResponse.data != null) {
                            Result.success(lyricsResponse.data)
                        } else {
                            Result.failure(Exception(lyricsResponse.error ?: "No data"))
                        }
                    } else {
                        Result.failure(Exception("Server error: ${connection.responseCode}"))
                    }
                } catch (e: Exception) {
                    Result.failure(e)
                }
            }
        }

        /**
         * 랜덤 가사 가져오기
         */
        suspend fun getRandomLyrics(): Result<LyricsData> {
            return withContext(Dispatchers.IO) {
                try {
                    val url = URL("$BASE_URL/random-lyric")
                    val connection = url.openConnection() as HttpURLConnection
                    connection.requestMethod = "GET"
                    connection.connectTimeout = 5000
                    connection.readTimeout = 5000

                    if (connection.responseCode == HttpURLConnection.HTTP_OK) {
                        val response = connection.inputStream.bufferedReader().use { it.readText() }
                        val lyricsResponse = json.decodeFromString<LyricsResponse>(response)

                        if (lyricsResponse.success && lyricsResponse.data != null) {
                            Result.success(lyricsResponse.data)
                        } else {
                            Result.failure(Exception(lyricsResponse.error ?: "No data"))
                        }
                    } else {
                        Result.failure(Exception("Server error: ${connection.responseCode}"))
                    }
                } catch (e: Exception) {
                    Result.failure(e)
                }
            }
        }

        /**
         * 서버 상태 확인
         */
        suspend fun checkHealth(): Boolean {
            return withContext(Dispatchers.IO) {
                try {
                    val url = URL("$BASE_URL/health")
                    val connection = url.openConnection() as HttpURLConnection
                    connection.requestMethod = "GET"
                    connection.connectTimeout = 3000
                    connection.readTimeout = 3000

                    connection.responseCode == HttpURLConnection.HTTP_OK
                } catch (e: Exception) {
                    false
                }
            }
        }
    }
}
