# 마크다운 레벨 변환기 - 윈도우 실행 파일 빌드 가이드

## 준비사항

1. Python 3.7 이상 설치
2. 필요한 패키지 설치:
```bash
pip install flask pyinstaller
```

## 빌드 방법

### 방법 1: spec 파일 사용 (권장)

```bash
cd web
pyinstaller web_converter.spec
```

### 방법 2: 직접 명령어 사용

```bash
cd web
pyinstaller --onefile --name MarkdownConverter --add-data "templates:templates" web_converter.py
```

## 빌드 결과

빌드가 완료되면 다음 위치에 실행 파일이 생성됩니다:
- `web/dist/MarkdownConverter.exe` (Windows)
- `web/dist/MarkdownConverter` (Linux/Mac)

## 실행 방법

1. 실행 파일을 더블클릭하거나 터미널에서 실행
2. 콘솔 창에 "웹서버 시작: http://localhost:5000" 메시지 표시
3. 웹 브라우저에서 `http://localhost:5000` 접속
4. 마크다운 변환기 사용

## 주의사항

- 실행 파일 크기가 크게 나올 수 있습니다 (50-100MB)
- 첫 실행 시 약간의 시간이 걸릴 수 있습니다
- 백신 프로그램이 오탐할 수 있으니 예외 처리가 필요할 수 있습니다
- 종료 시 콘솔 창에서 Ctrl+C를 누르거나 창을 닫으세요

## 배포

빌드된 실행 파일(`MarkdownConverter.exe`)만 배포하면 됩니다.
다른 사용자는 Python 설치 없이 실행 파일만으로 사용 가능합니다.

## 콘솔 창 숨기기 (선택사항)

콘솔 창 없이 백그라운드로 실행하려면 `web_converter.spec` 파일에서:
```python
console=True,  # 이 부분을
console=False, # 이렇게 변경
```

## 아이콘 추가 (선택사항)

실행 파일에 아이콘을 추가하려면:
1. `.ico` 파일 준비 (32x32 또는 256x256 픽셀)
2. `web_converter.spec` 파일에서:
```python
icon=None,  # 이 부분을
icon='icon.ico',  # 아이콘 파일 경로로 변경
```

## 문제 해결

### 빌드 오류 발생 시
```bash
# 기존 빌드 파일 삭제
rm -rf build dist *.spec
# 다시 빌드
pyinstaller --clean web_converter.spec
```

### 실행 시 templates 폴더를 찾지 못하는 경우
spec 파일의 `datas` 설정을 확인하세요:
```python
datas=[('templates', 'templates')],
```
