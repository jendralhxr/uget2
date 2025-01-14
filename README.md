# COMOT: cell counting and motility observation tool

kamerad bersama menghitung  uget-uget


usage: 
```
python run_cellcv.py <file_name> <start_frame> <end_frame> <show_video> <save_result>
python -u trackandcount.py <inputvideo> <start_frame> <end_frame> <cue.mp4> <heat.mp4> <threshold.mp4> [ | tee output.log ] 
```
dependencies: (for the command line version)
- numpy
- opencv_python
- cmapy
- ffmpegcv (and ffmpeg binary installed separately)
