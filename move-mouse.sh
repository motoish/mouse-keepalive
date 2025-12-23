#!/bin/bash

# Auto Mouse Mover for macOS
# Usage: ./move-mouse.sh [interval_seconds]
# Example: ./move-mouse.sh 60  (moves mouse every 60 seconds)

INTERVAL=${1:-60}  # Default to 60 seconds if not specified
MOVE_DISTANCE=1    # Move mouse by 1 pixel

echo "Auto Mouse Mover started"
echo "Interval: ${INTERVAL} seconds"
echo "Press Ctrl+C to stop"

# Function to move mouse
move_mouse() {
    # Get current mouse position
    CURRENT_POS=$(osascript -e 'tell application "System Events" to get position of mouse')
    
    # Extract x and y coordinates
    X=$(echo $CURRENT_POS | awk '{print $1}')
    Y=$(echo $CURRENT_POS | awk '{print $2}')
    
    # Move mouse slightly (1 pixel) and back
    osascript -e "tell application \"System Events\" to set position of mouse to {$(($X + $MOVE_DISTANCE)), $Y}"
    sleep 0.1
    osascript -e "tell application \"System Events\" to set position of mouse to {$X, $Y}"
    
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Mouse moved"
}

# Main loop
while true; do
    move_mouse
    sleep $INTERVAL
done

