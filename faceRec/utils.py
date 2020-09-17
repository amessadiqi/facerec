import os
import random
import string
import face_recognition
from faceRec.models import db, User


def add_user(email, password, first_name, last_name, gender, profile_picture, birthday, address):
    user = User(email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                profile_picture=profile_picture,
                birthday=birthday,
                address=address)
    db.session.add(user)
    db.session.commit()


def find_user_by_email(email):
    return User.query.filter_by(email=email).first()


def find_user_by_id(id):
    return User.query.filter_by(id=id).first()


def get_users():
    return User.query.all()


# Return User object or False if not found
def find_user_by_image(image):
    users = get_users()

    for user in users:
        known_image = face_recognition.load_image_file(os.path.dirname(__file__) + user.profile_picture)
        unknown_image = face_recognition.load_image_file(image)

        biden_encoding = face_recognition.face_encodings(known_image)[0]
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

        results = face_recognition.compare_faces([biden_encoding], unknown_encoding)

        if results[0] == True:
            return user

    return False


def save_uploaded_image(image, dir):
    image_filename = ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=5)) + image.filename
    image_uri = dir + image_filename
    image_path = os.path.dirname(__file__) + image_uri
    image.save(image_path)

    return image_path, image_uri, image_filename


def compare_faces(img1, img2):
    image1 = face_recognition.load_image_file(img1)
    image2 = face_recognition.load_image_file(img2)

    encoding1 = face_recognition.face_encodings(image1)[0]
    encoding2 = face_recognition.face_encodings(image2)[0]

    return face_recognition.compare_faces([encoding1], encoding2)


def detect_faces(img_path, img_filename, scaleFactor=1.1):
    import cv2

    colored_img = cv2.imread(img_path)

    f_cascade = cv2.CascadeClassifier(r'C:\Users\lenovo\Desktop\faceRec\faceRec\haarcascade_frontalface_alt.xml')
    img_copy = colored_img.copy()

    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

    faces = f_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imwrite(img_path, img_copy)

    return img_filename
