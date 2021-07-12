import os
import cv2
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image

from threading import Thread


# --- Camera Kivy --- #
class KivyCV(Image):

    def __init__(self, capture, fps) -> object:
        super().__init__()
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)


    # --- Face detection configuration --- #
    def update(self, dt):

        ret, frame = self.capture.read()

        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(20, 20))
            
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # --- Transforming an image into texture to place the camera --- #
            buf = cv2.flip(frame, 0).tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

            # ---Display image from the texture--- #
            self.texture = image_texture    


# --- Capture photos --- #
class CapturaFotos():
    
    def __init__(self, **kwargs):
        super().__init__()

        # --- Camera configuration --- #
        self.capture = cv2.VideoCapture(0)
    

    # --- Starts capturing faces --- #
    def fotofaces(self, cpf, *args):

        # --- Code to extract the images --- #
        def face_extractor(img):
            face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)

            # --- Identifies face to cut--- #
            if faces == ():
                return None

            # --- Recorta a Cut out the face --- #
            for (x, y, w, h) in faces:
                cropped_face = img[y:y + h, x:x + w]
            return cropped_face

        count = 0

        # --- If the camera turns on captures the faces --- #
        while True:
            ret, frame = self.capture.read()

            if face_extractor(frame) is not None:
                count += 1
                face = cv2.resize(face_extractor(frame), (200, 200))
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

                # --- Directory to save faces --- #
                path_photos = os.path.expanduser(f"~/Documents/Projeto Leticia/faces/{cpf}_")
                file_name_path = path_photos + str(count) + '.jpg'

                cv2.imwrite(file_name_path, face)
                cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow('Face Cropper', face)

            else:
                print("FACE NOT DETECTED")
                pass

            if cv2.waitKey(1) == 13 or count == 5:
                break

        # --- Ends capturing photos --- #
        self.capture.release()
        cv2.destroyAllWindows()
