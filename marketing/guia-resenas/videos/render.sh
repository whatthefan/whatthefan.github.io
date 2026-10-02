#!/bin/bash
cd /tmp/claude-0/guiav
r(){ INTER=h264 node /home/user/whatthefan.github.io/.claude/skills/motion-reels/motor/grabar.js guia.html $1 raw-$1.mov > log-$1.txt 2>&1; }
(r v1; r v4) & (r v2; r v5) & (r v3; r v6) & wait
echo HECHO > render.done
