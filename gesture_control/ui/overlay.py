"""
UI 覆盖层 - 视觉反馈
"""

import cv2
from ..config import (
    COLOR_GREEN, COLOR_RED, COLOR_YELLOW, COLOR_WHITE,
    COLOR_MAGENTA, COLOR_CYAN,
    FONT_SCALE, FONT_THICKNESS,
    TOP_ZONE_RATIO, BOTTOM_ZONE_RATIO,
)


class Overlay:
    """UI 覆盖层，提供视觉反馈"""

    def __init__(self):
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def draw(self, frame, mode_info, gesture_points, status):
        """
        绘制所有 UI 元素
        
        Args:
            frame: 图像帧
            mode_info: 当前模式信息
            gesture_points: 手势坐标点
            status: 状态信息
        """
        h, w = frame.shape[:2]
        
        # 绘制模式名称
        self._draw_mode_name(frame, mode_info.get('mode_name', ''), w)
        
        # 绘制操作提示
        self._draw_hints(frame, mode_info.get('hints', []), h)
        
        # 绘制滚动区域（如果是滚动模式）
        if 'zones' in mode_info:
            self._draw_scroll_zones(frame, w, h)
        
        # 绘制手指位置指示器
        if gesture_points and 'index_x' in gesture_points:
            self._draw_finger_indicator(
                frame, gesture_points['index_x'], gesture_points['index_y']
            )
        
        # 绘制动作反馈
        if status.get('action'):
            self._draw_action_feedback(frame, status['action'], w)
        
        # 绘制模式切换进度
        if status.get('menu_progress', 0) > 0:
            self._draw_switch_progress(frame, status['menu_progress'], w, h)

    def _draw_mode_name(self, frame, mode_name, width):
        """绘制当前模式名称"""
        cv2.putText(
            frame, mode_name, (10, 30),
            self.font, FONT_SCALE, COLOR_CYAN, FONT_THICKNESS
        )

    def _draw_hints(self, frame, hints, height):
        """绘制操作提示"""
        y = height - 20 - (len(hints) - 1) * 25
        for hint in hints:
            cv2.putText(
                frame, hint, (10, y),
                self.font, 0.5, COLOR_WHITE, 1
            )
            y += 25

    def _draw_scroll_zones(self, frame, w, h):
        """绘制滚动触发区域"""
        top_y = int(h * TOP_ZONE_RATIO)
        bottom_y = int(h * BOTTOM_ZONE_RATIO)
        
        cv2.line(frame, (0, top_y), (w, top_y), COLOR_GREEN, 2)
        cv2.line(frame, (0, bottom_y), (w, bottom_y), COLOR_RED, 2)
        
        cv2.putText(frame, "UP", (w - 50, top_y - 10),
                    self.font, 0.6, COLOR_GREEN, 2)
        cv2.putText(frame, "DOWN", (w - 70, bottom_y + 25),
                    self.font, 0.6, COLOR_RED, 2)

    def _draw_finger_indicator(self, frame, x, y):
        """绘制手指位置指示器"""
        cv2.circle(frame, (x, y), 15, COLOR_MAGENTA, -1)

    def _draw_action_feedback(self, frame, action, width):
        """绘制动作反馈"""
        text_size = cv2.getTextSize(action, self.font, 0.9, 2)[0]
        x = (width - text_size[0]) // 2
        cv2.putText(frame, action, (x, 70),
                    self.font, 0.9, COLOR_YELLOW, 2)

    def _draw_switch_progress(self, frame, progress, w, h):
        """绘制模式切换进度条"""
        bar_width = int(w * 0.6)
        bar_height = 20
        x = (w - bar_width) // 2
        y = h // 2
        
        # 背景
        cv2.rectangle(frame, (x, y), (x + bar_width, y + bar_height),
                      COLOR_WHITE, 2)
        # 进度
        fill_width = int(bar_width * progress)
        cv2.rectangle(frame, (x, y), (x + fill_width, y + bar_height),
                      COLOR_GREEN, -1)
        # 文字
        cv2.putText(frame, "Hold to switch mode...", (x, y - 10),
                    self.font, 0.6, COLOR_WHITE, 2)

