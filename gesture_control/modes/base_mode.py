"""
模式基类 - 定义模式接口
"""

from abc import ABC, abstractmethod
from ..core.gestures import GestureType


class BaseMode(ABC):
    """所有控制模式的基类"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def handle_gesture(self, gesture: GestureType, points: dict) -> str:
        """
        处理手势输入
        
        Args:
            gesture: 识别的手势类型
            points: 手势相关的坐标信息
            
        Returns:
            str: 执行的动作描述，如果没有执行动作则返回空字符串
        """
        pass

    @abstractmethod
    def get_overlay_info(self) -> dict:
        """
        获取覆盖层显示信息
        
        Returns:
            dict: 包含需要显示的信息
        """
        pass

    def __str__(self):
        return f"{self.name}: {self.description}"

