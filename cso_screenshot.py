from win32gui import FindWindow, GetWindowRect, GetWindowDC, DeleteObject, ReleaseDC
from win32ui import CreateDCFromHandle, CreateBitmap
from win32con import SRCCOPY
from PIL.Image import frombuffer
import cv2 as cv
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# source https://www.programmersought.com/article/37942783573/
def screenshot(name):
    hWnd = FindWindow(None, "Counter-Strike Online")
    if not hWnd: return None
    left, top, right, bot = GetWindowRect(hWnd)
    width = right - left
    height = bot - top
    x = int(width / 2) + 10
    y = int(height / 2) + 15

    hWndDC = GetWindowDC(hWnd)
    mfcDC = CreateDCFromHandle(hWndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = CreateBitmap()

    saveBitMap.CreateCompatibleBitmap(mfcDC,125,27)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((-x,-y), (width,height), mfcDC, (0, 0), SRCCOPY)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im_PIL = frombuffer('RGB',(bmpinfo['bmWidth'],bmpinfo['bmHeight']),bmpstr,'raw','BGRX',0,1)

    DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    ReleaseDC(hWnd,hWndDC)

    im_PIL.save(name)
    return True


def convertGrayImage(name, newName):
    # 載入圖片
    img = cv.imread(name)
    # 改變圖片尺吋
    img = cv.resize(img, (img.shape[1] * 2, img.shape[0] * 2))
    # 灰階
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, thresh = cv.threshold(gray, 200, 255, cv.THRESH_BINARY)
    cv.imwrite(newName, thresh)
