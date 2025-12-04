#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Daily Lyrics - 일일 랜덤 가사
CLI 인터페이스
"""

import sys
import argparse
from datetime import datetime, date
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.lyrics_database import LyricsDatabase
from src.daily_selector import get_daily_lyric, get_random_lyric, parse_date


def format_lyric_output(chunk: dict, show_date: str = None) -> str:
    """
    가사 청크를 보기 좋게 포맷팅

    Args:
        chunk: 가사 청크 딕셔너리
        show_date: 표시할 날짜 문자열 (선택)

    Returns:
        포맷된 문자열
    """
    output = []
    output.append("")
    output.append("=" * 60)

    # 날짜 표시 (있으면)
    if show_date:
        output.append(f"📅 {show_date}")
        output.append("-" * 60)

    # 곡 정보
    output.append(f"🎵 {chunk['title']}")
    output.append(f"💿 {chunk['album']} ({chunk['year']})")
    output.append("=" * 60)
    output.append("")

    # 가사 라인들
    for line in chunk['lines']:
        output.append(f"    {line}")

    output.append("")
    output.append("=" * 60)
    output.append("")

    return "\n".join(output)


def show_stats(db: LyricsDatabase) -> None:
    """
    데이터베이스 통계를 표시

    Args:
        db: LyricsDatabase 인스턴스
    """
    print("\n" + "=" * 60)
    print("📊 가사 데이터베이스 통계")
    print("=" * 60)
    print(f"\n총 가사 청크: {db.get_chunk_count()}개")
    print(f"총 앨범: {db.albums_count}개")
    print(f"총 트랙: {db.tracks_count}개\n")

    albums_info = db.get_albums_info()

    if albums_info:
        print("앨범별 상세:")
        print("-" * 60)

        # 연도순 정렬
        sorted_albums = sorted(albums_info.items(), key=lambda x: x[1]['year'])

        for album, info in sorted_albums:
            print(f"\n  📀 {album} ({info['year']})")
            print(f"     트랙 수: {info['track_count']}개")
            print(f"     가사 청크: {info['chunk_count']}개")

    print("\n" + "=" * 60 + "\n")


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description='태연의 일일 랜덤 가사를 표시합니다.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python cli.py                    # 오늘의 가사
  python cli.py --random           # 완전 랜덤 가사
  python cli.py --date 2025-12-01  # 특정 날짜의 가사
  python cli.py --stats            # 통계 보기
        """
    )

    parser.add_argument(
        '--random',
        action='store_true',
        help='완전 랜덤 가사 선택 (날짜 무관)'
    )

    parser.add_argument(
        '--date',
        type=str,
        metavar='YYYY-MM-DD',
        help='특정 날짜의 가사 표시 (형식: YYYY-MM-DD)'
    )

    parser.add_argument(
        '--stats',
        action='store_true',
        help='가사 데이터베이스 통계 표시'
    )

    args = parser.parse_args()

    # 가사 데이터베이스 로드
    #print("\n📚 가사 데이터베이스 로딩 중...")
    db = LyricsDatabase()

    # 통계 표시
    if args.stats:
        show_stats(db)
        return 0

    # 데이터가 없으면 종료
    if db.is_empty():
        print("\n⚠️  가사 데이터가 없습니다.")
        print("⚠️ data/ 폴더에 앨범과 트랙 JSON 파일을 추가해주세요.\n")
        return 1

    # 가사 선택
    chunk = None
    display_date = None

    if args.random:
        chunk = get_random_lyric(db.get_all_chunks())
        print("\n🎲 완전 랜덤 가사:")

    elif args.date:
        target_date = parse_date(args.date)
        if target_date is None:
            print(f"\n❌ 잘못된 날짜 형식: {args.date}")
            print("   올바른 형식: YYYY-MM-DD (예: 2025-12-03)\n")
            return 1

        chunk = get_daily_lyric(db.get_all_chunks(), target_date)
        display_date = args.date

    else:
        # 오늘의 가사 (기본)
        chunk = get_daily_lyric(db.get_all_chunks())
        today = date.today()
        display_date = today.strftime('%Y-%m-%d')

    # 가사 출력
    if chunk:
        print(format_lyric_output(chunk, display_date))
    else:
        print("\n❌ 가사를 선택할 수 없습니다.\n")
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
