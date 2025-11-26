"""
手势识别器 - 识别各种静态和动态手势
"""

from enum import Enum, auto
from collections import deque
from ..config import SWIPE_THRESHOLD, SWIPE_FRAMES


class GestureType(Enum):
    """手势类型枚举"""
    NONE = auto()           # 无识别手势
    FIST = auto()           # 握拳 ✊
    OPEN_PALM = auto()      # 张开手掌 🖐️
    POINTING = auto()       # 单指指向 ☝️
    SWIPE_LEFT = auto()     # 向左挥手 👈
    SWIPE_RIGHT = auto()    # 向右挥手 👉


class GestureRecognizer:
    """手势识别器"""

    def __init__(self):
        # 用于检测挥手的位置历史
        self.palm_x_history = deque(maxlen=SWIPE_FRAMES)
        self.last_gesture = GestureType.NONE

    def recognize(self, landmarks, frame_width, frame_height):
        """
        识别当前手势
        
        Args:
            landmarks: MediaPipe 手部关键点
            frame_width: 画面宽度
            frame_height: 画面高度
            
        Returns:
            GestureType: 识别的手势类型
            dict: 额外信息（如指尖位置）
        """
        if landmarks is None:
            self.palm_x_history.clear()
            return GestureType.NONE, {}

        # 提取关键点坐标
        points = self._extract_points(landmarks, frame_width, frame_height)
        
        # 检查动态手势（挥手）
        swipe = self._check_swipe(points['palm_x'], frame_width)
        if swipe != GestureType.NONE:
            return swipe, points

        # 检查静态手势
        fingers_up = self._count_fingers_up(landmarks)
        
        if fingers_up == 0:
            return GestureType.FIST, points
        elif fingers_up == 5:
            return GestureType.OPEN_PALM, points
        elif fingers_up == 1 and self._is_index_up(landmarks):
            return GestureType.POINTING, points
        
        return GestureType.NONE, points

    def _extract_points(self, landmarks, w, h):
        """提取关键坐标点"""
        index_tip = landmarks.landmark[8]
        palm = landmarks.landmark[0]  # 手腕作为手掌中心参考
        
        return {
            'index_x': int(index_tip.x * w),
            'index_y': int(index_tip.y * h),
            'palm_x': palm.x,
            'palm_y': palm.y,
        }

    def _count_fingers_up(self, landmarks):
        """计算伸出的手指数量"""
        tips = [8, 12, 16, 20]  # 食指、中指、无名指、小指指尖
        pips = [6, 10, 14, 18]  # 对应的第二关节
        
        count = 0
        # 四指：指尖高于第二关节则认为伸出
        for tip, pip in zip(tips, pips):
            if landmarks.landmark[tip].y < landmarks.landmark[pip].y:
                count += 1
        
        # 大拇指：水平方向判断
        thumb_tip = landmarks.landmark[4]
        thumb_ip = landmarks.landmark[3]
        if abs(thumb_tip.x - thumb_ip.x) > 0.05:
            count += 1
            
        return count

    def _is_index_up(self, landmarks):
        """检查是否只有食指伸出"""
        index_tip = landmarks.landmark[8]
        index_pip = landmarks.landmark[6]
        middle_tip = landmarks.landmark[12]
        middle_pip = landmarks.landmark[10]
        
        index_up = index_tip.y < index_pip.y
        middle_down = middle_tip.y > middle_pip.y
        
        return index_up and middle_down

    def _check_swipe(self, current_x, frame_width):
        """检测挥手动作"""
        self.palm_x_history.append(current_x)
        
        if len(self.palm_x_history) < SWIPE_FRAMES:
            return GestureType.NONE
        
        # 计算移动距离
        start_x = self.palm_x_history[0]
        end_x = self.palm_x_history[-1]
        delta = end_x - start_x
        
        if delta > SWIPE_THRESHOLD:
            self.palm_x_history.clear()
            return GestureType.SWIPE_RIGHT
        elif delta < -SWIPE_THRESHOLD:
            self.palm_x_history.clear()
            return GestureType.SWIPE_LEFT
        
        return GestureType.NONE

