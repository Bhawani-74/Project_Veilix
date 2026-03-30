import cv2

# Load DNN face detector model (use your absolute path if needed)
net = cv2.dnn.readNetFromCaffe(
    "C:/Users/Lenovo/OneDrive/Desktop/Veilix/models/deploy.prototxt",
    "C:/Users/Lenovo/OneDrive/Desktop/Veilix/models/res10_300x300_ssd_iter_140000.caffemodel"
)

def detect_faces(image_path):
    """
    Detect faces and return bounding boxes
    """
    image = cv2.imread(image_path)

    if image is None:
        print("Error: Image not found!")
        return []

    (h, w) = image.shape[:2]

    # Create blob for DNN
    blob = cv2.dnn.blobFromImage(
        image,
        1.0,
        (300, 300),
        (104.0, 177.0, 123.0)
    )

    net.setInput(blob)
    detections = net.forward()

    faces = []

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * [w, h, w, h]
            (x1, y1, x2, y2) = box.astype("int")
            faces.append((x1, y1, x2, y2))

    print(f"Detected {len(faces)} face(s)")
    return faces