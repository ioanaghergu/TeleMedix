# Variables
$FoldersToArchive = @(
    "modules\ai_diagnosis_prediction\results",
    "modules\ai_diagnosis_prediction\trained_model"
)
$MaxSize = 100MB  # Size limit for each part in bytes
$SevenZipPath = "C:\Program Files\7-Zip\7z.exe"  # Path to 7-Zip executable (adjust if needed)
$ArchiveDestination = "modules\ai_diagnosis_prediction"

# Archive each folder individually
foreach ($Folder in $FoldersToArchive) {
    # Get the folder name (last part of the path)
    $FolderName = Split-Path -Leaf $Folder
    $ParentDir = Split-Path -Parent $Folder
    $ArchiveName = Join-Path -Path $ArchiveDestination -ChildPath "$FolderName.7z"

    # Create a multi-part archive using 7-Zip
    $arguments = "a", "$ArchiveName", "$Folder", "-v$($MaxSize)", "-mx=9"  # -v for split size, -mx=9 for max compression
    & $SevenZipPath @arguments

    # Check if the archive parts were created successfully
    If (Test-Path "$ArchiveDestination\$FolderName.7z.001") {
        Write-Host "Archived $Folder to $ArchiveDestination\$FolderName.7z"
        
        # Remove the original folder after archiving
        Remove-Item -Path $Folder -Recurse -Force
        Write-Host "Deleted original folder: $Folder"
    } Else {
        Write-Host "Failed to archive $Folder" -ForegroundColor Red
    }
}

Write-Host "Archiving completed. Archives are located under their respective destination folders."
