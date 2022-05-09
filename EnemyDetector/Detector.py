import os
import torch
from .Predictor import Predictor
from yolox.exp import get_exp

CLASSES = (
    "cyroreg",
    "andrius",
    "rhodeia",
    "geovishap",
    "pyroreg",
    "mechanicalarray",
    "maguukenki",
    "thundermanifestation",
    "wolfloard"
)

class Detector:
  def __init__(self):
    self.exp = get_exp(os.path.join(os.path.dirname(__file__), "yolox_s.py"))
    self.model = self.exp.get_model()
    self.model.cuda()
    self.model.half()
    self.model.eval()
    self.ckpt = torch.load(os.path.join(os.path.dirname(__file__), "best_ckpt.pth"), map_location="cuda")
    self.model.load_state_dict(self.ckpt["model"])
    self.predictor = Predictor(
      model=self.model,
      exp=self.exp,
      cls_names=CLASSES,
      device="gpu",
      fp16=True
    )
  def get_enemies(self, img):
    outputs, img_info = self.predictor.inference(img)
    if outputs[0] is None:
      return [], [], []
    outputs = outputs[0].cpu()
    ratio = img_info["ratio"]
    if outputs is None:
      return []
    bbox = outputs[:, 0:4]
    bbox /= ratio
    cls = list(map(lambda x: CLASSES[int(x.item())], outputs[:,6]))
    score = outputs[:,4] * outputs[:, 5]
    return bbox, cls, score
