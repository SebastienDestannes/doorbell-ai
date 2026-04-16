import cv2
import face_recognition
import numpy as np
import os

ESP32_URL = "http://192.168.1.45:81/stream"
KNOWN_FACES_DIR = "known_faces"
TOLERANCE = 0.5

# Chargement des visages connus
known_encodings = []
known_names = []

print("Chargement des visages connus...")
for filename in os.listdir(KNOWN_FACES_DIR):
    if filename.endswith((".jpg", ".jpeg", ".png")):
        image = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{filename}")
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_encodings.append(encodings[0])
            name = os.path.splitext(filename)[0]
            known_names.append(name)
            print(f"  ✓ {name}")
        else:
            print(f"  ✗ Aucun visage détecté dans {filename}")

print(f"\n{len(known_encodings)} visage(s) chargé(s). Démarrage du stream...")

# Stream
cap = cv2.VideoCapture(ESP32_URL)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Flux perdu")
        break

    # Réduction pour aller plus vite
    small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

    # Détection
    locations = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, locations)

    for encoding, location in zip(encodings, locations):
        matches = face_recognition.compare_faces(known_encodings, encoding, TOLERANCE)
        name = "Inconnu"

        if True in matches:
            distances = face_recognition.face_distance(known_encodings, encoding)
            best = np.argmin(distances)
            name = known_names[best]

        # Affichage
        top, right, bottom, left = [v * 4 for v in location]
        color = (0, 255, 0) if name != "Inconnu" else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Doorbell AI", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
