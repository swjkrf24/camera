"""
Gesture Control Hub - 主程序入口
用手势控制电脑的一切操作
"""

import cv2
from .config import CAMERA_ID, WINDOW_NAME
from .core.detector import HandDetector
from .core.gestures import GestureRecognizer
from .core.mode_manager import ModeManager
from .ui.overlay import Overlay


def main():
    """主程序入口"""
    print("=" * 50)
    print("  Gesture Control Hub 启动中...")
    print("=" * 50)
    
    # 初始化组件
    detector = HandDetector()
    recognizer = GestureRecognizer()
    mode_manager = ModeManager()
    overlay = Overlay()
    
    # 初始化摄像头
    cap = cv2.VideoCapture(CAMERA_ID)
    if not cap.isOpened():
        print("❌ 错误: 无法打开摄像头")
        return 1
    
    print(f"\n当前模式: {mode_manager.current_mode.name}")
    print("\n操作说明:")
    print("  🖐️ 张开手掌 2 秒 → 切换模式")
    print("  按 'q' 键退出\n")
    
    # 获取画面尺寸
    ret, frame = cap.read()
    if ret:
        h, w = frame.shape[:2]
        mode_manager.set_frame_size(w, h)
    
    # 主循环
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ 错误: 无法读取摄像头帧")
            break
        
        # 镜像翻转
        frame = cv2.flip(frame, 1)
        h, w = frame.shape[:2]
        
        # 检测手部
        landmarks = detector.detect(frame)
        
        # 识别手势
        gesture, points = recognizer.recognize(landmarks, w, h)
        
        # 更新模式管理器
        status = mode_manager.update(gesture, points)
        
        # 绘制手部骨架
        detector.draw_landmarks(frame, landmarks)
        
        # 绘制 UI 覆盖层
        mode_info = mode_manager.current_mode.get_overlay_info()
        overlay.draw(frame, mode_info, points, status)
        
        # 显示画面
        cv2.imshow(WINDOW_NAME, frame)
        
        # 按 'q' 退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # 清理资源
    cap.release()
    cv2.destroyAllWindows()
    detector.close()
    
    print("\n👋 已退出 Gesture Control Hub")
    return 0


if __name__ == "__main__":
    exit(main())

