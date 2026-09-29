#!/bin/bash
cd /tmp/claude-0/claude15; rm -f prueba-x-*.png
timeout 900 node /home/user/whatthefan.github.io/.claude/skills/motion-reels/motor/grabar.js claude15.html prueba x "$@" 2>&1 | grep -iE "err|Error" | head -8
F=/tmp/claude-0/bin/ffmpeg; IN=""; n=0; for t in "$@"; do [ -f prueba-x-$t.png ] && { IN="$IN -i prueba-x-$t.png"; n=$((n+1)); }; done
[ $n -eq 1 ] && { $F -v error -y $IN -vf scale=540:-1 hoja.jpg; exit 0; }
L=""; for ((j=0;j<n;j++)); do L="$L$([ $j -gt 0 ] && echo '|')$(( (j%5)*360 ))_$(( (j/5)*640 ))"; done
$F -v error -y $IN -filter_complex "$(for ((j=0;j<n;j++)); do printf "[$j]scale=360:-1[v$j];"; done)$(for ((j=0;j<n;j++)); do printf "[v$j]"; done)xstack=inputs=$n:layout=$L:fill=black" hoja.jpg
