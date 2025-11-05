#!/usr/bin/env python3
"""
목차.md 파일의 헤딩 레벨을 변경하는 스크립트

변환 규칙:
- ## (H2) → ##### (H5)
- 1. 2. 3. (번호 목록) → #### (H4)
- - (하위 항목) → ### (H3)
"""

import re
import sys
from pathlib import Path


def convert_markdown_format(input_file='목차.md', output_file='목차_converted.md'):
    """
    마크다운 파일의 형식을 변환

    Args:
        input_file: 입력 파일 경로
        output_file: 출력 파일 경로
    """

    # 파일 읽기
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"❌ 파일을 찾을 수 없습니다: {input_file}")
        return False

    converted_lines = []

    for line in lines:
        original_line = line
        converted = False

        # ## 섹션 헤더를 ##### 로 변환
        if line.startswith('## '):
            converted_line = '##### ' + line[3:]
            converted_lines.append(converted_line)
            converted = True
            print(f"✓ H2 → H5: {line.strip()[:50]}...")

        # 번호 목록 (1. 2. 3. 등)을 #### 로 변환
        elif re.match(r'^\d+\.\s+', line):
            # 번호와 점을 제거하고 #### 로 시작
            content = re.sub(r'^\d+\.\s+', '', line)
            converted_line = '#### ' + content
            converted_lines.append(converted_line)
            converted = True
            print(f"✓ Numbered → H4: {line.strip()[:50]}...")

        # 들여쓰기된 하위 항목 (   - )을 ### 로 변환
        elif re.match(r'^\s+-\s+', line):
            # 들여쓰기와 대시를 제거하고 ### 로 시작
            content = re.sub(r'^\s+-\s+', '', line)
            converted_line = '### ' + content
            converted_lines.append(converted_line)
            converted = True
            print(f"✓ Bullet → H3: {line.strip()[:50]}...")

        # 변환하지 않는 라인은 그대로 유지
        else:
            converted_lines.append(original_line)

    # 변환된 내용을 파일로 저장
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(converted_lines)
        print(f"\n✅ 변환 완료! '{output_file}' 파일이 생성되었습니다.")
        return True
    except Exception as e:
        print(f"❌ 파일 저장 중 오류 발생: {e}")
        return False


def preview_conversion(input_file='목차.md', num_lines=10):
    """
    변환 결과를 미리보기

    Args:
        input_file: 입력 파일 경로
        num_lines: 미리볼 라인 수
    """

    print("\n" + "=" * 60)
    print("🔍 변환 미리보기 (처음 {}줄)".format(num_lines))
    print("=" * 60)

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:num_lines]
    except FileNotFoundError:
        print(f"❌ 파일을 찾을 수 없습니다: {input_file}")
        return

    for i, line in enumerate(lines, 1):
        if line.strip():
            print(f"\n라인 {i}:")
            print(f"  원본: {line.rstrip()}")

            # 변환 결과 표시
            if line.startswith('## '):
                converted = '##### ' + line[3:]
                print(f"  변환: {converted.rstrip()}")
            elif re.match(r'^\d+\.\s+', line):
                content = re.sub(r'^\d+\.\s+', '', line)
                converted = '#### ' + content
                print(f"  변환: {converted.rstrip()}")
            elif re.match(r'^\s+-\s+', line):
                content = re.sub(r'^\s+-\s+', '', line)
                converted = '### ' + content
                print(f"  변환: {converted.rstrip()}")
            else:
                print(f"  변환: (변경 없음)")


def main():
    """메인 실행 함수"""

    print("🔄 마크다운 헤딩 레벨 변환 스크립트")
    print("=" * 60)
    print("변환 규칙:")
    print("  • ## (섹션 헤더) → ##### (H5)")
    print("  • 1. 2. 3. (번호 목록) → #### (H4)")
    print("  • - (하위 항목) → ### (H3)")
    print("=" * 60)

    # 미리보기 표시
    preview_conversion('목차.md', num_lines=15)

    print("\n" + "=" * 60)
    response = input("\n계속 진행하시겠습니까? (y/n): ")

    if response.lower() == 'y':
        # 실제 변환 실행
        if convert_markdown_format('목차.md', '목차_converted.md'):
            print("\n📝 변환된 파일 정보:")
            print("  • 원본 파일: 목차.md")
            print("  • 변환된 파일: 목차_converted.md")

            # 원본 파일을 변환된 내용으로 덮어쓸지 확인
            print("\n" + "=" * 60)
            overwrite = input("\n원본 파일(목차.md)을 변환된 내용으로 덮어쓰시겠습니까? (y/n): ")

            if overwrite.lower() == 'y':
                try:
                    # 백업 생성
                    import shutil
                    shutil.copy('목차.md', '목차_backup.md')
                    print("✅ 백업 파일 생성: 목차_backup.md")

                    # 변환된 파일로 원본 덮어쓰기
                    shutil.move('목차_converted.md', '목차.md')
                    print("✅ 원본 파일이 업데이트되었습니다.")
                except Exception as e:
                    print(f"❌ 파일 덮어쓰기 중 오류 발생: {e}")
    else:
        print("❌ 변환이 취소되었습니다.")


if __name__ == "__main__":
    # 명령줄 인자 처리 (옵션)
    if len(sys.argv) > 1:
        if sys.argv[1] == '--auto':
            # 자동 모드: 확인 없이 바로 변환
            print("🚀 자동 변환 모드")
            convert_markdown_format('목차.md', '목차_converted.md')
        elif sys.argv[1] == '--help':
            print("사용법:")
            print("  python convert_markdown_headings.py        # 대화형 모드")
            print("  python convert_markdown_headings.py --auto # 자동 변환")
            print("  python convert_markdown_headings.py --help # 도움말")
    else:
        main()