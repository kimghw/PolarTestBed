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

def convert_markdown_level(content, output_level=1, level1_pattern=r'^###\s+', level2_pattern=r'^\d+\.\d+\s+', level3_pattern=r'^\s*-\s+', level4_pattern='', level5_pattern='', suffix='', exclude_levels=None):
    """
    마크다운 레벨 변환 (사용자 정의 패턴 지원, 최대 5레벨)
    Args:
        content: 마크다운 텍스트
        output_level: 출력 시작 레벨 (1=#, 2=##, 3=### 등)
        level1_pattern: 레벨 1로 인식할 정규식 패턴
        level2_pattern: 레벨 2로 인식할 정규식 패턴
        level3_pattern: 레벨 3로 인식할 정규식 패턴
        level4_pattern: 레벨 4로 인식할 정규식 패턴
        level5_pattern: 레벨 5로 인식할 정규식 패턴
        suffix: 마크 뒤에 추가할 공백이나 심볼 (예: ' ', '  ', ' ▶ ', ' >> ' 등)
        exclude_levels: 변환 결과에서 제외할 레벨 리스트 (예: ['level1', 'level2'])
    Returns:
        변환된 마크다운 텍스트
    """
    if exclude_levels is None:
        exclude_levels = []

    lines = content.split('\n')
    result = []
    line_types = []  # 각 라인이 어떤 소스 레벨에서 왔는지 추적

    # 출력 레벨에 따른 # 개수
    level1 = '#' * output_level
    level2 = '#' * (output_level + 1)
    level3 = '#' * (output_level + 2)
    level4 = '#' * min(output_level + 3, 6)  # 최대 6개
    level5 = '#' * min(output_level + 4, 6)  # 최대 6개

    # 패턴 컴파일 (빈 패턴 체크)
    try:
        pattern1 = re.compile(level1_pattern) if level1_pattern else None
        pattern2 = re.compile(level2_pattern) if level2_pattern else None
        pattern3 = re.compile(level3_pattern) if level3_pattern else None
        pattern4 = re.compile(level4_pattern) if level4_pattern else None
        pattern5 = re.compile(level5_pattern) if level5_pattern else None
    except re.error as e:
        raise ValueError(f"정규식 오류: {e}")

    for line in lines:
        # 빈 줄은 그대로 유지
        if line.strip() == '':
            result.append(line)
            line_types.append(None)
            continue

        converted_line = None
        source_type = None

        # 레벨 1 패턴 매칭
        if pattern1 and pattern1.match(line):
            text = pattern1.sub('', line).strip()
            # 숫자 번호 제거 (1., 2., A. 등)
            text = re.sub(r'^[0-9A-Za-z]+[\.\)]\s*', '', text)
            converted_line = f'{level1}{suffix} {text}'
            source_type = 'level1'

        # 레벨 2 패턴 매칭
        elif pattern2 and pattern2.match(line):
            text = pattern2.sub('', line).strip()
            # 숫자 번호 제거
            text = re.sub(r'^[0-9A-Za-z]+[\.\)]\s*', '', text)
            converted_line = f'{level2}{suffix} {text}'
            source_type = 'level2'

        # 레벨 3 패턴 매칭
        elif pattern3 and pattern3.match(line):
            text = pattern3.sub('', line).strip()
            converted_line = f'{level3}{suffix} {text}'
            source_type = 'level3'

        # 레벨 4 패턴 매칭
        elif pattern4 and pattern4.match(line):
            text = pattern4.sub('', line).strip()
            converted_line = f'{level4}{suffix} {text}'
            source_type = 'level4'

        # 레벨 5 패턴 매칭
        elif pattern5 and pattern5.match(line):
            text = pattern5.sub('', line).strip()
            converted_line = f'{level5}{suffix} {text}'
            source_type = 'level5'

        # 변환할 라인이 있으면 추가, 없으면 원본 그대로
        if converted_line is not None:
            result.append(converted_line)
            line_types.append(source_type)
        else:
            result.append(line)
            line_types.append(None)

    # 변환 완료 후 제외 레벨 적용 (소스 레벨 기준)
    if exclude_levels:
        print(f"[제외 레벨] exclude_levels={exclude_levels}")

        # 제외 레벨에 해당하는 라인 필터링
        filtered_result = []
        for i, (line, source_type) in enumerate(zip(result, line_types)):
            # 소스 타입이 제외 레벨에 포함되지 않으면 추가
            if source_type not in exclude_levels:
                filtered_result.append(line)
            else:
                print(f"[제외됨] {line[:50]}... (소스: {source_type})")

        print(f"[필터링 완료] 원본 {len(result)}줄 → 필터링 후 {len(filtered_result)}줄")
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
        output_level = int(data.get('output_level', 1))
        level1_pattern = data.get('level1_pattern', r'^###\s+')
        level2_pattern = data.get('level2_pattern', r'^\d+\.\d+\s+')
        level3_pattern = data.get('level3_pattern', r'^\s*-\s+')
        level4_pattern = data.get('level4_pattern', '')
        level5_pattern = data.get('level5_pattern', '')
        suffix = data.get('suffix', '')

        # 디버깅 로그
        print(f"[변환 요청] output_level={output_level}, suffix='{suffix}'")
        print(f"  level1_pattern='{level1_pattern}'")
        print(f"  level2_pattern='{level2_pattern}'")
        print(f"  level3_pattern='{level3_pattern}'")
        print(f"  level4_pattern='{level4_pattern}'")
        print(f"  level5_pattern='{level5_pattern}'")

        if not content:
            return jsonify({'error': '내용을 입력해주세요.'}), 400

        if output_level < 1 or output_level > 6:
            return jsonify({'error': '출력 레벨은 1-6 사이여야 합니다.'}), 400

        result = convert_markdown_level(
            content,
            output_level,
            level1_pattern,
            level2_pattern,
            level3_pattern,
            level4_pattern,
            level5_pattern,
            suffix,
            None  # exclude_levels는 더이상 사용하지 않음
        )

        print(f"[변환 완료] 결과 라인 수: {len(result.split(chr(10)))}")

        return jsonify({
            'success': True,
            'result': result,
            'output_level': output_level,
            'suffix': suffix
        })

    except ValueError as e:
        print(f"[변환 오류] {str(e)}")
        return jsonify({'error': str(e)}), 400
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
