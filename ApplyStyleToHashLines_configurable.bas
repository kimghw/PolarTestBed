Sub ApplyStyleToHashLines_configurable()
    ' 시작 레벨을 선택할 수 있는 마크다운 스타일 적용 매크로
    ' 예: startLevel = 1 이면 # -> 기획_□, ## -> 기획_ㅇ, ### -> 기획_-
    '     startLevel = 3 이면 ### -> 기획_□, #### -> 기획_ㅇ, ##### -> 기획_-

    Dim doc As Document
    Dim para As Paragraph
    Dim count As Integer
    Dim paraText As String
    Dim styleName As String
    Dim hasRestart As Boolean
    Dim startLevel As Integer
    Dim userInput As String
    Dim hashPatterns As Variant
    Dim i As Integer

    ' 사용자에게 시작 레벨 입력 받기
    userInput = InputBox( _
        "시작 레벨을 입력하세요 (1-6):" & vbCrLf & vbCrLf & _
        "1 = #부터 시작" & vbCrLf & _
        "2 = ##부터 시작" & vbCrLf & _
        "3 = ###부터 시작" & vbCrLf & _
        "4 = ####부터 시작" & vbCrLf & _
        "5 = #####부터 시작" & vbCrLf & _
        "6 = ######부터 시작", _
        "마크다운 시작 레벨 선택", _
        "3")

    ' 취소 또는 빈 입력 처리
    If userInput = "" Then
        MsgBox "취소되었습니다.", vbInformation
        Exit Sub
    End If

    ' 숫자 검증
    If Not IsNumeric(userInput) Then
        MsgBox "숫자를 입력해주세요.", vbExclamation
        Exit Sub
    End If

    startLevel = CInt(userInput)

    ' 범위 검증
    If startLevel < 1 Or startLevel > 6 Then
        MsgBox "1부터 6 사이의 숫자를 입력해주세요.", vbExclamation
        Exit Sub
    End If

    Set doc = ActiveDocument
    count = 0

    ' 시작 레벨에 따른 # 문자열 생성
    Dim level1Str As String
    Dim level2Str As String
    Dim level3Str As String

    level1Str = String(startLevel, "#")
    level2Str = String(startLevel + 1, "#")
    level3Str = String(startLevel + 2, "#")

    ' 모든 단락을 검색
    For Each para In doc.Paragraphs
        paraText = Trim(para.Range.Text)
        styleName = ""
        hasRestart = False

        ' level3 체크 (가장 긴 것부터)
        If Left(paraText, Len(level3Str)) = level3Str Then
            ' 다음 문자가 #가 아닌지 확인 (더 긴 패턴 제외)
            If Len(paraText) > Len(level3Str) Then
                If Mid(paraText, Len(level3Str) + 1, 1) <> "#" Then
                    styleName = "기획_-"
                    If Mid(paraText, Len(level3Str) + 1, 1) = "$" Then hasRestart = True
                End If
            Else
                styleName = "기획_-"
            End If

        ' level2 체크
        ElseIf Left(paraText, Len(level2Str)) = level2Str Then
            If Len(paraText) > Len(level2Str) Then
                If Mid(paraText, Len(level2Str) + 1, 1) <> "#" Then
                    styleName = "기획_ㅇ"
                    If Mid(paraText, Len(level2Str) + 1, 1) = "$" Then hasRestart = True
                End If
            Else
                styleName = "기획_ㅇ"
            End If

        ' level1 체크
        ElseIf Left(paraText, Len(level1Str)) = level1Str Then
            If Len(paraText) > Len(level1Str) Then
                If Mid(paraText, Len(level1Str) + 1, 1) <> "#" Then
                    styleName = "기획_□"
                    If Mid(paraText, Len(level1Str) + 1, 1) = "$" Then hasRestart = True
                End If
            Else
                styleName = "기획_□"
            End If
        End If

        ' 스타일이 매칭되면 적용
        If styleName <> "" Then
            ' 스타일 적용
            On Error Resume Next
            para.Range.Style = styleName
            If Err.Number <> 0 Then
                MsgBox "스타일 '" & styleName & "'을(를) 찾을 수 없습니다." & vbCrLf & _
                       "문서에 해당 스타일이 정의되어 있는지 확인하세요.", vbExclamation
                Exit Sub
            End If
            On Error GoTo 0

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
    ' 긴 것부터 삭제
    ReDim hashPatterns(0 To 5) As String

    For i = startLevel + 2 To startLevel Step -1
        Dim hashStr As String
        hashStr = String(i, "#")

        ' 공백 있는 패턴
        With doc.Range.Find
            .Text = hashStr & " "
            .Replacement.Text = ""
            .Forward = True
            .Wrap = wdFindContinue
            .Format = False
            .MatchCase = True
            .MatchWholeWord = False
            .Execute Replace:=wdReplaceAll
        End With

        ' 공백 없는 패턴
        With doc.Range.Find
            .Text = hashStr
            .Replacement.Text = ""
            .Forward = True
            .Wrap = wdFindContinue
            .Format = False
            .MatchCase = True
            .MatchWholeWord = False
            .Execute Replace:=wdReplaceAll
        End With
    Next i

    MsgBox "시작 레벨: " & level1Str & vbCrLf & _
           count & "개의 단락에 스타일을 적용하고 # 기호를 삭제했습니다." & vbCrLf & vbCrLf & _
           level1Str & " -> 기획_□" & vbCrLf & _
           level2Str & " -> 기획_ㅇ" & vbCrLf & _
           level3Str & " -> 기획_-", _
           vbInformation, "완료"
End Sub
