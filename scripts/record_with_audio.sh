ffmpeg -f pulse -ac 1 -ar 48000 -i alsa_output.pci-0000_00_1b.0.analog-stereo.monitor \
-f pulse -ac 2 -ar 44100 \
-i alsa_input.usb-BLUE_MICROPHONE_Blue_Snowball_201306-00.mono-fallback \
-filter_complex amix=inputs=2 \
-video_size 1920x1080 -framerate 60 -f x11grab -i :0.0+0,0 -c:v libx264rgb -crf 0 -preset ultrafast \
sample.mkv
