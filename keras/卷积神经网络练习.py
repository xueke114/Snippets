# On Windows
# pip install tensorflow-directml-plugin

import numpy as np
import matplotlib.pyplot as plt
from keras import layers, models
from keras.datasets import mnist
from keras.utils import to_categorical
from keras.losses import categorical_crossentropy

# 使用Sequential类定义模型
model = models.Sequential()
# 添加卷积层，通道数为32或64，卷积窗口是3x3，设置输入张量大小为28x28x1
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
# 添加最大池化层，窗口为2x2
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
# 展平数据为1D
model.add(layers.Flatten())
# relu激活的密集连接层
model.add(layers.Dense(64, activation='relu'))
# 带10个输出softmax激活，对应10个类别
model.add(layers.Dense(10, activation='softmax'))
# 模型概况
print(model.summary())

# 加载数据集
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

train_images = train_images.reshape((60000, 28, 28, 1)).astype('float32') / 255
test_images = test_images.reshape((10000, 28, 28, 1)).astype('float32') / 255

train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

model.compile(optimizer='rmsprop', loss=categorical_crossentropy, metrics=['accuracy'])
model.fit(train_images, train_labels, epochs=5, batch_size=64)

test_loss, test_acc = model.evaluate(test_images, test_labels)
print(f"测试精度：{test_acc}")

# 从mnist中选取一张
digit = test_images[88]
print(f'原始图形尺寸：{digit.shape}')
# 为图像添加一个维度，以适应模型的输入
expand_image = np.expand_dims(digit, axis=0)
print(f'调整后的输入图像尺寸：{expand_image.shape}')
pred = model.predict(expand_image)
print('预测结果\n', pred)
class_=np.argmax(pred[0])
print(f'可以看出第{class_}个label的可能性最大{max(pred[0])*100}%')
print(f'即该图是{class_}的可能性最大')

# 画出来测试图像
plt.imshow(digit, cmap=plt.cm.binary)
plt.show()
