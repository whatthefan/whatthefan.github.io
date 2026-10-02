#!/bin/bash
# prueba.sh v1 t1 t2 ...
cd /tmp/claude-0/guiav; V=$1; shift; rm -f prueba-$V-*.png
timeout 600 node /home/user/whatthefan.github.io/.claude/skills/motion-reels/motor/grabar.js guia.html prueba $V "$@" 2>&1 | grep -iE "err" | head -5
F=/tmp/claude-0/bin/ffmpeg; IN=""; n=0; for t in "$@"; do [ -f prueba-$V-$t.png ] && { IN="$IN -i prueba-$V-$t.png"; n=$((n+1)); }; done
L=""; for ((j=0;j<n;j++)); do L="$L$([ $j -gt 0 ] && echo '|')$(( (j%6)*270 ))_$(( (j/6)*480 ))"; done
$F -v error -y $IN -filter_complex "$(for ((j=0;j<n;j++)); do printf "[$j]scale=270:480[v$j];"; done)$(for ((j=0;j<n;j++)); do printf "[v$j]"; done)xstack=inputs=$n:layout=$L:fill=black" hoja.jpg
