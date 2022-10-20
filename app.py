#app.py
from email.policy import default
from random import randrange
from urllib import response
from flask import Flask, flash, request, redirect, url_for, render_template , send_file , make_response
import numpy
import os
from werkzeug.utils import secure_filename
import cv2          # 匯入 OpenCV 函式庫
from io import BytesIO
import numpy as np  # 引入 numpy 模組
import datetime
from io import StringIO
#import scipy.misc


app = Flask(__name__)

 
UPLOAD_FOLDER = 'static/uploads/'
 
#app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html', showbg = True)
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    #opencv 
    orifile =request.files['file']

    if orifile.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if orifile and allowed_file(orifile.filename):


        ResizeAndSave(orifile)


        return redirect('/display')
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display')
def display_image():    #filename
    file_list = []
    basepath ='./static/uploads/'
    gausspath = './static/gauss'
    basedir = os.walk(basepath)
    gaussdir = os.walk(gausspath)

    nowtime = datetime.datetime.now().strftime('%Y%m%d%H%M%S') #2022 10 18 24:00:00 -> 14位數 
    nowmonth = int ( nowtime[4:6] )
    nowdate  = int ( nowtime[6:8] )
    nowhour  = int ( nowtime[8:10])
    nowminute = int ( nowtime[10:12])

    #imgName = file[0:4]+'/'+file[4:6]+'/'+file[6:8]+' - '+file[8:10]+':'+file[10:12]
    for path, subdirs, files in basedir:
        for file in files:
            #模糊後存檔至gauss資料夾
            defalut = nowtime
            filemonth = int( file[4:6] )  #月份
            filedate  = int( file[6:8] ) #日期
            filehour  = int( file[8:10])  #小時
            fileminute  = int( file[10:12])  #分鐘
            print('nowtime= ' + str(nowtime)  + ' filemonth= ' + str(filemonth) 
            + ' filedate= ' + str(filedate) + ' filehour= ' + str(filehour)+ ' filemin= ' + str(fileminute))

            #try:
            #    default = int(filenum)
            #except:
            #    default = default
            
            #判斷模糊指數的邏輯
            if nowmonth - filemonth >=1 :
                value = 99
            elif nowdate - filedate >= 5:
                value = 99
            else :   #計算模糊指數 模糊指數只能是奇數且整數
                timedelta = nowdate*24*60 + nowhour*60 + nowminute - ( filedate*24*60 + filehour*60 + fileminute )
                value = int (timedelta/60)

            if value>100 :
                print(str(value) + '超出99所以模糊指數為99')
                value=99
            if value%2==0:
                value+=1
            print('value = ' + str(value) )
            GaussianBlur(file , value)
            #value = value + 10  #踩大坑了 因為模糊指數只能是奇數
    for path, subdirs, files in gaussdir:
        for file in files:
            #回傳模糊後的圖片
            file_list.append( file )

    file_list.reverse()# 因為是新的插入在前端 所以list反轉
    #response = render_template("index.html", file_list)
    return render_template("index.html", imagelist=file_list , showbg = False)  
    
 


def ResizeAndSave(img):
    #filename = secure_filename(img.filename)
    #img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #print('upload_image and saved filename: ' + filename)

    #opencv  
    filestr = img.read()
    originalImg = numpy.frombuffer(filestr, numpy.uint8)
    img = cv2.imdecode(originalImg , cv2.IMREAD_UNCHANGED)

    x = 0
    y = 0
    w = 512
    h = 512

    resizeimg = cv2.resize(img, (w, h))   # 產生 512x512 的圖
    # 儲存圖片 save image
    # 第一個參數為圖片路徑(可直接修改副檔名)，第二個為圖片
    # 加上隨機參數以免有檔名重複導致覆蓋掉, 不是最佳解, 但也夠用了, 一秒中抽到同樣數字的機率微乎其微
    path = './static/uploads/'+ datetime.datetime.now().strftime('%Y%m%d%H%M%S')+ str(randrange(100,999)) + '.png'
    cv2.imwrite(path, resizeimg)

def GaussianBlur(file, blurValue):
    #opencv  

    img = cv2.imread('./static/uploads/'+file)  # 讀取圖片
    print("gaussian! img read successfully: "+file)


    # crop_img = img[y:y+h, x:x+w]        # 取出陣列的範圍

    #output1 = cv2.blur(img, (5, 5))     # 指定區域單位為 (5, 5)
    output1 = cv2.GaussianBlur(img,(blurValue, blurValue),0)
    #output2 = cv2.blur(resizeimg, (25, 25))   # 指定區域單位為 (25, 25)

    #cv2.imshow('Gaussian blur', output1)
    #cv2.imshow('G blur', output2)
    #cv2.waitKey(0)                # 設定 0 表示不要主動關閉視窗

    #儲存模糊的圖片
    path = './static/gauss/'+ file
    cv2.imwrite(path, output1)

def serve_pil_image(pil_img):
    img_io = StringIO()
    pil_img.save(img_io, 'png', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


if __name__ == "__main__":
    app.debug = True
    app.run()


#一些網頁垃圾
#    <!--{% if showbg == True %}-->
#    <!-- Background image -->
#    <!-- <img src="{{url_for('static', filename='memorypython.jpg')}}"> -->
#    <!--{% endif %}-->