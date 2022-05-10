import eel
import wx
from video_controller import VideoController
from analyze_video import analyze_video
import cv2
import base64

controller = None

@eel.expose
def get_local_file(wildcard="*"):
  global controller
  app = wx.App(None)
  style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
  dialog = wx.FileDialog(None, 'Open', wildcard="*.mp4", style=style)
  if dialog.ShowModal() == wx.ID_OK:
      path = dialog.GetPath()
  else:
      path = None
  dialog.Destroy()
  controller = VideoController(path)
  return controller.get_video_info()

def convert_frame(frame):
  if frame is None:
    return None
  _, jpg = cv2.imencode('.jpg', frame)
  base64_image = base64.b64encode(jpg)
  return "data:image/jpg;base64," + base64_image.decode("ascii")

@eel.expose
def get_frame():
  global controller
  return convert_frame(controller.next())

@eel.expose
def set_frame(index):
  global controller
  controller.seek(index)

def progress_callback(progress):
  eel.progress(progress)()

@eel.expose
def analyze(key):
  global controller
  if controller is None:
    return None
  return analyze_video(controller, key, progress_callback)

def handle_exit(a, b):
  import sys
  sys.exit(0)

if __name__ == "__main__":
  eel.init("gui/app")
  eel.start(
    "",
    close_callback=handle_exit,
    cmdline_args=[
      '--disable-web-security',
      '–-allow-file-access-from-files'
    ],
    port=8000
  )
