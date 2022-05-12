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
        self.record = False
        self.space = False
        self.h, self.w, self.z = 0, 0, 0
        self.video = None
        self.out = []
        x = 100
        y = 100
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
        pygame.init()
        pygame.display.set_caption(" MOIL ")

        self.record = False
        self.screen = pygame.display.set_mode(set_size_window, DOUBLEBUF)
        self.surface = pygame.Surface(self.screen.get_size()).convert()

    @classmethod
    def cvimage_to_pygame(cls, cv2Image, ratio):
        """
        :param cv2Image:
        :param ratio:
        :return:
        """
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
        :param image_1: camera source 1
        :param image_2: camera source 2
        :param image_3: camera source 3
        :param image_4: camera source 4
        :param ratio:
        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    sys.exit(0)

                if event.key == K_SPACE:
                    print("save image")
                    self.space = True

                if event.key == K_r:
                    print("start record")
                    self.record = True
                    print(self.record)

                if event.key == K_s:
                    print("stop record")
                    self.record = False

        if image_2 is not None:
            img2 = self.cvimage_to_pygame(image_2, ratio)
            self.screen.blit(img2, (600, 5))

        if image_3 is not None:
            img2 = self.cvimage_to_pygame(image_3, ratio)
            self.screen.blit(img2, (5, 450))

        if image_4 is not None:
            img2 = self.cvimage_to_pygame(image_4, ratio)
            self.screen.blit(img2, (600, 450))

        img1 = self.cvimage_to_pygame(image_1, ratio)
        self.screen.blit(img1, (5, 5))
        pygame.display.flip()

    def main(self):
        """
        Start program
        """

        # read video
        cap_1 = cv2.VideoCapture("http://10.42.0.212:8000/stream.mjpg")
        cap_2 = cv2.VideoCapture("http://10.42.0.170:8000/stream.mjpg")
        cap_3 = cv2.VideoCapture("http://10.42.0.183:8000/stream.mjpg")
        cap_4 = cv2.VideoCapture("http://10.42.0.251:8000/stream.mjpg")

        _, image = cap_1.read()
        self.h, self.w, self.z = image.shape
        self.record_setup()

        while cap_1.isOpened():
            success, frame1 = cap_1.read()
            _, frame2 = cap_2.read()
            _, frame3 = cap_3.read()
            _, frame4 = cap_4.read()

            if success:
                if self.space:
                    cv2.imwrite("images/image1.jpg", frame1)
                    cv2.imwrite("images/image2.jpg", frame2)
                    cv2.imwrite("images/image3.jpg", frame3)
                    cv2.imwrite("images/image4.jpg", frame4)
                    self.space = False

                if self.record:
                    self.out[0].write(frame1)
                    self.out[1].write(frame2)
                    self.out[2].write(frame3)
                    self.out[3].write(frame4)

                # self.showImage(image_1=frame1, ratio=0.25)
                self.showImage(image_1=frame1, image_2=frame2, image_3=frame3, image_4=frame4, ratio=0.25)

    def record_setup(self):
        """
        setup record video
        """
        print("setup")
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out.append(cv2.VideoWriter("Videos/video_1.avi", fourcc, 10, (self.w, self.h)))
        self.out.append(cv2.VideoWriter('Videos/video_2.avi', fourcc, 10, (self.w, self.h)))
        self.out.append(cv2.VideoWriter('Videos/video_3.avi', fourcc, 10, (self.w, self.h)))
        self.out.append(cv2.VideoWriter('Videos/video_4.avi', fourcc, 10, (self.w, self.h)))


if __name__ == "__main__":
    app = Display2D()
    app.main()
