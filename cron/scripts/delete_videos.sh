#!/bin/bash
LOG_FILE="/var/log/ytviewer/video_deletion.log"

set -a
. /app/active.env
set +a

OUTPUT=$(/usr/local/bin/python /app/ytviewer/manage.py delete_old_videos 2>&1)

echo "$(date '+%Y-%m-%d %H:%M:%S') - $OUTPUT" >> "$LOG_FILE" 
