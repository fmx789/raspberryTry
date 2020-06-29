"""
本程序使用k-nearest-neighbors (KNN)算法进行人脸识别，
在可行的计算时间内对未知的人进行预测，
并且支持对多个人同时识别。
算法描述:
knn分类器首先在一组被标记(已知)的面孔上进行训练，然后可以
通过在它的训练集中寻找k个最相似的面孔(在欧几里得距离下具有
最近似的面孔特征的图像)，使得在实时视频流中预测出这个人，
并在他们的标签上执行多数投票算法(可能加权)。
例如，k=3，在训练集中与给定图像最接近的三张人脸中一张是A的图像，
另两张是B的图像，预测结果为B
这种方法使用了加权投票，这样会使得较近的邻居投票权重更大

人脸识别结果通过建立socket通信发往服务端

结构：
dataset/
    ├── <person1>/
    │   ├── <somename1>.jpg
    │   ├── <somename2>.jpg
    │   ├── ...
    ├── <person2>/
    │   ├── <somename1>.jpg
    │   └── <somename2>.jpg
clientnew.py
trained_knn_model.clf
"""
import socket
import time
import sys

import cv2
import math
from sklearn import neighbors
import os
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import numpy as np

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'JPG'}#支持的图像格式

"""
训练knn分类器模型
参数：
train_dir：训练集文件夹路径
model_save_path（可选）：模型保存路径，未指定则自动选择
n_neighbors（可选）：分类中权衡的邻居数量，未指定则自动选择
knn_algo（可选）：支持knn的底层数据结构
verbose：训练的冗长
返回在给定数据上训练的knn分类器。
"""
def train(train_dir, model_save_path=None, n_neighbors=None, knn_algo='ball_tree', verbose=False):
    X = []
    y = []

    # 循环遍历训练集中的每个人
    for class_dir in os.listdir(train_dir):
        if not os.path.isdir(os.path.join(train_dir, class_dir)):
            continue

        # 循环遍历当前人的每个训练图像
        for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):
            image = face_recognition.load_image_file(img_path)
            face_bounding_boxes = face_recognition.face_locations(image)

            if len(face_bounding_boxes) != 1:
                # 如果训练图像中没有人或人太多，跳过图像。
                if verbose:
                    print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(face_bounding_boxes) < 1 else "Found more than one face"))
            else:
                # 将当前图像的人脸编码添加到训练集中
                X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
                y.append(class_dir)

    # 确定在KNN分类器中使用多少邻居进行加权
    if n_neighbors is None: #未指定邻居数
        n_neighbors = int(round(math.sqrt(len(X))))
        if verbose:
            print("Chose n_neighbors automatically:", n_neighbors)

    # 创建并训练KNN分类器
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    knn_clf.fit(X, y)

    # 保存训练好的KNN分类器
    if model_save_path is not None:
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)

    return knn_clf

"""
使用训练好的KNN分类器识别给定图像中的人脸
参数：
X_frame：做预测的帧
knn_clf（可选）：如果该项未指定，则model_save_path必须指定
model_path（可选）：knn分类器的路径。如果没有指定，model_save_path必须是knn_clf
distance_threshold（可选）：人脸分类的距离阈值。它越大，把不认识的人错当成认识的人概率就越大
返回图像中已识别面孔的名称和面孔位置列表[(name,bounding box),…]
不认识的人的面孔，name将会是“unknown”
"""
def predict(X_frame, knn_clf=None, model_path=None, distance_threshold=0.45): #0.6
    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")

    # 加载一个训练好的KNN模型
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)

    X_face_locations = face_recognition.face_locations(X_frame)

    # 如果在图像中找不到面孔，返回空
    if len(X_face_locations) == 0:
        return []

    # 找到测试图像中人脸的编码
    faces_encodings = face_recognition.face_encodings(X_frame, known_face_locations=X_face_locations)

    # 使用KNN模型为测试人脸找到最佳匹配
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]

    # 预测结果，并删除超出阈值的结果
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]

"""
识别结果显示函数
参数：
frame：显示预测的帧
predictions：预测函数的结果
"""
def show_prediction_labels_on_image(frame, predictions):
    pil_image = Image.fromarray(frame)
    draw = ImageDraw.Draw(pil_image)

    for name, (top, right, bottom, left) in predictions:
        # 放大对全尺寸图像的预测
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        # 用Pillow模块在脸部周围画一个框
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
        name = name.encode("UTF-8")

        # 在人脸下面画一个表示学号的标签
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

    del draw
    # 以open-cv格式保存图像，以便能够显示它

    opencvimage = np.array(pil_image)
    return opencvimage

if __name__ == "__main__":
    # 训练部分
    #print("Training KNN classifier...")
    #classifier = train("dataset", model_save_path="trained_knn_model.clf", n_neighbors=2)
    #classifier = train("dataset", model_save_path="trained_knn_model.clf")
    #print("Training complete!")
    
    # 获取树莓派视频流
    # 每10帧处理一帧以提高速度
    process_this_frame = 9
    print('Setting cameras up...')
    url = 'http://192.168.43.122:8080/?action=stream?dummy=param.mjpg'
    # 网络摄像头
    cap = cv2.VideoCapture(url)
    print('connetct camera ok')
    # 上报流程中人脸识别结果预设值
    pre = 'unknown'

    # 设置ip和端口
    host = '192.168.43.122'
    port = 5000
    print("client open")
    # 套接字接口
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 连接树莓派
    while True:
        try:
            mySocket.connect((host, port)) # 连接到树莓派
            print("connect to server")
            break
        except :                           # 连接不成功，运行最初的ip
            print ('connect fail')
            time.sleep(1)
            continue
    
    # 连接成功将识别结果返回    
    while True:

        ret, frame = cap.read()
        if ret:
            # 图像调整以获取更稳定的视频流
            img = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            process_this_frame = process_this_frame + 1
            if process_this_frame % 10 == 0:
                predictions = predict(img, model_path="trained_knn_model.clf")
            frame = show_prediction_labels_on_image(frame, predictions)
            cv2.imshow('camera', frame)
            if len(predictions) < 2:
                # 检测到只有一个人时才上报
                for name, (top, right, bottom, left) in predictions:
                    if name != 'unknown':
                        # 仅当识别出已知身份时上报，且同一名字短时间只上报一次，避免频繁发送
                        if name != pre:
                            flag = 1
                            name=name.encode("utf-8")# 上报检测的身份
                            mySocket.send(name)
                            print(name)
                            print("发送完成") 
                        if flag:
                            pre = name.decode("utf-8")
                            flag = 0

            # 跳出循环以关闭socket连接、关闭摄像头
            if ord('q') == cv2.waitKey(1):
                break
    mySocket.send('close'.encode("utf-8"))
    mySocket.close()
    mySocket=None
    cap.release() 
    cv2.destroyAllWindows()
    sys.exit(1)
