#!/bin/bash
# exporta.sh pagina.html voz.wav salida.mp4
# Graba la página fotograma a fotograma → mezcla voz + FX de la página en calidad HQ → borra el .mov (≈1,8 GB)
# → si pasa de 29 MB saca además salida-chat.mp4 a dos pasadas (límite de envío por chat: 30 MB).
set -e
D=$(cd "$(dirname "$0")" && pwd); M=$D/../motor
FF=${FFMPEG:-$( [ -x /tmp/claude-0/bin/ffmpeg ] && echo /tmp/claude-0/bin/ffmpeg || which ffmpeg )}
pag=$(realpath "$1"); voz=$(realpath "$2"); out=$(realpath -m "$3"); mov=${out%.mp4}.mov
(cd "$(dirname "$pag")" && node $M/grabar.js "$(basename "$pag")" todo "$mov")
HQ=1 python3 $D/mezcla4.py "$mov" "$voz" "$out" "$pag" && rm -f "$mov"
if [ $(stat -c %s "$out") -gt 29000000 ]; then
  c=${out%.mp4}-chat.mp4; cd /tmp
  $FF -v error -y -i "$out" -c:v libx264 -preset slow -tune film -b:v 7000k -pass 1 -an -f null /dev/null
  $FF -v error -y -i "$out" -c:v libx264 -preset slow -tune film -b:v 7000k -maxrate 12M -bufsize 16M -pass 2 -pix_fmt yuv420p -c:a copy -movflags +faststart "$c"
fi
echo FIN
