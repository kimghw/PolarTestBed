#!/bin/bash

# ============================================================
# 목차.md 파일의 헤딩 레벨을 변경하는 Shell 스크립트
#
# 변환 규칙:
# - ## (H2) → ##### (H5)
# - 1. 2. 3. (번호 목록) → #### (H4)
# - - (하위 항목) → ### (H3)
# ============================================================

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 파일 설정
INPUT_FILE="목차.md"
OUTPUT_FILE="목차_converted.md"
BACKUP_FILE="목차_backup.md"

# 함수: 헤더 출력
print_header() {
    echo "============================================================"
    echo "🔄 마크다운 헤딩 레벨 변환 스크립트"
    echo "============================================================"
    echo "변환 규칙:"
    echo "  • ## (섹션 헤더) → ##### (H5)"
    echo "  • 1. 2. 3. (번호 목록) → #### (H4)"
    echo "  • - (하위 항목) → ### (H3)"
    echo "============================================================"
}

# 함수: 파일 존재 확인
check_file() {
    if [ ! -f "$INPUT_FILE" ]; then
        echo -e "${RED}❌ 파일을 찾을 수 없습니다: $INPUT_FILE${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ 입력 파일 확인: $INPUT_FILE${NC}"
}

# 함수: 변환 실행
convert_file() {
    echo -e "\n${BLUE}📝 변환 시작...${NC}"

    # 임시 파일 생성
    > "$OUTPUT_FILE"

    # 라인별로 처리
    while IFS= read -r line; do
        # ## 로 시작하는 라인을 ##### 로 변환
        if [[ "$line" == "## "* ]]; then
            # sed를 사용하여 정확하게 변환
            converted_line=$(echo "$line" | sed 's/^## /##### /')
            echo "$converted_line" >> "$OUTPUT_FILE"
            echo -e "${GREEN}  ✓ H2 → H5: ${line:0:50}...${NC}"

        # 숫자. 로 시작하는 라인을 #### 로 변환
        elif [[ "$line" =~ ^[0-9]+\. ]]; then
            # 번호와 점, 공백을 제거하고 #### 추가
            content=$(echo "$line" | sed 's/^[0-9]*\. //')
            echo "#### $content" >> "$OUTPUT_FILE"
            echo -e "${GREEN}  ✓ Numbered → H4: ${line:0:50}...${NC}"

        # 공백으로 시작하고 - 가 있는 라인을 ### 로 변환
        elif [[ "$line" =~ ^[[:space:]]+-[[:space:]] ]]; then
            # 들여쓰기와 대시를 제거하고 ### 추가
            content=$(echo "$line" | sed 's/^[[:space:]]*- //')
            echo "### $content" >> "$OUTPUT_FILE"
            echo -e "${GREEN}  ✓ Bullet → H3: ${line:0:50}...${NC}"

        # 변환하지 않는 라인은 그대로 유지
        else
            echo "$line" >> "$OUTPUT_FILE"
        fi
    done < "$INPUT_FILE"

    echo -e "\n${GREEN}✅ 변환 완료!${NC}"
}

# 함수: 미리보기
preview_changes() {
    echo -e "\n${YELLOW}🔍 변환 결과 미리보기 (처음 20줄)${NC}"
    echo "============================================================"
    head -n 20 "$OUTPUT_FILE"
    echo "============================================================"
}

# 함수: 원본 파일 덮어쓰기
overwrite_original() {
    echo -e "\n${YELLOW}⚠️  경고: 원본 파일을 덮어쓰시겠습니까?${NC}"
    echo "현재 원본 파일은 백업됩니다: $BACKUP_FILE"
    read -p "계속하시겠습니까? (y/n): " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # 백업 생성
        cp "$INPUT_FILE" "$BACKUP_FILE"
        echo -e "${GREEN}✅ 백업 생성: $BACKUP_FILE${NC}"

        # 변환된 파일로 원본 덮어쓰기
        mv "$OUTPUT_FILE" "$INPUT_FILE"
        echo -e "${GREEN}✅ 원본 파일이 업데이트되었습니다: $INPUT_FILE${NC}"
    else
        echo -e "${BLUE}ℹ️  변환된 파일이 유지됩니다: $OUTPUT_FILE${NC}"
    fi
}

# 함수: 자동 모드
auto_mode() {
    check_file
    convert_file
    echo -e "${GREEN}✅ 변환된 파일: $OUTPUT_FILE${NC}"
}

# 메인 실행
main() {
    print_header
    check_file
    convert_file
    preview_changes

    # 사용자 확인
    echo -e "\n${YELLOW}변환이 올바르게 되었나요?${NC}"
    read -p "원본 파일을 덮어쓰시겠습니까? (y/n): " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # 백업 생성
        cp "$INPUT_FILE" "$BACKUP_FILE"
        echo -e "${GREEN}✅ 백업 생성: $BACKUP_FILE${NC}"

        # 변환된 파일로 원본 덮어쓰기
        mv "$OUTPUT_FILE" "$INPUT_FILE"
        echo -e "${GREEN}✅ 원본 파일이 업데이트되었습니다: $INPUT_FILE${NC}"
    else
        echo -e "${BLUE}ℹ️  변환된 파일이 유지됩니다: $OUTPUT_FILE${NC}"
    fi

    echo -e "\n${GREEN}✨ 작업 완료!${NC}"
}

# 명령줄 인자 처리
case "$1" in
    --auto)
        echo "🚀 자동 변환 모드"
        auto_mode
        ;;
    --help)
        echo "사용법:"
        echo "  ./convert_headings.sh        # 대화형 모드 (미리보기 및 확인)"
        echo "  ./convert_headings.sh --auto # 자동 변환 (확인 없음)"
        echo "  ./convert_headings.sh --help # 도움말"
        ;;
    *)
        main
        ;;
esac