#!/bin/bash
LOG_FILE="/var/log/ytviewer/video_deletion.log"

# Activate the environment
set -a
. /app/active.env
set +a

# Catch the output
OUTPUT=$(/usr/local/bin/python /app/ytviewer/manage.py delete_old_videos 2>&1)

# Log the data
echo "$(date '+%Y-%m-%d %H:%M:%S') - $OUTPUT" >> "$LOG_FILE" 
