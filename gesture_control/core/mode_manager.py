"""
模式管理器 - 管理模式切换
"""

import time
from ..config import PALM_HOLD_TIME
from ..core.gestures import GestureType
from ..modes.video_mode import VideoMode
from ..modes.scroll_mode import ScrollMode


class ModeManager:
    """模式管理器，处理模式切换逻辑"""

    def __init__(self):
        # 注册可用模式
        self.modes = [
            VideoMode(),
            ScrollMode(),
        ]
        self.current_mode_index = 0
        
        # 模式切换状态
        self.palm_start_time = None
        self.is_showing_menu = False
        self.menu_selection = 0

    @property
    def current_mode(self):
        """获取当前模式"""
        return self.modes[self.current_mode_index]

    def update(self, gesture: GestureType, points: dict) -> dict:
        """
        更新状态，处理模式切换和手势
        
        Returns:
            dict: 包含动作结果和状态信息
        """
        result = {
            'action': '',
            'showing_menu': False,
            'menu_progress': 0,
            'switched_mode': False,
        }

        # 检测张开手掌（用于切换模式）
        if gesture == GestureType.OPEN_PALM:
            if self.palm_start_time is None:
                self.palm_start_time = time.time()
            
            elapsed = time.time() - self.palm_start_time
            result['menu_progress'] = min(elapsed / PALM_HOLD_TIME, 1.0)
            
            if elapsed >= PALM_HOLD_TIME:
                # 切换到下一个模式
                self._switch_to_next_mode()
                self.palm_start_time = None
                result['switched_mode'] = True
                result['action'] = f"切换到 {self.current_mode.name}"
        else:
            self.palm_start_time = None
            
            # 非张开手掌时，交给当前模式处理
            action = self.current_mode.handle_gesture(gesture, points)
            result['action'] = action

        return result

    def _switch_to_next_mode(self):
        """切换到下一个模式"""
        self.current_mode_index = (self.current_mode_index + 1) % len(self.modes)

    def set_frame_size(self, width, height):
        """设置画面尺寸（传递给需要的模式）"""
        for mode in self.modes:
            if hasattr(mode, 'set_frame_size'):
                mode.set_frame_size(width, height)

