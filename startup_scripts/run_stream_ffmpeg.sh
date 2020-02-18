#!/bin/bash -x

sleep 1m

while :
do

wget -q --spider https://google.com
if [ $? -eq 0 ]; then
    echo "Internet access available"
    ffmpeg -rtsp_transport tcp -i rtsp://192.168.0.10:8554/CH001.sdp -f mpegts -s 1280x1200 -codec:v mpeg1video -b:v 3000k -framerate 30 -r 30 -bf 0 https://cloud-track.herokuapp.com/cloudtrackinglivestream
else
    echo "No internet, retrying..."
    sleep 30
    continue
fi
done
