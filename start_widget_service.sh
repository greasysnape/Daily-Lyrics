#!/bin/bash
# Daily Lyrics Widget Service 시작 스크립트

# 작업 디렉토리로 이동
cd "/Users/cky/Documents/CKY/Daily Lyrics"

# 환경 변수 설정
export PATH="/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:$PATH"
export HOME="/Users/cky"

# Python 경로 확인
PYTHON3="/usr/bin/python3"

# 로그 디렉토리 생성
mkdir -p logs

# 서버 시작
echo "$(date): Starting Daily Lyrics Widget Service..." >> logs/startup.log
$PYTHON3 -m uvicorn src.widget_service:app \
    --host 0.0.0.0 \
    --port 58384 \
    --loop asyncio \
    --http h11 \
    >> logs/widget_service.log 2>> logs/widget_service_error.log
