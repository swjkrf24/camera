"""
滚动模式 - 控制页面上下滚动
"""

import time
import pyautogui
from .base_mode import BaseMode
from ..core.gestures import GestureType
from ..config import (
    SCROLL_AMOUNT,
    TOP_ZONE_RATIO,
    BOTTOM_ZONE_RATIO,
    SCROLL_COOLDOWN,
)


class ScrollMode(BaseMode):
    """滚动控制模式"""

    def __init__(self):
        super().__init__(
            name="📜 滚动模式",
            description="控制页面滚动"
        )
        self.last_scroll_time = 0
        self.last_action = ""
        self.frame_height = 480  # 默认值，会在运行时更新

    def set_frame_size(self, width, height):
        """设置画面尺寸用于计算触发区域"""
        self.frame_height = height

    def handle_gesture(self, gesture: GestureType, points: dict) -> str:
        """处理手势，执行滚动"""
        current_time = time.time()
        
        # 冷却检查
        if current_time - self.last_scroll_time < SCROLL_COOLDOWN:
            return ""

        action = ""
        
        # 单指指向时，根据位置滚动
        if gesture == GestureType.POINTING and 'index_y' in points:
            index_y = points['index_y']
            top_line = int(self.frame_height * TOP_ZONE_RATIO)
            bottom_line = int(self.frame_height * BOTTOM_ZONE_RATIO)
            
            if index_y < top_line:
                pyautogui.scroll(SCROLL_AMOUNT)
                action = "⬆️ 向上滚动"
            elif index_y > bottom_line:
                pyautogui.scroll(-SCROLL_AMOUNT)
                action = "⬇️ 向下滚动"

        if action:
            self.last_scroll_time = current_time
            self.last_action = action
            
        return action

    def get_overlay_info(self) -> dict:
        """返回覆盖层信息"""
        return {
            'mode_name': self.name,
            'hints': [
                "☝️ 指向顶部 → 向上滚动",
                "☝️ 指向底部 → 向下滚动",
            ],
            'last_action': self.last_action,
            'zones': {
                'top_ratio': TOP_ZONE_RATIO,
                'bottom_ratio': BOTTOM_ZONE_RATIO,
            }
        }

