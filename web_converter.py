#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
마크다운 레벨 변환 웹서비스
"""

from flask import Flask, render_template, request, send_file, jsonify
import re
import io
import os

app = Flask(__name__)

def convert_markdown_level(content, start_level=1, suffix='', exclude_levels=None):
    """
    마크다운 레벨 변환
    Args:
        content: 마크다운 텍스트
        start_level: 시작 레벨 (1=#, 2=##, 3=### 등)
        suffix: 마크 뒤에 추가할 공백이나 심볼 (예: ' ', '  ', ' ▶ ', ' >> ' 등)
        exclude_levels: 변환 결과에서 제외할 레벨 리스트 (예: ['level1', 'level2'])
    Returns:
        변환된 마크다운 텍스트
    """
    if exclude_levels is None:
        exclude_levels = []

    lines = content.split('\n')
    result = []

    # 시작 레벨에 따른 # 개수
    level1 = '#' * start_level
    level2 = '#' * (start_level + 1)
    level3 = '#' * (start_level + 2)

    # 원본 형식별로 어떤 레벨로 변환될지 매핑
    source_to_target_level = {}

    for line in lines:
        # 빈 줄은 그대로 유지
        if line.strip() == '':
            result.append(line)
            continue

        converted_line = None
        source_type = None

        # ### 제목 → level1 제목 (번호 제거)
        if line.startswith('###'):
            text = line[3:].strip()
            # "1. ", "2. " 등 앞의 번호 제거
            text = re.sub(r'^\d+\.\s+', '', text)
            converted_line = f'{level1}{suffix} {text}'
            source_type = 'level1'

        # 1.1, 1.2, 2.1 등으로 시작하는 줄 → level2 (번호 제거)
        elif re.match(r'^\d+\.\d+\s+', line):
            text = re.sub(r'^\d+\.\d+\s+', '', line)
            converted_line = f'{level2}{suffix} {text}'
            source_type = 'level2'

        # 앞에 공백이 있는 경우도 처리
        elif re.match(r'^\s+\d+\.\d+\s+', line):
            text = re.sub(r'^\s+\d+\.\d+\s+', '', line)
            converted_line = f'{level2}{suffix} {text}'
            source_type = 'level2'

        # - 로 시작하는 줄 → level3
        elif re.match(r'^\s*-\s+', line):
            text = re.sub(r'^\s*-\s+', '', line)
            converted_line = f'{level3}{suffix} {text}'
            source_type = 'level3'

        # 변환할 라인이 있으면 추가, 없으면 원본 그대로
        if converted_line is not None:
            result.append(converted_line)
            if source_type:
                source_to_target_level[source_type] = converted_line.split()[0]
        else:
            result.append(line)

    # 변환 완료 후 제외 레벨 적용
    if exclude_levels:
        # 제외할 마크다운 레벨 계산 (level1 -> #, level2 -> ##, level3 -> ###)
        exclude_markdown_levels = []
        for ex_level in exclude_levels:
            if ex_level == 'level1':
                exclude_markdown_levels.append(level1)
            elif ex_level == 'level2':
                exclude_markdown_levels.append(level2)
            elif ex_level == 'level3':
                exclude_markdown_levels.append(level3)
            elif ex_level == 'level4':
                exclude_markdown_levels.append('#' * (start_level + 3))
            elif ex_level == 'level5':
                exclude_markdown_levels.append('#' * (start_level + 4))
            elif ex_level == 'level6':
                exclude_markdown_levels.append('#' * (start_level + 5))

        # 제외 레벨에 해당하는 라인 필터링
        filtered_result = []
        for line in result:
            # 마크다운 헤딩인지 확인
            if line.strip().startswith('#'):
                # 헤딩 레벨 추출
                heading_match = re.match(r'^(#+)', line.strip())
                if heading_match:
                    heading_level = heading_match.group(1)
                    # 제외 레벨에 포함되지 않으면 추가
                    if heading_level not in exclude_markdown_levels:
                        filtered_result.append(line)
                else:
                    filtered_result.append(line)
            else:
                filtered_result.append(line)

        return '\n'.join(filtered_result)

    return '\n'.join(result)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json()
        content = data.get('content', '')
        start_level = int(data.get('start_level', 1))
        suffix = data.get('suffix', '')
        exclude_levels = data.get('exclude_levels', [])

        # 디버깅 로그
        print(f"[변환 요청] start_level={start_level}, suffix='{suffix}', exclude_levels={exclude_levels}")

        if not content:
            return jsonify({'error': '내용을 입력해주세요.'}), 400

        if start_level < 1 or start_level > 6:
            return jsonify({'error': '시작 레벨은 1-6 사이여야 합니다.'}), 400

        result = convert_markdown_level(content, start_level, suffix, exclude_levels)

        print(f"[변환 완료] 결과 라인 수: {len(result.split(chr(10)))}")

        return jsonify({
            'success': True,
            'result': result,
            'start_level': start_level,
            'suffix': suffix,
            'exclude_levels': exclude_levels
        })

    except Exception as e:
        print(f"[변환 오류] {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        content = data.get('content', '')
        filename = data.get('filename', 'converted.md')

        # 메모리에 파일 생성
        file_io = io.BytesIO()
        file_io.write(content.encode('utf-8'))
        file_io.seek(0)

        return send_file(
            file_io,
            mimetype='text/markdown',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # templates 폴더가 없으면 생성
    os.makedirs('templates', exist_ok=True)

    print("웹서버 시작: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
