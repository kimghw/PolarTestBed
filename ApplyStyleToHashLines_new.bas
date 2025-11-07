Sub ApplyStyleToHashLines_new()
    ' # 개수에 따라 다른 스타일 적용 (마크다운 표준 순서)
    ' # -> 기획_장 (H1 - 가장 큰 제목)
    ' ## -> 기획_절절 (H2)
    ' ### -> 기획_1 (H3)
    ' #### -> 기획_□ (H4)
    ' ##### -> 기획_ㅇ (H5)
    ' ###### -> 기획_- (H6 - 가장 작은 제목)
    ' $ 가 있으면 목록 번호를 1부터 새로 시작

    Dim doc As Document
    Dim para As Paragraph
    Dim count As Integer
    Dim paraText As String
    Dim styleName As String
    Dim hasRestart As Boolean

    Set doc = ActiveDocument
    count = 0

    ' 모든 단락을 검색
    For Each para In doc.Paragraphs
        paraText = Trim(para.Range.Text)
        styleName = ""
        hasRestart = False

        ' ###### 체크 (6개 - 가장 긴 것부터 체크)
        If Left(paraText, 6) = "######" Then
            styleName = "기획_-"
            If Mid(paraText, 7, 1) = "$" Then hasRestart = True

        ' ##### 체크 (5개)
        ElseIf Left(paraText, 5) = "#####" Then
            styleName = "기획_ㅇ"
            If Mid(paraText, 6, 1) = "$" Then hasRestart = True

        ' #### 체크 (4개)
        ElseIf Left(paraText, 4) = "####" Then
            styleName = "기획_□"
            If Mid(paraText, 5, 1) = "$" Then hasRestart = True

        ' ### 체크 (3개)
        ElseIf Left(paraText, 3) = "###" Then
            styleName = "기획_1"
            If Mid(paraText, 4, 1) = "$" Then hasRestart = True

        ' ## 체크 (2개)
        ElseIf Left(paraText, 2) = "##" Then
            styleName = "기획_절절"
            If Mid(paraText, 3, 1) = "$" Then hasRestart = True

        ' # 체크 (1개)
        ElseIf Left(paraText, 1) = "#" Then
            styleName = "기획_장"
            If Mid(paraText, 2, 1) = "$" Then hasRestart = True
        End If

        ' 스타일이 매칭되면 적용
        If styleName <> "" Then
            ' 스타일 적용
            para.Range.Style = styleName

            ' $ 있으면 목록 1부터 새로 시작
            If hasRestart Then
                para.Range.ListFormat.ApplyListTemplate _
                    ListTemplate:=para.Range.ListFormat.ListTemplate, _
                    ContinuePreviousList:=False
            End If

            count = count + 1
        End If
    Next para

    ' 모든 처리 끝난 후 # 문자 삭제
    ' 긴 것부터 삭제 (###### 부터)
    Dim hashPatterns As Variant
    Dim i As Integer

    hashPatterns = Array("###### ", "######", "##### ", "#####", "#### ", "####", "### ", "###", "## ", "##", "# ", "#")

    For i = LBound(hashPatterns) To UBound(hashPatterns)
        With doc.Range.Find
            .Text = hashPatterns(i)
            .Replacement.Text = ""
            .Forward = True
            .Wrap = wdFindContinue
            .Format = False
            .MatchCase = True
            .MatchWholeWord = False
            .Execute Replace:=wdReplaceAll
        End With
    Next i

    MsgBox count & "개의 단락에 스타일을 적용하고 # 기호를 삭제했습니다.", vbInformation
End Sub