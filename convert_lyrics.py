#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
가사 텍스트 파일을 JSON으로 변환하는 도구

사용법:
1. lyrics_input/ 폴더에 앨범별로 폴더 생성
2. 각 폴더에 트랙별 .txt 파일 작성
3. python3 convert_lyrics.py 실행
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional


class LyricsConverter:
    """가사 텍스트 파일을 JSON으로 변환하는 클래스"""

    def __init__(self, input_dir: str = "lyrics_input", output_dir: str = "data"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)

    def parse_txt_file(self, file_path: Path) -> Optional[Dict]:
        """
        텍스트 파일을 파싱하여 딕셔너리로 변환

        파일 형식:
        title: 곡 제목
        album: 앨범명
        year: 연도
        track_number: 트랙 번호
        ---
        가사 청크 1

        가사 청크 2
        (빈 줄로 청크 구분)

        Args:
            file_path: 텍스트 파일 경로

        Returns:
            파싱된 데이터 딕셔너리 또는 None
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # --- 구분선으로 메타데이터와 가사 분리
            if '---' in content:
                metadata_section, lyrics_section = content.split('---', 1)
            else:
                print(f"⚠️  {file_path.name}: '---' 구분선이 없습니다. 전체를 가사로 처리합니다.")
                metadata_section = ""
                lyrics_section = content

            # 메타데이터 파싱
            metadata = self._parse_metadata(metadata_section, file_path.name)

            # 가사 청크 파싱 (빈 줄로 구분)
            chunks = self._parse_chunks(lyrics_section)

            if not chunks:
                print(f"⚠️  {file_path.name}: 가사 청크가 없습니다.")
                return None

            return {
                'track_number': metadata['track_number'],
                'title': metadata['title'],
                'album': metadata['album'],
                'year': metadata['year'],
                'artist': metadata.get('artist'),
                'chunks': chunks
            }

        except Exception as e:
            print(f"❌ {file_path.name} 파싱 오류: {e}")
            return None

    def _parse_metadata(self, metadata_section: str, filename: str) -> Dict:
        """메타데이터 섹션 파싱"""
        metadata = {
            'title': 'Unknown',
            'album': 'Unknown',
            'year': 0,
            'track_number': 0,
            'artist': 'Unknown'
        }

        # 각 줄에서 key: value 형식 파싱
        for line in metadata_section.strip().split('\n'):
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()

                if key == 'title':
                    metadata['title'] = value
                elif key == 'album':
                    metadata['album'] = value
                elif key == 'year':
                    try:
                        metadata['year'] = int(value)
                    except ValueError:
                        print(f"⚠️  잘못된 year 값: {value}")
                elif key == 'track_number' or key == 'track':
                    try:
                        metadata['track_number'] = int(value)
                    except ValueError:
                        print(f"⚠️  잘못된 track_number 값: {value}")
                elif key == 'artist':
                    metadata['artist'] = value

        # 파일명에서 트랙 번호 추출 시도 (예: 01_곡명.txt)
        if metadata['track_number'] == 0:
            match = re.match(r'^(\d+)_', filename)
            if match:
                metadata['track_number'] = int(match.group(1))

        return metadata

    def _parse_chunks(self, lyrics_section: str) -> List[Dict]:
        """가사를 청크로 분리 (빈 줄로 구분)"""
        chunks = []

        # 연속된 빈 줄을 구분자로 사용
        # 가사를 빈 줄 하나 이상으로 분리
        raw_chunks = re.split(r'\n\s*\n', lyrics_section.strip())

        chunk_id = 1
        for raw_chunk in raw_chunks:
            lines = [line.strip() for line in raw_chunk.strip().split('\n') if line.strip()]

            if not lines:
                continue

            chunks.append({
                'id': chunk_id,
                'lines': lines
            })
            chunk_id += 1

        return chunks

    def convert_file(self, txt_file: Path, album_folder: Path) -> bool:
        """
        텍스트 파일을 JSON으로 변환

        Args:
            txt_file: 입력 텍스트 파일
            album_folder: 출력할 앨범 폴더

        Returns:
            성공 여부
        """
        # 텍스트 파일 파싱
        data = self.parse_txt_file(txt_file)
        if data is None:
            return False

        # 출력 폴더 생성
        album_folder.mkdir(parents=True, exist_ok=True)

        # JSON 파일명은 입력 파일명과 동일하게 (확장자만 변경)
        json_filename = txt_file.stem + '.json'
        json_path = album_folder / json_filename

        # JSON 저장
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"✅ {txt_file.name} → {json_path.relative_to(self.output_dir)}")
            print(f"   {len(data['chunks'])}개 청크 변환 완료")
            return True

        except Exception as e:
            print(f"❌ JSON 저장 오류: {e}")
            return False

    def convert_all(self, folder_names: List[str] = None) -> None:
        """
        lyrics_input/ 폴더의 텍스트 파일을 변환

        Args:
            folder_names: 특정 앨범 폴더들만 변환 (None이면 전체)
        """
        if not self.input_dir.exists():
            print(f"❌ '{self.input_dir}' 폴더가 없습니다.")
            print(f"💡 폴더를 생성하고 앨범별로 가사 텍스트 파일을 추가해주세요.")
            return

        # 특정 폴더들만 변환
        if folder_names:
            album_folders = []
            for folder_name in folder_names:
                target_folder = self.input_dir / folder_name
                if not target_folder.exists():
                    print(f"⚠️  '{folder_name}' 폴더를 찾을 수 없습니다. 건너뜁니다.")
                    continue
                if not target_folder.is_dir():
                    print(f"⚠️  '{folder_name}'은(는) 폴더가 아닙니다. 건너뜁니다.")
                    continue
                album_folders.append(target_folder)

            if not album_folders:
                print(f"❌ 유효한 폴더가 없습니다.")
                return
        else:
            # 모든 앨범 폴더 찾기 (example_album 제외)
            album_folders = [f for f in self.input_dir.iterdir()
                            if f.is_dir() and not f.name.startswith('.') and 'example' not in f.name.lower()]

        if not album_folders:
            print(f"⚠️  '{self.input_dir}' 폴더에 앨범 폴더가 없습니다.")
            return

        total_files = 0
        success_count = 0

        print("=" * 60)
        if folder_names:
            print(f"🎵 가사 변환 시작 (폴더: {', '.join(folder_names)})")
        else:
            print("🎵 가사 변환 시작 (전체)")
        print("=" * 60)

        for album_folder in sorted(album_folders):
            print(f"\n📀 앨범: {album_folder.name}")
            print("-" * 60)

            # 앨범 폴더 내의 모든 .txt 파일 찾기
            txt_files = sorted(album_folder.glob("*.txt"))

            if not txt_files:
                print(f"   ⚠️  텍스트 파일이 없습니다.")
                continue

            # 출력 앨범 폴더
            output_album_folder = self.output_dir / album_folder.name

            for txt_file in txt_files:
                total_files += 1
                if self.convert_file(txt_file, output_album_folder):
                    success_count += 1

        print("\n" + "=" * 60)
        print(f"✨ 변환 완료: {success_count}/{total_files}개 파일")
        print("=" * 60)


def main():
    """메인 함수"""
    import argparse

    parser = argparse.ArgumentParser(
        description='가사 텍스트 파일을 JSON으로 변환',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 방법:
1. lyrics_input/ 폴더에 앨범별 폴더 생성
2. 각 폴더에 트랙별 .txt 파일 작성
   형식:
   title: 곡 제목
   album: 앨범명
   year: 연도
   track_number: 트랙 번호
   artist: 아티스트 이름
   ---
   가사 청크 1

   가사 청크 2

3. python3 convert_lyrics.py 실행

예시:
  python3 convert_lyrics.py                                    # 모든 파일 변환
  python3 convert_lyrics.py --folder 016_INVU                  # 특정 폴더 하나만 변환
  python3 convert_lyrics.py --folder 016_INVU 999_OST          # 여러 폴더 변환
        """
    )

    parser.add_argument(
        '--folder',
        type=str,
        nargs='+',
        metavar='FOLDER_NAME',
        help='특정 앨범 폴더만 변환 (여러 개 가능, 예: --folder 016_INVU 999_OST)'
    )

    parser.add_argument(
        '--input',
        type=str,
        default='lyrics_input',
        help='입력 폴더 경로 (기본: lyrics_input)'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='data',
        help='출력 폴더 경로 (기본: data)'
    )

    args = parser.parse_args()
    converter = LyricsConverter(args.input, args.output)
    converter.convert_all(args.folder)


if __name__ == '__main__':
    main()
