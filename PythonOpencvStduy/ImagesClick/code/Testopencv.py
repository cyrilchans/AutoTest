import cv2
import numpy as np
import cv2 as cv
#
# # 读取图像   默认格式bgr  第二个参数表示读取类型
# p1 = cv.imread('../pictrue/img_3.png')
# # print(p1)
# # 改变图片大小
# # p2 = cv.resize(p1, (200, 200))
#
# # 保存图像  第一参数属性名， 第二参数保存格式
# # cv.imwrite()
#
# # 颜色提取通道
# # b, g, r = cv.split(p1)
# # 还原
# # img = cv2.merge((b,g,r))
#
# # 边界填充   上下左右指定值  第三个参数是选择填充方式
# # top, bottom, left, right = (50, 50, 50, 50)
# #
# # re1 = cv.copyMakeBorder(p1, top, bottom, left, right, cv.BORDER_CONSTANT)
#
# # 数值计算
# # p2 = p1+100
# # print(p2)
#
# # 图像融合  shape值要一致， 然后添加权重
# # t1 = cv.addWeighted(img1,0.4, img2, 0.6, 0)
#
# # 图像阈值
# # 超过阈值部分取最大值   简单来说就是暗的更暗 白的更白
# # ret, p2 = cv.threshold(p1, 127, 255, cv.THRESH_BINARY)
# # 反转
# # ret, p2 = cv.threshold(p1, 127, 255, cv.THRESH_BINARY_INV)
#
# # 图像平滑   处理噪音点
# # 均值滤波
# # 简单的平均卷积操作
# # blur = cv.blur(p1, (3,  3))
# # 方框滤波
# # 基本和均值一样，可以选择归一化   normalize 是否做归一化
# # box = cv.boxFilter(p1, -1, (3,3), normalize=True)
# # 高斯滤波 (较好的处理噪点方法)
# # 高斯模糊的卷积核里的数值是满足高斯分布，相当于更重视中间的
# # gaussian = cv.GaussianBlur(p1, (5,5),1)
# # 中值滤波 (处理噪点好的方法)
# # media = cv.medianBlur(p1, 5)
#
# # 展示所有的 拼在一起
# # np.hstack
#
#
# # 形态学-腐蚀操作
# # kernel = np.ones((30,30),np.uint8)
# # erode_1 = cv2.erode(p1.kernel, iterations=1)
# # 膨胀
# # dilate_1 = cv2.dilate(p1.kernel, iterations=1)
#
# # 开运算闭运算
# # 先腐蚀在膨胀
# # opening = cv2.morphologyEx(p1, cv.MORPH_OPEN,kernel)
# # 先膨胀在腐蚀
# # opening = cv2.morphologyEx(p1, cv.MORPH_CLOSE,kernel)
#
# # 梯度计算 (图像轮廓)  膨胀-腐蚀
# # gradient = cv.morphologyEx(p1,cv.MORPH_GRADIENT, kernel)
#
# # 礼帽和黑帽
# # 礼帽=原始输入-开运算结果
# # tophat = cv.morphologyEx(p1,cv.MORPH_TOPHAT, kernel)
# # 黑帽=闭运算-原始输入
# # blackhat = cv.morphologyEx(p1,cv.MORPH_BLACKHAT,kernel)
#
# # 梯度处理
# '''
# 图像梯度-Sobel算子 右减左，上减下
# dst = cv.Sobel(src, ddepth, dx, fdy, ksize)
# ddepth  图像的深度
# dx 和 dy 分别表示水平和竖直方向
# ksize是Sobel的大小
# '''
# # sobelx = cv.Sobel(p1, cv.CV_64F, 1,0,ksize=3 )
# # 转换  绝对值 得到整体的轮廓
# # sebelx = cv.convertScaleAbs(sobelx)
#
# '''
# 图像梯度 - scharr 算子  （更对细节）
# 图像梯度 - laplacian 算子， （对噪音点明显）
# '''
#
# #  边缘检测
# '''
# canny 边缘检测
# 1.使用高斯滤波器，以平滑图像，滤除噪音
# 2.计算图像像素点的梯度强度和方向
# 3.应用非极大值抑制， 以消除边缘检测带来的杂散响应
# 4.应用双闸门值
# '''
# # v1 = cv.Canny(p1, 80, 150)
# # v2 = cv.Canny(p1, 50, 100)
# # res = np.hstack(v1,v2)
#
# # 图像金字塔  放大缩小图像类似
# '''
# 高斯金字塔
# 拉普拉斯金字塔
# '''
#
# # 图像轮廓
# '''
# cv2.findContours(img,mode,method)
#
#
# mode: 轮廓检索模式
# 常用mode RETR_TREE:检索所有的轮廓，并重构嵌套轮廓的整个层次
# method: 轮廓逼近方法
# 常用method:  CHAIN_APPROX_NONE
# '''
#
# '''
# 为了更高的准确率，使用二值图像
#
# 图片常规处理方法
# 读图片
# 转灰色
# 转二值图像  图像阈值
# 然后在用检测函数操作
# '''
#
# '''
# cv2.drawContours(img, contours)
# '''
#
# # 轮廓特征
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# # 显示图像
# # cv.imshow("img", p2)
# cv.imshow("img2", p1)
#
#
#
#
# cv.waitKey(0)
# cv.destroyAllWindows()
#
# # 图像缩放
#
# # 模板匹配 matchTemplate
# # numpy 数组的维度
# # 从一个矩阵中找出全局的最大值和最小值
#
#
#
#
a = cv.imread('C:\\Users\\chenyh39\\Desktop\\Screenshot7.png')
b = cv.imread('C:\\Users\\chenyh39\\Desktop\\Screenshot8.png')
width = b.shape[1]
height = b.shape[0]
print(width, height)
# 模板匹配
c = cv.matchTemplate(a, b, cv.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(c)
print(min_val, max_val, min_loc, max_loc)
print(max_loc)
target_center = (max_loc[0] + int(width / 2), max_loc[1] + int(height / 2))
print(target_center)
# img_show = cv.rectangle(a, max_loc[0]+width, max_loc[1]+height, color=(0, 0, 255), thickness=2)
print(max_loc[0]+width)
print(max_loc[1]+height)
# img_show = cv.circle(a, target_center, radius=5, color=(0, 0, 255), thickness=2)
# cv.imshow('img', img_show)
cv.waitKey(0)
