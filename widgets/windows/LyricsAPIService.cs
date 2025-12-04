using System;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;

namespace DailyLyricsWidget
{
    /// <summary>
    /// API 통신 서비스
    /// </summary>
    public class LyricsAPIService
    {
        private static readonly HttpClient httpClient = new HttpClient();
        private const string BASE_URL = "http://localhost:58384";  // 로컬 서버 주소

        static LyricsAPIService()
        {
            httpClient.Timeout = TimeSpan.FromSeconds(5);
        }

        /// <summary>
        /// 현재 가사 가져오기
        /// </summary>
        public static async Task<LyricsData?> GetCurrentLyricsAsync(string interval = "24h")
        {
            try
            {
                var url = $"{BASE_URL}/current-lyric?interval={interval}";
                var response = await httpClient.GetStringAsync(url);

                var lyricsResponse = JsonSerializer.Deserialize<LyricsResponse>(response);

                if (lyricsResponse?.Success == true && lyricsResponse.Data != null)
                {
                    return lyricsResponse.Data;
                }

                return null;
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"API Error: {ex.Message}");
                return null;
            }
        }

        /// <summary>
        /// 랜덤 가사 가져오기
        /// </summary>
        public static async Task<LyricsData?> GetRandomLyricsAsync()
        {
            try
            {
                var url = $"{BASE_URL}/random-lyric";
                var response = await httpClient.GetStringAsync(url);

                var lyricsResponse = JsonSerializer.Deserialize<LyricsResponse>(response);

                if (lyricsResponse?.Success == true && lyricsResponse.Data != null)
                {
                    return lyricsResponse.Data;
                }

                return null;
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"API Error: {ex.Message}");
                return null;
            }
        }

        /// <summary>
        /// 서버 상태 확인
        /// </summary>
        public static async Task<bool> CheckHealthAsync()
        {
            try
            {
                var url = $"{BASE_URL}/health";
                var response = await httpClient.GetAsync(url);
                return response.IsSuccessStatusCode;
            }
            catch
            {
                return false;
            }
        }
    }
}
