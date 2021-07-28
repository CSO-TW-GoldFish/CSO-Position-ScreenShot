import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPlainTextEdit, QPushButton, QLabel

from PIL import Image
from cso_screenshot import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.tooltip = QLabel("請使用視窗化哦! by 崩潰金魚燒 <a href='https://github.com/CSO-TW-GoldFish/CSO-Position-ScreenShot'>Github</a>")
        self.tooltip.setOpenExternalLinks(True)
        self.tooltip.setStyleSheet("color: red;")
        self.setWindowTitle("CSO Studio 截圖自動轉換座標")
        self.convertText = QPlainTextEdit()
        self.convertText.setStyleSheet("font-size: 16px;font-family: Segoe UI")
        self.convertBtn = QPushButton("截圖並轉換")
        self.convertBtn.clicked.connect(self.ScreenShotAndConvertPosition)
        self.convertBtn.setMinimumHeight(60)
        self.clearTextBtn = QPushButton("清除文字")
        self.clearTextBtn.clicked.connect(lambda: self.convertText.clear())

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.tooltip)
        self.mainLayout.addWidget(self.convertText)
        self.mainLayout.addWidget(self.convertBtn)
        self.mainLayout.addWidget(self.clearTextBtn)
        self.setLayout(self.mainLayout)
    
    def ScreenShotAndConvertPosition(self):
        error = ""
        fileName = "position.png"
        newName = "newPosition.png"

        hasImage = screenshot(fileName)
        if not hasImage:
            error = "未偵測到遊戲!"
        else:
            convertGrayImage(fileName, newName)

            img = Image.open(newName)
            text = pytesseract.image_to_string(img, lang='eng',config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789-,[]')

            tmp_pos = text.strip().split(",")

            try:
                x = tmp_pos[0]
                y = tmp_pos[1]
                z = tmp_pos[2]
                error = "{" + f"x = {x}, y = {y}, z = {z}" + "}"
            except IndexError:
                error = "無法分析!"

        self.convertText.appendPlainText(error)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())