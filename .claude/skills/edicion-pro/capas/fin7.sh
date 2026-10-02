cd /tmp/claude-0/v3; O=/tmp/claude-0/-home-user-whatthefan-github-io/7b3f125b-7d9a-5895-bb74-0f439706fcca/scratchpad; M=/home/user/whatthefan.github.io/marketing/instagram/sonidos/mixkit/musica-hazy-after-hours.mp3
until grep -q FIN log-m7b.txt; do sleep 10; done
python3 mezcla2.py v-mosca7b.mov voz3-mosca.wav sm7b.mp4 sfx7-mosca.json && python3 musica.py sm7b.mp4 $M $O/PLEA5E-mosca-v8.mp4 20 -19 && echo MOSCA_OK
until grep -q FIN log-u7.txt; do sleep 10; done
python3 mezcla2.py v-uber7.mov voz3-uber.wav su7.mp4 sfx7-uber.json && python3 musica.py su7.mp4 $M $O/PLEA5E-uber-v7.mp4 60 -19 && echo UBER_OK
