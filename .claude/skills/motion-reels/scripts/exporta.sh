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
if [ -f "$out" ] && [ $(stat -c %s "$out") -gt 29000000 ]; then
  c=${out%.mp4}-chat.mp4; cd /tmp
  dur=$($FF -i "$out" 2>&1 | grep -oP "Duration: \K[0-9:.]+" | awk -F: '{print $1*3600+$2*60+$3}'); vb=$(awk -v d=$dur 'BEGIN{printf "%d", 27.5*8000/d-300}')   # kbps para ~28 MB
  $FF -v error -y -i "$out" -c:v libx264 -preset slow -tune film -b:v ${vb}k -pass 1 -an -f null /dev/null
  $FF -v error -y -i "$out" -c:v libx264 -preset slow -tune film -b:v ${vb}k -maxrate $((vb*2))k -bufsize $((vb*3))k -pass 2 -pix_fmt yuv420p -c:a copy -movflags +faststart "$c"
fi
echo FIN
