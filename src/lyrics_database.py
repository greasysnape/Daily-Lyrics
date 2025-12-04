"""
가사 데이터베이스 관리 모듈
앨범 폴더를 스캔하고 모든 트랙의 가사 청크를 로드
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional


class LyricsDatabase:
    """가사 데이터베이스 관리 클래스"""

    def __init__(self, data_dir: str = "data"):
        """
        Args:
            data_dir: 가사 데이터가 저장된 디렉토리 경로
        """
        self.data_dir = Path(data_dir)
        self.all_chunks: List[Dict] = []
        self.albums_count = 0
        self.tracks_count = 0

        if self.data_dir.exists():
            self.load_all_lyrics()
        else:
            print(f"⚠️  경고: '{data_dir}' 디렉토리가 존재하지 않습니다.")

    def load_all_lyrics(self) -> None:
        """모든 앨범 폴더를 스캔하고 모든 청크를 로드"""
        self.all_chunks = []
        self.albums_count = 0
        self.tracks_count = 0

        # data/ 안의 모든 앨범 폴더 찾기 (example_album 제외)
        album_folders = sorted([
            f for f in self.data_dir.iterdir()
            if f.is_dir() and not f.name.startswith('.') and 'example' not in f.name.lower()
        ])

        if not album_folders:
            print(f"⚠️  '{self.data_dir}' 폴더에 앨범이 없습니다.")
            return

        self.albums_count = len(album_folders)

        for album_folder in album_folders:
            # 각 앨범 폴더 안의 모든 JSON 파일 찾기
            track_files = sorted(album_folder.glob("*.json"))

            for track_file in track_files:
                try:
                    with open(track_file, 'r', encoding='utf-8') as f:
                        track_data = json.load(f)
                        self.tracks_count += 1

                        # 각 청크에 메타데이터 추가
                        for chunk in track_data.get('chunks', []):
                            self.all_chunks.append({
                                'lines': chunk.get('lines', []),
                                'title': track_data.get('title', 'Unknown'),
                                'album': track_data.get('album', 'Unknown'),
                                'year': track_data.get('year', 0),
                                'track_number': track_data.get('track_number', 0),
                                'artist': track_data.get('artist', '태연 (TAEYEON)'),
                                'album_folder': album_folder.name  # 앨범 커버용 폴더명
                            })
                except json.JSONDecodeError as e:
                    print(f"❌ JSON 파싱 오류: {track_file.name} - {e}")
                except Exception as e:
                    print(f"❌ 파일 로드 오류: {track_file.name} - {e}")

    def get_all_chunks(self) -> List[Dict]:
        """
        모든 가사 청크 반환

        Returns:
            모든 가사 청크의 리스트
        """
        return self.all_chunks

    def get_chunk_count(self) -> int:
        """
        총 청크 수 반환

        Returns:
            청크 개수
        """
        return len(self.all_chunks)

    def get_albums_info(self) -> Dict[str, Dict]:
        """
        앨범별 통계 정보 반환

        Returns:
            앨범명을 키로 하는 딕셔너리 (year, chunk_count 포함)
        """
        albums = {}
        for chunk in self.all_chunks:
            album_name = chunk['album']
            if album_name not in albums:
                albums[album_name] = {
                    'year': chunk['year'],
                    'chunk_count': 0,
                    'tracks': set()
                }
            albums[album_name]['chunk_count'] += 1
            albums[album_name]['tracks'].add(chunk['title'])

        # set을 리스트로 변환
        for album in albums.values():
            album['tracks'] = sorted(list(album['tracks']))
            album['track_count'] = len(album['tracks'])

        return albums

    def is_empty(self) -> bool:
        """
        데이터베이스가 비어있는지 확인

        Returns:
            비어있으면 True
        """
        return len(self.all_chunks) == 0

    def get_random_chunk(self) -> Optional[Dict]:
        """
        임의의 청크 하나를 반환 (테스트용)

        Returns:
            랜덤 청크 또는 None
        """
        import random
        return random.choice(self.all_chunks) if self.all_chunks else None
