from keras.models import Sequential, load_model
from keras.layers import Dropout, Dense, Activation, Conv2D, MaxPooling2D, Flatten
from keras import backend as K
import os as OS
import numpy as NP
from PIL import Image
import glob as Glob

# 分割圖片 1 to 4
def DivideImage(img, number_str):
    number_batch = []
    n_idx = 0
    for n in number_str:
        if n_idx < 4:
            number_batch.append([1 if int(n) == t else 0 for t in range(10)])
        else:
            break
        n_idx += 1
    img_batch = []
    for sp in range(4):
        tmp_data = [[[0] for _ in range(31)] for __ in range(24)]
        for h in range(24):
            for w in range(sp * 31, (sp + 1) * 31):
                r, g, b = img.getpixel((w, h))
                tmp_w = w - sp * 31
                tmp_data[h][tmp_w][0] = (r * 0.299 + g * 0.587 + b * 0.114) / 255.0
        img_batch.append(tmp_data)
    return img_batch, number_batch
    '''
    (4, 24, 31, 1), (4, 10)
    '''

# 讀取預測圖片
def LoadForwardData(filepath):
    img = Image.open(filepath).convert('RGB')
    number_str = OS.path.split(filepath)[1].split('.')[0]
    return DivideImage(img, number_str)
    '''
    (4, 24, 31, 1), (4, 10)
    '''

# 讀取訓練圖片
def LoadTrainDatas():
    train_data_folder = './static/img/validcode/'
    img_list = []
    number_str_list = []
    for filename in Glob.glob(train_data_folder + '*.jpg'):
        number_str_list.append(OS.path.split(filename)[1].split('.')[0])
        img = Image.open(filename).convert('RGB')
        img_list.append(img)
    img_batch = []
    number_batch = []
    for idx in range(len(img_list)):
        img_b, number_b = DivideImage(img_list[idx], number_str_list[idx])
        img_batch += img_b
        number_batch += number_b
    return img_batch, number_batch
    '''
    (None, 24, 31, 1), (None, 10)
    '''

class ValidCode(object):
    def __init__(self):
        self.FolderPath = '.'
        self.ModelName = 'ValidCode'
        self.Model = None
        self.Build()
        self.Load()

    def Forward(self, images):
        images = NP.array(images)
        result = ''
        for n in self.Model.predict_classes(images):
            result += str(n)
        return result

    def Train(self, image_batch, number_batch, validation_split = 0.2, epochs = 5, batch_size = 128, display = True):
        '''
        validation_split = 驗證 / (訓練 + 驗證)
        epochs = 訓練週期
        batch_size = 每次訓練量
        '''
        image_batch = NP.array(image_batch)
        number_batch = NP.array(number_batch)
        return self.Model.fit(x = image_batch, y = number_batch, validation_split = validation_split, epochs = epochs, batch_size = batch_size, verbose = 2 if display else 1)

    def Build(self):
        K.clear_session()
        self.Model = Sequential()
        self.Model.add(Conv2D(
            input_shape = (24, 31, 1),
            filters = 16,
            kernel_size = (5, 5),
            padding = 'same',
            activation = 'relu'
        ))
        self.Model.add(MaxPooling2D(2, 2))
        self.Model.add(Conv2D(
            filters = 32,
            kernel_size = (5, 5),
            padding = 'same',
            activation = 'relu'
        ))
        self.Model.add(MaxPooling2D(2, 2))
        self.Model.add(Dropout(0.25))
        self.Model.add(Flatten())
        self.Model.add(Dense(128, activation = 'relu'))
        self.Model.add(Dropout(0.5))
        self.Model.add(Dense(10, activation = 'softmax'))
        self.Model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    def Summary(self):
        return self.Model.summary()

    def ModelPath(self):
        folder = './' + self.ModelName
        if not OS.path.exists(folder):
            OS.makedirs(folder)
        return OS.path.join(folder, self.ModelName + '.model')

    def Save(self):
        try:
            self.Model.save(self.ModelPath())
            print('Success save model:', self.ModelPath())
        except:
            print('Cannot save model:', self.ModelPath())

    def Load(self):
        try:
            self.Model = load_model(self.ModelPath())
            print('Success load model:', self.ModelPath())
        except:
            print('Cannot load model:', self.ModelPath())
