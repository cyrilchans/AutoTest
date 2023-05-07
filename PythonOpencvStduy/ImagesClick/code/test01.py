import cv2 as cv
# opencv-python  4.5.5.64


def match_thread(tpl, img):
    res = cv.matchTemplate(tpl, img, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    return max_val, max_loc

def tpl_match(tpl, img):
    tpl_sp = tpl.shape
    max_val, max_loc = match_thread(tpl, img)
    width = tpl_sp[1]
    height = tpl_sp[0]
    print(width, height)
    target_center = (max_loc[0] + int(width / 2), max_loc[1] + int(height / 2))
    target_vertex = max_loc
    print( max_val, target_center, target_vertex)
    return max_val, target_center, target_vertex

img = cv.imread('../pictrue/test1.png')
tpl = cv.imread('../pictrue/img.png')
tpl_match(tpl, img)
# img_show = cv.circle(img, text[1], radius=5, color=(0, 0, 255), thickness=2)
# cv.imshow('img', img_show)
# cv.waitKey(0)
# print(text)