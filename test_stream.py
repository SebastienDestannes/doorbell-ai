import cv2

ESP32_IP = "192.168.1.45:81"
stream_url = f"http://{ESP32_IP}/stream"

cap = cv2.VideoCapture(stream_url)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Impossible de lire le flux")
        break
    
    cv2.imshow("ESP32-CAM", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
