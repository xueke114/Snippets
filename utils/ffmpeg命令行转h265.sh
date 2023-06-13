# 音频保持默认
# 视频编码为h265，视频质量rcf 18（0无损，18-28肉眼无损，libx265默认28）
ffmpeg -i inputfile -c:a copy -c:v libx265 -rcf 18 -preset veryslow -output.mp4