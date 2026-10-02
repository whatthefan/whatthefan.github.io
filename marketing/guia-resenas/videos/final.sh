#!/bin/bash
# final.sh vN : mezcla HQ + versión web (720p) + póster
cd /tmp/claude-0/guiav; v=$1; F=/tmp/claude-0/bin/ffmpeg; W=/home/user/whatthefan.github.io/public/guia
HQ=1 python3 /home/user/whatthefan.github.io/.claude/skills/motion-reels/scripts/mezcla2.py raw-$v.mov mudo.wav final-$v.mp4 sfx-$v.json
$F -v error -y -i final-$v.mp4 -vf scale=720:1280:flags=lanczos -c:v libx264 -preset slow -crf 25 -profile:v high -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart $W/$v.mp4
$F -v error -y -ss 2.6 -i final-$v.mp4 -frames:v 1 -vf scale=720:1280 -q:v 4 $W/$v.jpg
ls -la final-$v.mp4 $W/$v.mp4
