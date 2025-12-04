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
    val interval: String? = null
)
