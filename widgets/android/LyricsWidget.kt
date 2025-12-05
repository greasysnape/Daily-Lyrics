package com.example.dailylyrics

import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.widget.RemoteViews
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.net.URL

/**
 * Daily Lyrics 위젯 Provider
 */
class LyricsWidget : AppWidgetProvider() {

    // 위젯 설정 (간격)
    private val interval = "3h"  // 1h, 3h, 6h, 12h, 24h

    override fun onUpdate(
        context: Context,
        appWidgetManager: AppWidgetManager,
        appWidgetIds: IntArray
    ) {
        // 각 위젯 인스턴스에 대해 업데이트
        for (appWidgetId in appWidgetIds) {
            updateWidget(context, appWidgetManager, appWidgetId)
        }
    }

    /**
     * 위젯 업데이트
     */
    private fun updateWidget(
        context: Context,
        appWidgetManager: AppWidgetManager,
        appWidgetId: Int
    ) {
        CoroutineScope(Dispatchers.Main).launch {
            val views = RemoteViews(context.packageName, R.layout.widget_lyrics)

            // API에서 가사 가져오기
            val result = LyricsAPIService.getCurrentLyrics(interval)

            result.onSuccess { lyricsData ->
                // 성공: 가사 표시
                views.setTextViewText(
                    R.id.widget_lyrics_text,
                    lyricsData.lines.take(4).joinToString("\n")
                )
                views.setTextViewText(R.id.widget_title, lyricsData.title)
                views.setTextViewText(
                    R.id.widget_album,
                    "${lyricsData.album} (${lyricsData.year})"
                )

                // 앨범 커버 배경 로드
                val coverURL = lyricsData.getCoverImageURL()
                if (coverURL != null) {
                    loadAlbumCover(coverURL) { bitmap ->
                        if (bitmap != null) {
                            views.setImageViewBitmap(R.id.widget_background_image, bitmap)
                            views.setViewVisibility(R.id.widget_background_default, android.view.View.GONE)
                            views.setViewVisibility(R.id.widget_overlay, android.view.View.VISIBLE)
                        } else {
                            // 이미지 로드 실패 시 기본 배경 사용
                            views.setViewVisibility(R.id.widget_background_default, android.view.View.VISIBLE)
                            views.setViewVisibility(R.id.widget_overlay, android.view.View.GONE)
                        }
                        appWidgetManager.updateAppWidget(appWidgetId, views)
                    }
                } else {
                    // 앨범 커버 없을 경우 기본 배경
                    views.setViewVisibility(R.id.widget_background_default, android.view.View.VISIBLE)
                    views.setViewVisibility(R.id.widget_overlay, android.view.View.GONE)
                }

                // 에러 메시지 숨기기
                views.setViewVisibility(R.id.widget_error, android.view.View.GONE)
                views.setViewVisibility(R.id.widget_content, android.view.View.VISIBLE)
            }.onFailure { error ->
                // 실패: 에러 메시지 표시
                views.setViewVisibility(R.id.widget_content, android.view.View.GONE)
                views.setViewVisibility(R.id.widget_error, android.view.View.VISIBLE)
                views.setTextViewText(
                    R.id.widget_error_message,
                    "서버 연결 필요\n\nDaily Lyrics 서버를\nPC에서 실행해주세요"
                )
            }

            // 위젯 업데이트
            appWidgetManager.updateAppWidget(appWidgetId, views)
        }
    }

    override fun onEnabled(context: Context) {
        // 첫 위젯이 추가될 때
    }

    override fun onDisabled(context: Context) {
        // 마지막 위젯이 제거될 때
    }

    /**
     * 앨범 커버 이미지 로드
     */
    private fun loadAlbumCover(imageURL: String, callback: (Bitmap?) -> Unit) {
        CoroutineScope(Dispatchers.IO).launch {
            try {
                val url = URL(imageURL)
                val bitmap = BitmapFactory.decodeStream(url.openConnection().getInputStream())
                withContext(Dispatchers.Main) {
                    callback(bitmap)
                }
            } catch (e: Exception) {
                withContext(Dispatchers.Main) {
                    callback(null)
                }
            }
        }
    }
}
