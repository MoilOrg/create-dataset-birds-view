"""
This class is to showing image on the pygame user interface.
The reason why we use pygame is about the speed of the computation.

Writer: Haryanto
Last updated : 08/02/2022
Under copyright: MOIL-Org
"""
import os
import sys

import cv2
import numpy as np
import pygame
from pygame.locals import DOUBLEBUF, KEYDOWN, K_ESCAPE, K_q, K_SPACE, K_r, K_s


class Display2D(object):
    def __init__(self, set_size_window=(1400, 900)):
        x = 100
        y = 100
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
        pygame.init()
        # pygame.display.set_caption(" MOIL Visual SLAM      'Space to Play',  'Esc to Close'")
        pygame.display.set_caption(" MOIL ")

        self.record = False
        self.screen = pygame.display.set_mode(set_size_window, DOUBLEBUF)
        self.surface = pygame.Surface(self.screen.get_size()).convert()

    @classmethod
    def cvimage_to_pygame(cls, cv2Image, ratio):
        h, w = cv2Image.shape[:2]
        cv2Image = cv2.resize(cv2Image, (round(w * ratio), round(h * ratio)), interpolation=cv2.INTER_AREA)
        if cv2Image.dtype.name == 'uint16':
            cv2Image = (cv2Image / 256).astype('uint8')
        size = cv2Image.shape[1::-1]
        if len(cv2Image.shape) == 2:
            cv2Image = np.repeat(cv2Image.reshape(size[1], size[0], 1), 3, axis=2)
            format = 'RGB'
        else:
            format = 'RGBA' if cv2Image.shape[2] == 4 else 'RGB'
            cv2Image[:, :, [0, 2]] = cv2Image[:, :, [2, 0]]
        surface = pygame.image.frombuffer(cv2Image.flatten(), size, format)
        return surface.convert_alpha() if format == 'RGBA' else surface.convert()

    def showImage(self, image_1=None, image_2=None, image_3=None, image_4=None, ratio=0.5):
        """

        :param image_3:
        :type image_3:
        :param image_1:
        :param image_2:
        :param ratio:
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    # self.video.stop()
                    sys.exit(0)
                # if event.key == K_SPACE:
                #     if self.video.is_paused is True:
                #         self.video.resume()
                #     elif self.video.is_paused is False:
                #         self.video.pause()
                #
                if event.key == K_r:
                    self.record = True
                    # if record is not None:
                    #     record.write(image_1)
                #     self.video.restart()
                #
                if event.key == K_s:
                    print("test")

        if image_2 is not None:
            img2 = self.cvimage_to_pygame(image_2, ratio)
            self.screen.blit(img2, (600, 5))

        if image_3 is not None:
            img2 = self.cvimage_to_pygame(image_3, ratio)
            self.screen.blit(img2, (5, 450))

        if image_4 is not None:
            img2 = self.cvimage_to_pygame(image_4, ratio)
            self.screen.blit(img2, (600, 450))

        # if image_1 is not None:
        img1 = self.cvimage_to_pygame(image_1, ratio)
        self.screen.blit(img1, (5, 5))
        pygame.display.flip()


view = Display2D()
cap = cv2.VideoCapture("http://10.42.0.212:8000/stream.mjpg")
cap_2 = cv2.VideoCapture("http://10.42.0.170:8000/stream.mjpg")
cap_3 = cv2.VideoCapture("http://10.42.0.183:8000/stream.mjpg")
cap_4 = cv2.VideoCapture("http://10.42.0.251:8000/stream.mjpg")
ret, image = cap.read()
h, w, z = image.shape

record = True
out = []
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out.append(cv2.VideoWriter("output_image_1_4.avi", fourcc, 10, (w, h)))
out.append(cv2.VideoWriter('output_image_2_4.avi', fourcc, 10, (w, h)))
out.append(cv2.VideoWriter('output_image_3_4.avi', fourcc, 10, (w, h)))
out.append(cv2.VideoWriter('output_image_4_4.avi', fourcc, 10, (w, h)))

while cap.isOpened():
    success, frame = cap.read()
    _, frame2 = cap_2.read()
    _, frame3 = cap_3.read()
    _, frame4 = cap_4.read()
    if success:
        cv2.imwrite("images/right_true_park5.jpg", frame)
        cv2.imwrite("images/left_true_park5.jpg", frame2)
        cv2.imwrite("images/front_true_park5.jpg", frame3)
        cv2.imwrite("images/back_true_park5.jpg", frame4)

        if record:
            out[0].write(frame)
            out[1].write(frame2)
            out[2].write(frame3)
            out[3].write(frame4)

        view.showImage(image_1=frame, image_2=frame2, image_3=frame3, image_4=frame4, ratio=0.25)
