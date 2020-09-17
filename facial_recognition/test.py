import face_recognition
import time


def func():
    t1 = time.time()

    known_image = face_recognition.load_image_file("celebrity/amine.jpg")
    unknown_image = face_recognition.load_image_file("celebrity/amine2.jpg")

    biden_encoding = face_recognition.face_encodings(known_image)[0]
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

    results = face_recognition.compare_faces([biden_encoding], unknown_encoding)

    return time.time() - t1


def run(n=1):
    moy = 0
    for i in range(n):
        moy = moy + func()

    moy = moy / n
    print(moy)


while True:
    run()
    q = input("Want to quit ? ")
