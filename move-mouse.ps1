# Auto Mouse Mover for Windows
# Usage: .\move-mouse.ps1 [interval_seconds]
# Example: .\move-mouse.ps1 60  (moves mouse every 60 seconds)

param(
    [int]$Interval = 60  # Default to 60 seconds if not specified
)

$MoveDistance = 1  # Move mouse by 1 pixel

Write-Host "Auto Mouse Mover started"
Write-Host "Interval: $Interval seconds"
Write-Host "Press Ctrl+C to stop"

# Add required .NET types for mouse control
Add-Type -AssemblyName System.Windows.Forms

# Function to move mouse
function Move-Mouse {
    $currentPos = [System.Windows.Forms.Cursor]::Position
    $x = $currentPos.X
    $y = $currentPos.Y
    
    # Move mouse slightly (1 pixel) and back
    [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point(($x + $MoveDistance), $y)
    Start-Sleep -Milliseconds 100
    [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point($x, $y)
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "$timestamp - Mouse moved"
}

# Main loop
while ($true) {
    Move-Mouse
    Start-Sleep -Seconds $Interval
}

