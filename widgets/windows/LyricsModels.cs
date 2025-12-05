using System.Text.Json.Serialization;

namespace DailyLyricsWidget
{
    /// <summary>
    /// API 응답 모델
    /// </summary>
    public class LyricsResponse
    {
        [JsonPropertyName("success")]
        public bool Success { get; set; }

        [JsonPropertyName("data")]
        public LyricsData? Data { get; set; }

        [JsonPropertyName("error")]
        public string? Error { get; set; }
    }

    /// <summary>
    /// 가사 데이터
    /// </summary>
    public class LyricsData
    {
        [JsonPropertyName("lines")]
        public List<string> Lines { get; set; } = new();

        [JsonPropertyName("title")]
        public string Title { get; set; } = string.Empty;

        [JsonPropertyName("album")]
        public string Album { get; set; } = string.Empty;

        [JsonPropertyName("year")]
        public int Year { get; set; }

        [JsonPropertyName("artist")]
        public string Artist { get; set; } = string.Empty;

        [JsonPropertyName("timestamp")]
        public string Timestamp { get; set; } = string.Empty;

        [JsonPropertyName("interval")]
        public string? Interval { get; set; }

        [JsonPropertyName("albumFolder")]
        public string? AlbumFolder { get; set; }

        /// <summary>
        /// 앨범 커버 URL 생성
        /// </summary>
        public string? GetCoverImageURL(string baseURL = "http://127.0.0.1:58384")
        {
            if (string.IsNullOrEmpty(AlbumFolder))
                return null;

            // URL 인코딩 (세미콜론 등 특수문자 처리)
            var encodedFilename = Uri.EscapeDataString($"{AlbumFolder}.webp");
            return $"{baseURL}/covers/{encodedFilename}";
        }
    }
}
