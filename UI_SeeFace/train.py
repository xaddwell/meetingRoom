import numpy as np
import os
import cv2


# 创建一个函数，用于从数据集文件夹中获取训练图片,并获取id
# 注意图片的命名格式为User.id.sampleNum
def get_images_and_labels(path):
    image_dir = os.listdir(path)
    # 新建两个list用于存放
    face_samples = []
    ids = []

    for img in image_dir:
        img_path = os.path.join(path, img)
        face = cv2.imread(img_path, 0)
        face_samples.append(face)
        ids.append(int(img[:-6]))
        print(img[:-6])

    return face_samples, ids


# 创建我们的LBPH人脸识别器
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

f, i = get_images_and_labels('train_images')
# for j in range(len(i)):
#     face_recognizer.train(f[j], np.array(i[j]))
#     # 保存模型
#     yml = str(j) + ".yml"
#     rec_f = open(yml, "w+")
#     rec_f.close()
#     face_recognizer.save(yml)


# face_recognizer.read('3.yml')
# for j in range(3):
#     idnum, confidence = face_recognizer.predict(f[2-j])
#     print(idnum, confidence)
