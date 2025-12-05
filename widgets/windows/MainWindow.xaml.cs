using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Input;
using Microsoft.UI.Xaml.Media;
using Microsoft.UI.Xaml.Media.Imaging;
using System;
using System.Linq;
using System.Threading.Tasks;
using Windows.System;

namespace DailyLyricsWidget
{
    /// <summary>
    /// Daily Lyrics 위젯 메인 윈도우
    /// </summary>
    public sealed partial class MainWindow : Window
    {
        private DispatcherTimer? updateTimer;
        private const string DEFAULT_INTERVAL = "3h";  // 1h, 3h, 6h, 12h, 24h

        public MainWindow()
        {
            this.InitializeComponent();

            // 초기 위치 설정 (화면 오른쪽 하단)
            SetInitialPosition();

            // 드래그 가능하도록 설정
            this.SetupDragMove();

            // 초기 데이터 로드
            _ = LoadLyricsAsync();

            // 자동 업데이트 타이머 시작
            StartAutoUpdate();
        }

        /// <summary>
        /// 초기 위치 설정
        /// </summary>
        private void SetInitialPosition()
        {
            var displayArea = Windows.Graphics.DisplayInformation.GetForCurrentView().ScreenHeightInRawPixels;
            // 화면 오른쪽 하단에 배치
            var appWindow = this.AppWindow;
            if (appWindow != null)
            {
                appWindow.Move(new Windows.Graphics.PointInt32(
                    (int)(displayArea.Width - this.Width - 20),
                    (int)(displayArea.Height - this.Height - 100)
                ));
            }
        }

        /// <summary>
        /// 드래그로 이동 가능하도록 설정
        /// </summary>
        private void SetupDragMove()
        {
            this.PointerPressed += (sender, e) =>
            {
                if (e.GetCurrentPoint(this).Properties.IsLeftButtonPressed)
                {
                    this.AppWindow?.MoveAndResize(this.AppWindow.Position, this.AppWindow.Size);
                }
            };
        }

        /// <summary>
        /// 가사 데이터 로드
        /// </summary>
        private async Task LoadLyricsAsync()
        {
            try
            {
                var lyrics = await LyricsAPIService.GetCurrentLyricsAsync(DEFAULT_INTERVAL);

                if (lyrics != null)
                {
                    // 성공: 가사 표시
                    this.DispatcherQueue.TryEnqueue(() =>
                    {
                        LyricsText.Text = string.Join("\n", lyrics.Lines.Take(4));
                        TitleText.Text = lyrics.Title;
                        AlbumText.Text = $"{lyrics.Album} ({lyrics.Year})";

                        // 앨범 커버 배경 로드
                        var coverURL = lyrics.GetCoverImageURL();
                        if (!string.IsNullOrEmpty(coverURL))
                        {
                            LoadAlbumCover(coverURL);
                        }
                        else
                        {
                            // 앨범 커버 없을 경우 기본 배경 및 검정색 텍스트
                            SetDefaultBackground();
                        }

                        ContentPanel.Visibility = Visibility.Visible;
                        ErrorPanel.Visibility = Visibility.Collapsed;
                    });
                }
                else
                {
                    // 실패: 에러 표시
                    ShowError("서버에 연결할 수 없습니다");
                }
            }
            catch (Exception ex)
            {
                ShowError($"오류: {ex.Message}");
            }
        }

        /// <summary>
        /// 에러 메시지 표시
        /// </summary>
        private void ShowError(string message)
        {
            this.DispatcherQueue.TryEnqueue(() =>
            {
                ErrorMessage.Text = message;
                ContentPanel.Visibility = Visibility.Collapsed;
                ErrorPanel.Visibility = Visibility.Visible;
            });
        }

        /// <summary>
        /// 자동 업데이트 시작
        /// </summary>
        private void StartAutoUpdate()
        {
            updateTimer = new DispatcherTimer();

            // 3시간마다 업데이트
            updateTimer.Interval = TimeSpan.FromHours(3);
            updateTimer.Tick += async (sender, e) => await LoadLyricsAsync();
            updateTimer.Start();
        }

        /// <summary>
        /// 새로고침 메뉴
        /// </summary>
        private async void Refresh_Click(object sender, RoutedEventArgs e)
        {
            await LoadLyricsAsync();
        }

        /// <summary>
        /// 설정 메뉴
        /// </summary>
        private async void Settings_Click(object sender, RoutedEventArgs e)
        {
            var dialog = new ContentDialog
            {
                Title = "설정",
                Content = "가사 변경 주기 및 기타 설정",
                CloseButtonText = "닫기",
                XamlRoot = this.Content.XamlRoot
            };

            await dialog.ShowAsync();
        }

        /// <summary>
        /// 종료 메뉴
        /// </summary>
        private void Exit_Click(object sender, RoutedEventArgs e)
        {
            updateTimer?.Stop();
            this.Close();
            Application.Current.Exit();
        }

        /// <summary>
        /// 앨범 커버 배경 이미지 로드
        /// </summary>
        private void LoadAlbumCover(string imageURL)
        {
            try
            {
                var bitmap = new BitmapImage(new Uri(imageURL));
                BackgroundImage.ImageSource = bitmap;
                BackgroundImage.Opacity = 1.0;
                DarkOverlay.Opacity = 1.0;

                // 흰색 텍스트로 변경
                LyricsText.Foreground = new SolidColorBrush(Windows.UI.Color.FromArgb(255, 255, 255, 255));
                TitleText.Foreground = new SolidColorBrush(Windows.UI.Color.FromArgb(230, 255, 255, 255));
                AlbumText.Foreground = new SolidColorBrush(Windows.UI.Color.FromArgb(204, 255, 255, 255));
            }
            catch
            {
                // 이미지 로드 실패 시 기본 배경 사용
                SetDefaultBackground();
            }
        }

        /// <summary>
        /// 기본 배경 설정 (앨범 커버 없을 때)
        /// </summary>
        private void SetDefaultBackground()
        {
            BackgroundImage.Opacity = 0;
            DarkOverlay.Opacity = 0;

            // 검정색 텍스트로 변경
            LyricsText.Foreground = new SolidColorBrush(Windows.UI.Color.FromArgb(255, 0, 0, 0));
            TitleText.Foreground = new SolidColorBrush(Windows.UI.Color.FromArgb(255, 102, 102, 102));
            AlbumText.Foreground = new SolidColorBrush(Windows.UI.Color.FromArgb(255, 153, 153, 153));
        }
    }
}
