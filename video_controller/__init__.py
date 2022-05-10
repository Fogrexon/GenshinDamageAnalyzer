import cv2

class VideoController:
  def __init__(self, video_path):
    self.path = video_path
    self.video = cv2.VideoCapture(video_path)
    self.fps = self.video.get(cv2.CAP_PROP_FPS)
    self.frame_count = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
    self.frame_width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
    self.frame_height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    self.frame_index = 0

  def get_video_info(self):
    return dict(
      path=self.path,
      fps=self.fps,
      frame_count=self.frame_count,
      frame_width=self.frame_width,
      frame_height=self.frame_height,
      current=self.frame_index
    )

  def next(self):
    self.frame_index += 1
    self.frame_index = min(max(self.frame_index, 0), self.frame_count - 1)
    ret, frame = self.video.read()
    if not ret:
      return None
    return frame

  def prev(self):
    self.frame_index -= 1
    self.frame_index = min(max(self.frame_index, 0), self.frame_count - 1)
    self.video.set(cv2.CAP_PROP_POS_FRAMES, self.frame_index)
    ret, frame = self.video.read()
    if not ret:
      return None
    return frame

  def seek(self, frame_index):
    self.frame_index = frame_index
    self.frame_index = min(max(self.frame_index, 0), self.frame_count - 1)
    self.video.set(cv2.CAP_PROP_POS_FRAMES, self.frame_index)
