# 定义NDVI数据集路径

$NDVIDir="C:/Users/xueke/Downloads/MOD13A3(NDVI)-China-201703--201802"

$FileDict=@{}

Get-ChildItem -Path $NDVIDir -Filter "*.hdf" | ForEach-Object{
    $DateDOY=($_.FullName -split "\.")[-5].Substring(1,7)
    if (-not $files_dict.ContainsKey($DateDOY)) {
        $files_dict[$DateDOY] = @()
    }
    $files_dict[$DateDOY] += $_.FullName
}

