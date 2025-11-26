"""
视频模式 - 控制 YouTube / B站 等视频播放
"""

import time
import pyautogui
from .base_mode import BaseMode
from ..core.gestures import GestureType
from ..config import ACTION_COOLDOWN


class VideoMode(BaseMode):
    """视频控制模式"""

    def __init__(self):
        super().__init__(
            name="📺 视频模式",
            description="控制视频播放"
        )
        self.last_action_time = 0
        self.last_action = ""

    def handle_gesture(self, gesture: GestureType, points: dict) -> str:
        """处理手势，执行视频控制"""
        current_time = time.time()
        
        # 冷却检查
        if current_time - self.last_action_time < ACTION_COOLDOWN:
            return ""

        action = ""
        
        if gesture == GestureType.FIST:
            # 握拳 → 播放/暂停 (空格键)
            pyautogui.press('space')
            action = "⏯️ 播放/暂停"
            
        elif gesture == GestureType.SWIPE_RIGHT:
            # 向右挥 → 快进 (按 L 键，YouTube 快进 10 秒，按 3 次 = 30 秒)
            for _ in range(3):
                pyautogui.press('l')
            action = "⏩ 快进 30 秒"
            
        elif gesture == GestureType.SWIPE_LEFT:
            # 向左挥 → 快退 (按 J 键)
            for _ in range(3):
                pyautogui.press('j')
            action = "⏪ 快退 30 秒"

        if action:
            self.last_action_time = current_time
            self.last_action = action
            
        return action

    def get_overlay_info(self) -> dict:
        """返回覆盖层信息"""
        return {
            'mode_name': self.name,
            'hints': [
                "✊ 握拳 → 播放/暂停",
                "👉 右挥 → 快进 30s",
                "👈 左挥 → 快退 30s",
            ],
            'last_action': self.last_action,
        }

