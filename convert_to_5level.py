#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
목차6.md를 5레벨 표준 구조로 변환
원본 구조:
  ### 1. 제목
  1.1 소제목
    - 항목

변환 후 (start_level에 따라):
  start_level=1: # 제목, ## 소제목, ### 항목
  start_level=2: ## 제목, ### 소제목, #### 항목
  start_level=3: ### 제목, #### 소제목, ##### 항목
"""

import re
import sys

def convert_to_5level(input_file, output_file, start_level=1):
    """
    Args:
        input_file: 입력 파일
        output_file: 출력 파일
        start_level: 시작 레벨 (1=#, 2=##, 3=### 등)
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    result = []

    # 시작 레벨에 따른 # 개수
    level1 = '#' * start_level
    level2 = '#' * (start_level + 1)
    level3 = '#' * (start_level + 2)

    for line in lines:
        # 빈 줄은 그대로 유지
        if line.strip() == '':
            result.append(line)
            continue

        # ### 제목 → level1 제목 (번호 제거)
        if line.startswith('###'):
            text = line[3:].strip()
            # "1. ", "2. " 등 앞의 번호 제거
            text = re.sub(r'^\d+\.\s+', '', text)
            result.append(f'{level1} {text}\n')
            continue

        # 1.1, 1.2, 2.1 등으로 시작하는 줄 → level2 (번호 제거)
        if re.match(r'^\d+\.\d+\s+', line):
            text = re.sub(r'^\d+\.\d+\s+', '', line)
            result.append(f'{level2} {text}')
            continue

        # 앞에 공백이 있는 경우도 처리
        if re.match(r'^\s+\d+\.\d+\s+', line):
            text = re.sub(r'^\s+\d+\.\d+\s+', '', line)
            result.append(f'{level2} {text}')
            continue

        # - 로 시작하는 줄 → level3
        if re.match(r'^\s*-\s+', line):
            text = re.sub(r'^\s*-\s+', '', line)
            result.append(f'{level3} {text}')
            continue

        # 그 외는 그대로 유지
        result.append(line)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(result)

    print(f"변환 완료: {input_file} → {output_file}")
    print(f"시작 레벨: {start_level} (### → {level1}, 1.1 → {level2}, - → {level3})")

if __name__ == '__main__':
    # 명령줄 인자로 start_level 지정 가능
    # 예: python convert_to_5level.py 3  (###부터 시작)
    start_level = 1
    if len(sys.argv) > 1:
        try:
            start_level = int(sys.argv[1])
        except ValueError:
            print("사용법: python convert_to_5level.py [start_level]")
            print("예: python convert_to_5level.py 1  (# 부터 시작)")
            print("예: python convert_to_5level.py 3  (### 부터 시작)")
            sys.exit(1)

    convert_to_5level('목차6.md', '목차6_5level.md', start_level)
