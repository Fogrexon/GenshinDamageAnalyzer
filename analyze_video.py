import cv2
from DamageDetector import Detector as DamageDetector
from EnemyDetector import Detector as EnemyDetector

def analyze_video(video_controller, key, progress_callback):
  video_info = video_controller.get_video_info()
  damage_dropout = int(video_info["fps"] / 10)
  enemy_dropout = int(video_info["fps"] / 2)
  progress_dropout = int(video_info["fps"] / 2)
  frame_infos = {
    "fps": video_info["fps"],
    "frame_count": video_info["frame_count"],
    "frame_width": video_info["frame_width"],
    "frame_height": video_info["frame_height"],
    "damage_dropout": damage_dropout,
    "enemy_dropout": enemy_dropout,
    "damages": [],
    "enemies": []
  }
  frame_count = video_info['frame_count']

  damage_detector = DamageDetector(scale=0.6, key=key)
  enemy_detector = EnemyDetector()
  current_index = 0
  video_controller.seek(current_index)
  
  for i in range(int(frame_count)):
    frame = video_controller.next()
    if frame is None:
      continue

    # damage detection
    if i % damage_dropout == 0:
      damage_info = {"total": 0, "damages": []}
      damages = damage_detector.get_damages(frame)
      for damage in damages:
        damage_info["total"] += damage["number"]
        damage["rect"] = list(damage["rect"])
        damage_info["damages"].append(damage)
      frame_infos["damages"].append(damage_info)
    
    # enemy detection
    if i % enemy_dropout == 0:
      bboxes, clses, scores = enemy_detector.get_enemies(frame)
      max_score_enemy = {"type": "none", "bbox": None, "score": 0}
      for bbox, cls, score in zip(bboxes, clses, scores):
        if score > 0.5 and score > max_score_enemy["score"]:
          max_score_enemy = {"bbox": list(map(int, bbox)), "type": cls, "score": int(score)}
      frame_infos["enemies"].append(max_score_enemy)

    # progress callback
    if i % progress_dropout == 0:
      progress_callback(i / frame_count)
  return frame_infos

    
