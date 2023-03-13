import sys

from cellcv.analyze_video import VideoAnalyzer

"""
Arguments:
    [1] video file path
    [2] starting frame number
    [3] end frame number
    [4] show video during analizing (true/false)
    [5] save result to a csv (true/false)
"""

show_video = False
if sys.argv[4].lower() == "true":
    show_video = True
ViNal = VideoAnalyzer(sys.argv[1])
ViNal.analyse(
    start_frame=int(sys.argv[2]), end_frame=int(sys.argv[3]), show_video=show_video
)

if sys.argv[5] == "true":
    ViNal.save_result_to_file()
