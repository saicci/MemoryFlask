import os
import pathlib
from datetime import datetime
import cv2          # 匯入 OpenCV 函式庫
import io           #byte io使用
import numpy as np  # 引入 numpy 模組

from flask import Flask, url_for, redirect,  render_template, request , flash
from werkzeug.utils import secure_filename
from flask import send_from_directory
from time import strftime

# 取得目前檔案所在的資料夾 
SRC_PATH = pathlib.Path(__file__).parent.absolute()
UPLOAD_FOLDER = os.path.join(SRC_PATH,  'static', 'uploads')
#print(UPLOAD_FOLDER)

app = Flask(__name__)
#app.secret_key =  b'_5#y2L"F4Q8z\n\xec]/'       #  設置密鑰 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER          # 設置儲存上傳檔的資料夾 
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024  * 1024  # 上傳檔最大3MB

# 檢查上傳檔的副檔名 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html" , date = datetime.now())

@app.route("/upload",methods=['POST'])
def upload_file():
    file = request.files['file']  # 取得上傳的檔案

    if file.filename == '':           #  若上傳的檔名是空白的… 
        flash('請選擇要上傳的影像')   # 發出快閃訊息 
        

    if file and allowed_file(file.filename):  # 確認有檔案且副檔名在允許之列
        filename = datetime.now() #轉成時間日期
        flash('影像上傳完畢！')
        # 顯示頁面並傳入上傳的檔名
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('uploaded_file',
                                    filename=filename))

    else:
        flash('僅允許上傳png, jpg, jpeg影像檔')
    return redirect(url_for('index'))   # 令瀏覽器跳回首頁


#對已上傳檔案的訪問服務
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)


@app.route("/result")
def result():
    return render_template("result.html")


if __name__ == "__main__":
    app.run()

    

def GaussianBlur():
    img = cv2.imread('meme.jpg')  # 讀取圖片
    x = 0
    y = 0
    w = 400
    h = 400
    resizeimg = cv2.resize(img, (400, 400))   # 產生 400x400 的圖

    # crop_img = img[y:y+h, x:x+w]        # 取出陣列的範圍
    # cv2.imwrite('output.jpg', crop_img) # 儲存圖片

    cv2.imshow('Square_Size',resizeimg)        # 賦予開啟的視窗名稱，開啟圖片
    output1 = cv2.blur(resizeimg, (5, 5))     # 指定區域單位為 (5, 5)
    output1 = cv2.GaussianBlur(resizeimg, (5, 5),0)
    output2 = cv2.blur(resizeimg, (25, 25))   # 指定區域單位為 (25, 25)

    cv2.imshow('Normal blur', output1)
    cv2.imshow('G blur', output2)
    cv2.waitKey(0)                # 設定 0 表示不要主動關閉視窗

