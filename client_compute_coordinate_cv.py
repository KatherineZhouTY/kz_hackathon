# calculate coordinates with cv2 and perform multiprocessing
# should send pictures to server
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import os
import multiprocessing as mp
from multiprocessing import Process, Queue

def compute_coordinate(files, queue):

    origin = cv.imread('./img/origin.png', 0)
    corner = cv.imread('./img/corner.png', 0)
    ball = cv.imread('./img/ball.png', 0)
    w, h = ball.shape[::-1]
    directory = "./img"

    for file in files:
        if file.lower().endswith('.png') and file.lower().startswith('image'):
            f = os.path.join(directory, file)
            img = cv.imread(f, 0)

            cv.imshow('Window', img)
            key = cv.waitKey(100) 
            if key == 27: #if ESC is pressed, exit loop
                cv.destroyAllWindows()
                break

            method = 3
            res = cv.matchTemplate(img,ball,method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            ball_x, ball_y = max_loc[0] + w, max_loc[1] + h
            
            res = cv.matchTemplate(img,origin,method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            origin_x, origin_y = max_loc[0] + w, max_loc[1] + h

            res = cv.matchTemplate(img,corner,method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            corner_x, corner_y = max_loc[0] + w, max_loc[1] + h
            
            x_coordinate = (ball_x-origin_x)/(corner_x-origin_x)*6-1
            y_coordinate = (origin_y-ball_y)/(origin_y-corner_y)*5
            coordinate = (round(x_coordinate,2), round(y_coordinate,2))
            queue.put(coordinate)


if __name__=="__main__":
    queue = Queue()
    directory = "./img"
    files = sorted(os.listdir(directory))
    process_a = Process(target = compute_coordinate, args = (files, queue))
    process_a.start()
    process_a.join()

    while not queue.empty():
        print(queue.get())


            
