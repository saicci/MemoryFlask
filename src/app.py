import os
import pathlib
from datetime import datetime
import cv2          # 匯入 OpenCV 函式庫
import io           #byte io使用
import numpy as np  # 引入 numpy 模組
import uuid
from flask import Flask, url_for, redirect,  render_template, request , flash , make_response
from werkzeug.utils import secure_filename
from flask import send_from_directory
from time import strftime

UPLOAD_FOLDER = "static/uploads"

# 靜態路由設定
app = Flask(__name__,
           
            template_folder='template',
            )

app.secret_key =  'key'       #  設置密鑰 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER          # 設置儲存上傳檔的資料夾 
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024  * 1024  # 上傳檔最大3MB

# 檢查上傳檔的副檔名 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)



if __name__ == "__main__":
    app.debug = True
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

