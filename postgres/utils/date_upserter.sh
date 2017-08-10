#!/bin/bash
set -euo pipefail

while read line; do
    filename_for_postgres=$(echo "$line" | sed s/\'/\'\'/g )
    date=$(exiftool -'FileModifyDate' -t -d '%Y-%m-%d %H:%M:%S' "$HOME/draws/distribute/$line" | cut -d'	' -f2)
    psql -d draws -c "
INSERT INTO draws (name, ctime)
    VALUES ('distribute/$filename_for_postgres', '$date'::timestamptz)
    ON CONFLICT (name) DO UPDATE SET ctime = '$date'::timestamptz;
"
done < $1
