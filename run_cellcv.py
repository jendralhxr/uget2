import sys

from cellcv.analyze_video import VideoAnalyzer

show_video = False
if sys.argv[4].lower() == "true":
    show_video = True
ViNal = VideoAnalyzer(sys.argv[1])
ViNal.analyse(
    start_frame=int(sys.argv[2]), end_frame=int(sys.argv[3]), show_video=show_video
)
