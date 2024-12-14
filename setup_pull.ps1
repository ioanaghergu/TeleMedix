# Variables
$ArchivesToExtract = @(
    "modules\ai_diagnosis_prediction\results.7z.001",
    "modules\ai_diagnosis_prediction\trained_model.7z.001"
)

# Define the base extraction directory
$ExtractionBaseDirResults = "modules\ai_diagnosis_prediction\results"
$ExtractionBaseDirModel = "modules\ai_diagnosis_prediction\trained_model"

# Path to the 7-Zip executable
$SevenZipPath = "C:\Program Files\7-Zip\7z.exe"  # Adjust path if needed

# Extract each archive
foreach ($Archive in $ArchivesToExtract) {
    Write-Host "Processing archive: $Archive"

    # Check if the archive exists before proceeding
    if (-not (Test-Path $Archive)) {
        Write-Host "Archive does not exist: $Archive" -ForegroundColor Red
        continue
    }

    # Determine the extraction folder based on the archive name
    if ($Archive -like "*results*") {
        $DestinationFolder = $ExtractionBaseDirResults
    } elseif ($Archive -like "*trained_model*") {
        $DestinationFolder = $ExtractionBaseDirModel
    } else {
        Write-Host "Unknown archive type: $Archive" -ForegroundColor Red
        continue
    }

    Write-Host "Destination folder: $DestinationFolder"

    # Create the folder if it doesn't exist
    if (-not (Test-Path -Path $DestinationFolder)) {
        Write-Host "Creating folder: $DestinationFolder"
        New-Item -Path $DestinationFolder -ItemType Directory
    }

    # Create a temporary folder for extraction
    $TempFolder = "$DestinationFolder\temp_extract"
    Write-Host "Temporary extraction folder: $TempFolder"
    
    # Create the temporary extraction folder
    if (-not (Test-Path -Path $TempFolder)) {
        New-Item -Path $TempFolder -ItemType Directory
    }

    # Extract the archive using 7-Zip to the temporary folder
    try {
        Write-Host "Extracting $($Archive) to $TempFolder"
        
        # Run the 7-Zip extraction command
        & "$SevenZipPath" x "$Archive" -o"$TempFolder" -y

        # Check if extraction was successful
        if (Test-Path $TempFolder) {
            Write-Host "Extracted $($Archive) to $TempFolder"

            # Flatten the folder structure: move files to the destination folder
            $ExtractedItems = Get-ChildItem -Path $TempFolder -Recurse
            foreach ($Item in $ExtractedItems) {
                # Only move files, not folders
                if (-not $Item.PSIsContainer) {
                    $TargetPath = Join-Path -Path $DestinationFolder -ChildPath $Item.Name
                    Move-Item -Path $Item.FullName -Destination $TargetPath -Force
                    Write-Host "Moved file: $($TargetPath)"
                }
            }

            # Delete all parts of the archive after extraction (e.g., .7z.001, .7z.002)
            $ArchiveParts = Get-ChildItem -Path (Split-Path $Archive) -Filter "$($Archive.Split('\')[-1].Split('.')[0]).7z.*"
            foreach ($Part in $ArchiveParts) {
                Remove-Item -Path $Part.FullName -Force
                Write-Host "Deleted archive part: $($Part.FullName)"
            }

            # Clean up the temporary folder
            Remove-Item -Path $TempFolder -Recurse -Force
            Write-Host "Deleted temporary extraction folder: $TempFolder"
        } else {
            Write-Host "Failed to extract $($Archive)" -ForegroundColor Red
        }
    } catch {
        Write-Host "Error extracting $($Archive): $_" -ForegroundColor Red
    }
}

Write-Host "Extraction completed. Archives have been deleted."
