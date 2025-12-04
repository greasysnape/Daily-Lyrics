"""
일일 가사 선택 로직
날짜와 시간 주기를 시드로 사용하여 일관된 가사를 선택합니다.
"""

import random
from datetime import date, datetime
from typing import Dict, List, Optional, Literal

# 지원하는 시간 주기
IntervalType = Literal["1h", "3h", "6h", "12h", "24h"]


def _get_time_block(current_time: datetime, interval: str) -> int:
    """
    시간 주기에 따라 현재 시간의 블록 번호 계산

    Args:
        current_time: 현재 시간
        interval: 시간 주기 (1h, 3h, 6h, 12h, 24h)

    Returns:
        시간 블록 번호
    """
    hour = current_time.hour

    if interval == "1h":
        return hour  # 0-23
    elif interval == "3h":
        return hour // 3  # 0-7
    elif interval == "6h":
        return hour // 6  # 0-3
    elif interval == "12h":
        return hour // 12  # 0-1
    else:  # 24h
        return 0


def get_interval_lyric(all_chunks: List[Dict],
                       interval: str = "24h",
                       target_datetime: Optional[datetime] = None) -> Optional[Dict]:
    """
    시간 주기별로 일관된 랜덤 청크 선택
    같은 시간 블록 내에서는 항상 같은 가사가 선택됩니다.

    Args:
        all_chunks: 모든 가사 청크 리스트
        interval: 시간 주기 (1h, 3h, 6h, 12h, 24h)
        target_datetime: 특정 시간 (None이면 현재 시간)

    Returns:
        선택된 가사 청크 또는 None
    """
    if not all_chunks:
        return None

    if target_datetime is None:
        target_datetime = datetime.now()

    # 날짜 부분 (YYYYMMDD)
    date_part = int(target_datetime.strftime('%Y%m%d'))

    # 시간 블록 계산
    time_block = _get_time_block(target_datetime, interval)

    # 시드 생성: 날짜 + 시간블록
    # 예: 2025120405 (2025-12-04, 5번째 블록)
    seed = date_part * 100 + time_block

    # 시드 설정하여 일관된 랜덤 선택
    random.seed(seed)
    selected_chunk = random.choice(all_chunks)
    random.seed()  # 시드 리셋

    return selected_chunk


def get_daily_lyric(all_chunks: List[Dict], target_date: Optional[date] = None) -> Optional[Dict]:
    """
    날짜를 시드로 사용하여 일관된 랜덤 청크 선택
    같은 날짜에는 항상 같은 가사가 선택됩니다.

    Args:
        all_chunks: 모든 가사 청크 리스트
        target_date: 특정 날짜 (None이면 오늘)

    Returns:
        선택된 가사 청크 (lines, title, album 등 포함) 또는 None
    """
    if not all_chunks:
        return None

    if target_date is None:
        target_date = date.today()

    # 날짜를 정수 시드로 변환 (예: 20251203)
    seed = int(target_date.strftime('%Y%m%d'))

    # 시드 설정하여 일관된 랜덤 선택
    random.seed(seed)
    selected_chunk = random.choice(all_chunks)
    random.seed()  # 시드 리셋

    return selected_chunk


def get_random_lyric(all_chunks: List[Dict]) -> Optional[Dict]:
    """
    완전 랜덤 가사 청크 선택 (날짜와 무관)

    Args:
        all_chunks: 모든 가사 청크 리스트

    Returns:
        선택된 가사 청크 또는 None
    """
    if not all_chunks:
        return None

    return random.choice(all_chunks)


def get_lyric_for_date_range(all_chunks: List[Dict],
                             start_date: date,
                             end_date: date) -> List[Dict]:
    """
    특정 날짜 범위의 가사들을 반환 (테스트/미리보기 용)

    Args:
        all_chunks: 모든 가사 청크 리스트
        start_date: 시작 날짜
        end_date: 종료 날짜

    Returns:
        각 날짜의 가사 리스트
    """
    if not all_chunks:
        return []

    results = []
    current_date = start_date

    while current_date <= end_date:
        lyric = get_daily_lyric(all_chunks, current_date)
        if lyric:
            results.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'lyric': lyric
            })
        current_date = date.fromordinal(current_date.toordinal() + 1)

    return results


def parse_date(date_string: str) -> Optional[date]:
    """
    날짜 문자열을 date 객체로 파싱

    Args:
        date_string: 날짜 문자열 (YYYY-MM-DD 형식)

    Returns:
        date 객체 또는 None (파싱 실패 시)
    """
    try:
        return datetime.strptime(date_string, '%Y-%m-%d').date()
    except ValueError:
        return None
