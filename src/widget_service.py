#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Daily Lyrics Widget Service
네이티브 위젯을 위한 HTTP API 서버

사용법:
    uvicorn src.widget_service:app --host 0.0.0.0 --port 58384
"""

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Optional
import logging

from src.lyrics_database import LyricsDatabase
from src.daily_selector import get_interval_lyric, get_random_lyric

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성
app = FastAPI(
    title="Daily Lyrics Widget Service",
    description="네이티브 위젯을 위한 가사 API",
    version="2.0.0"
)

# CORS 설정 (모든 origin 허용 - 로컬 전용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 가사 데이터베이스 초기화
logger.info("가사 데이터베이스 로딩 중...")
db = LyricsDatabase()
logger.info(f"로드 완료: {db.get_chunk_count()}개 가사 청크")


@app.get("/")
def root():
    """루트 엔드포인트"""
    return {
        "service": "Daily Lyrics Widget Service",
        "version": "2.0.0",
        "status": "running",
        "endpoints": {
            "current_lyric": "/current-lyric?interval=3h",
            "random_lyric": "/random-lyric",
            "health": "/health",
            "stats": "/stats"
        }
    }


@app.get("/health")
def health_check():
    """서비스 상태 확인"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "chunks_count": db.get_chunk_count(),
        "albums_count": db.albums_count,
        "tracks_count": db.tracks_count
    }


@app.get("/current-lyric")
def get_current_lyric(
    interval: str = Query(
        default="24h",
        regex="^(1h|3h|6h|12h|24h)$",
        description="가사 변경 주기 (1h, 3h, 6h, 12h, 24h)"
    )
):
    """
    현재 시간에 해당하는 가사 반환

    Query Parameters:
        interval: 가사 변경 주기 (1h, 3h, 6h, 12h, 24h)

    Returns:
        {
            "success": true,
            "data": {
                "lines": ["가사 라인 1", "가사 라인 2"],
                "title": "곡 제목",
                "album": "앨범명",
                "year": 2019,
                "artist": "태연 (TAEYEON)",
                "timestamp": "2025-12-04T..."
            }
        }
    """
    try:
        # 빈 데이터베이스 체크
        if db.is_empty():
            logger.warning("가사 데이터가 없습니다")
            return {
                "success": False,
                "error": "No lyrics data available",
                "message": "data/ 폴더에 가사 JSON 파일을 추가해주세요"
            }

        # 현재 시간의 가사 가져오기
        chunk = get_interval_lyric(
            db.get_all_chunks(),
            interval,
            datetime.now()
        )

        if chunk:
            logger.info(f"가사 반환: {chunk['title']} (interval={interval})")
            return {
                "success": True,
                "data": {
                    "lines": chunk['lines'],
                    "title": chunk['title'],
                    "album": chunk['album'],
                    "year": chunk['year'],
                    "artist": chunk.get('artist', '태연 (TAEYEON)'),
                    "timestamp": datetime.now().isoformat(),
                    "interval": interval
                }
            }
        else:
            logger.error("가사 선택 실패")
            return {
                "success": False,
                "error": "Failed to select lyrics"
            }

    except Exception as e:
        logger.error(f"오류 발생: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e)
        }


@app.get("/random-lyric")
def get_random_lyric_endpoint():
    """
    완전 랜덤 가사 반환 (시간과 무관)

    Returns:
        {
            "success": true,
            "data": {
                "lines": ["가사 라인 1", "가사 라인 2"],
                "title": "곡 제목",
                "album": "앨범명",
                "year": 2019,
                "artist": "태연 (TAEYEON)"
            }
        }
    """
    try:
        if db.is_empty():
            return {
                "success": False,
                "error": "No lyrics data available"
            }

        chunk = get_random_lyric(db.get_all_chunks())

        if chunk:
            logger.info(f"랜덤 가사 반환: {chunk['title']}")
            return {
                "success": True,
                "data": {
                    "lines": chunk['lines'],
                    "title": chunk['title'],
                    "album": chunk['album'],
                    "year": chunk['year'],
                    "artist": chunk.get('artist', '태연 (TAEYEON)'),
                    "timestamp": datetime.now().isoformat()
                }
            }
        else:
            return {
                "success": False,
                "error": "Failed to select lyrics"
            }

    except Exception as e:
        logger.error(f"오류 발생: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e)
        }


@app.get("/stats")
def get_statistics():
    """
    가사 데이터베이스 통계

    Returns:
        {
            "chunks_count": 787,
            "albums_count": 18,
            "tracks_count": 69,
            "albums": {...}
        }
    """
    try:
        return {
            "success": True,
            "data": {
                "chunks_count": db.get_chunk_count(),
                "albums_count": db.albums_count,
                "tracks_count": db.tracks_count,
                "albums": db.get_albums_info()
            }
        }
    except Exception as e:
        logger.error(f"통계 조회 오류: {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e)
        }


# 서버 시작 시 로그
@app.on_event("startup")
async def startup_event():
    logger.info("=" * 60)
    logger.info("Daily Lyrics Widget Service 시작")
    logger.info(f"가사 청크: {db.get_chunk_count()}개")
    logger.info(f"앨범: {db.albums_count}개")
    logger.info(f"트랙: {db.tracks_count}개")
    logger.info("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Daily Lyrics Widget Service 종료")


if __name__ == "__main__":
    import uvicorn

    print("🎵 Daily Lyrics Widget Service")
    print("=" * 60)
    print(f"가사 청크: {db.get_chunk_count()}개 로드됨")
    print("=" * 60)
    print("서버 시작 중...")
    print("접속: http://localhost:58384")
    print("=" * 60)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=58384,
        log_level="info"
    )
