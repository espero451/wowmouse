import sys
from PyQt6 import QtWidgets, QtGui, QtCore
from Xlib import display
from Xlib.ext import shape


class CursorOverlay(QtWidgets.QWidget):

    def __init__(self, image_path):
        super().__init__()

        # Window flags
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint |
            QtCore.Qt.WindowType.WindowStaysOnTopHint |
            QtCore.Qt.WindowType.BypassWindowManagerHint |
            QtCore.Qt.WindowType.Tool
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        # Load image
        self.original_pixmap = QtGui.QPixmap(image_path)

        # WOW animation state
        self.scale = 1.0
        self.target_scale = 1.0
        self.max_scale = 1.5
        self.animation_speed = 0.25

        # Fixed window size (max scale)
        max_w = int(self.original_pixmap.width() * self.max_scale)
        max_h = int(self.original_pixmap.height() * self.max_scale)
        self.setFixedSize(max_w, max_h)

        # X11 access (click-through)
        self.x_display = display.Display()
        self.root = self.x_display.screen().root

        # Timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(16)  # ~60 FPS

        self.prev_pressed = False

    # Click-through setup
    def showEvent(self, event):
        super().showEvent(event)
        QtCore.QTimer.singleShot(0, self.make_click_through)

    # Make window ignore mouse input
    def make_click_through(self):
        win_id = int(self.winId())
        window = self.x_display.create_resource_object('window', win_id)

        pixmap = window.create_pixmap(1, 1, 1)
        window.shape_mask(
            shape.SO.Set,
            shape.SK.Input,
            0,
            0,
            pixmap
        )
        self.x_display.sync()

    # Main update loop
    def update_frame(self):
        pos = QtGui.QCursor.pos()
        self.move(
            pos.x() - self.width() // 2,
            pos.y() - self.height() // 2
        )

        data = self.root.query_pointer()
        mask = data.mask
        pressed = bool(mask & 0x700)  # Button1/2/3

        if pressed and not self.prev_pressed:
            self.target_scale = self.max_scale
        if not pressed and self.prev_pressed:
            self.target_scale = 1.0

        self.prev_pressed = pressed

        # Smooth interpolation
        self.scale += (self.target_scale - self.scale) * self.animation_speed
        if abs(self.target_scale - self.scale) < 0.001:
            self.scale = self.target_scale

        self.update()

    # Paint scaled image
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.SmoothPixmapTransform)

        scaled_w = int(self.original_pixmap.width() * self.scale)
        scaled_h = int(self.original_pixmap.height() * self.scale)

        scaled = self.original_pixmap.scaled(
            scaled_w,
            scaled_h,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation
        )

        x = (self.width() - scaled_w) // 2
        y = (self.height() - scaled_h) // 2
        painter.drawPixmap(x, y, scaled)


def main():
    app = QtWidgets.QApplication(sys.argv)
    overlay = CursorOverlay("overlay.png")
    overlay.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
