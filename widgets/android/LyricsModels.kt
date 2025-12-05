package com.example.dailylyrics

import kotlinx.serialization.Serializable

/**
 * API 응답 모델
 */
@Serializable
data class LyricsResponse(
    val success: Boolean,
    val data: LyricsData? = null,
    val error: String? = null
)

/**
 * 가사 데이터
 */
@Serializable
data class LyricsData(
    val lines: List<String>,
    val title: String,
    val album: String,
    val year: Int,
    val artist: String,
    val timestamp: String,
    val interval: String? = null,
    val albumFolder: String? = null
) {
    /**
     * 앨범 커버 URL 생성
     */
    fun getCoverImageURL(baseURL: String = "http://10.0.2.2:58384"): String? {
        if (albumFolder.isNullOrEmpty()) return null

        // URL 인코딩 (세미콜론 등 특수문자 처리)
        val encodedFilename = java.net.URLEncoder.encode("$albumFolder.webp", "UTF-8")
        return "$baseURL/covers/$encodedFilename"
    }
}
