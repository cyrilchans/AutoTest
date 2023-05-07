import cv2 as cv
import numpy as np
import threading
import queue


q = queue.Queue()
def match_thread(tpl, img, ratio, scale_type):
    res = cv.matchTemplate(tpl, img, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

    q.put([max_val, max_loc, ratio, scale_type])


def tpl_match(tpl, img, ratio_lv=21):
    img_sp = img.shape
    tpl_sp = tpl.shape
    t_list = []
    isp_re = (0, 0)
    tsp_re = (0, 0)
    for ratio in range(1, ratio_lv):
        ratio = 1 - ratio / 100
        sp_re = (round(img_sp[1] * ratio), round(img_sp[0] * ratio))
        if sp_re != isp_re:
            img_re = cv.resize(img, sp_re)
            t = threading.Thread(target=match_thread,
                                 args=(tpl, img_re, ratio, "img"))
            t.start()
            t_list.append(t)
            isp_re = sp_re
        sps_re = (round(tpl_sp[1] * ratio), round(tpl_sp[0] * ratio))
        if sps_re != tsp_re:
            tpl_re = cv.resize(tpl, sps_re)
            t = threading.Thread(target=match_thread,
                                 args=(tpl_re, img, ratio, "tpl"))
            t.start()
            t_list.append(t)
            tsp_re = sps_re

    t = threading.Thread(target=match_thread,
                         args=(tpl, img, 1, "none"))
    t.start()
    t_list.append(t)
    thread_rlt = []
    while 1:
        if not q.empty():
            result = q.get()
            if result:
                thread_rlt.append(result)
        else:
            break

    thread_rlt.sort(reverse=True)
    max_val, max_loc, ratio, scale_type = thread_rlt[0]
    if scale_type == "img":
        max_loc = (round(max_loc[0] / ratio), round(max_loc[1] / ratio))

    width = tpl_sp[1]
    height = tpl_sp[0]
    if scale_type == "img":
        width /= ratio
        height /= ratio
    elif scale_type == "tpl":
        width *= ratio
        height *= ratio

    target_center = (max_loc[0] + int(width / 2), max_loc[1] + int(height / 2))
    target_vertex = max_loc

    return max_val, target_center, ratio, scale_type, target_vertex

img = cv.imread('./pictrue/test03.png')
tpl = cv.imread('./pictrue/test02.png')
text = tpl_match(tpl, img)
img_show = cv.circle(img, text[1], radius=5, color=(0, 0, 255), thickness=2)
cv.imshow('img', img_show)
cv.waitKey(0)
print(text)