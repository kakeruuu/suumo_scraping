# xlsxファイルをCSVに変換する
# 関数を含んだエクセルファイルを更新するため

try {

    $item = Get-Item { 変換したいExcelファイルのパス }
    $original_file_path = $item.FullName
    $clone_file_path = $original_file_path -replace ".xlsx", ".csv"

    Remove-Item $clone_file_path
    $excel = New-Object -ComObject Excel.Application            # Excel起動
    $excel.Visible = $false                                     # 表示する・しない
    $book = $excel.Workbooks.Open($original_file_path)      # ブックを開く
 
    $book.SaveAs($clone_file_path, 6)    # Excelを上書き保存する
}
finally {
    $excel.Quit()   # Excelを閉じる
    $excel = $null  # プロセスを開放する
    [GC]::Collect()
}
