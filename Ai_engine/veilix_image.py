import cv2

# ================================
# LOAD PRE-TRAINED DNN MODEL
# ================================
# This loads the AI model:
# - deploy.prototxt → structure
# - .caffemodel → trained weights

net = cv2.dnn.readNetFromCaffe(
    "models/deploy.prototxt",
    "models/res10_300x300_ssd_iter_140000.caffemodel"
)

# ================================
# LOAD INPUT IMAGE
# ================================
# Replace 'input.jpg' with your image name

image = cv2.imread("input.jpg")

# Check if image loaded properly
if image is None:
    print("Error: Image not found!")
    exit()

# Optional: scale down large images for easier processing & viewing
scale_factor = 0.5  # change to 0.5 for 50% size, 0.3 for 30%, etc.
image = cv2.resize(image, (0, 0), fx=scale_factor, fy=scale_factor)

# Get image dimensions
(h, w) = image.shape[:2]

# ================================
# PREPROCESS IMAGE FOR DNN
# ================================
# Convert image into blob (format required by model)

blob = cv2.dnn.blobFromImage(
    image,
    1.0,
    (300, 300),
    (104.0, 177.0, 123.0)
)

# Pass blob into the network
net.setInput(blob)
detections = net.forward()

# ================================
# SELECT MODE
# ================================
# 2 = Blur, 3 = Pixelate

mode = 2

# ================================
# PROCESS DETECTIONS
# ================================

for i in range(detections.shape[2]):

    # Confidence score of detection
    confidence = detections[0, 0, i, 2]

    # Ignore weak detections
    if confidence > 0.5:

        # Get bounding box coordinates
        box = detections[0, 0, i, 3:7] * [w, h, w, h]
        (x1, y1, x2, y2) = box.astype("int")

        # Ensure box is inside image boundaries
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)

        # Extract face region
        face = image[y1:y2, x1:x2]

        if face.size != 0:

            # ================================
            # APPLY PRIVACY FILTER
            # ================================

            if mode == 2:
                # Blur face
                blur = cv2.GaussianBlur(face, (99, 99), 30)
                image[y1:y2, x1:x2] = blur

            elif mode == 3:
                # Pixelate face
                small = cv2.resize(face, (16, 16))
                pixel = cv2.resize(
                    small,
                    (x2 - x1, y2 - y1),
                    interpolation=cv2.INTER_NEAREST
                )
                image[y1:y2, x1:x2] = pixel

# ================================
# SAVE OUTPUT IMAGE
# ================================

cv2.imwrite("output.jpg", image)

# ================================
# DISPLAY RESULT
# ================================
# Resize image for display (optional)
display_image = cv2.resize(image, (800, 600))  # or any size that fits your screen
cv2.imshow("Veilix Image Output", display_image)
cv2.imshow("Veilix Image Output", image)
cv2.waitKey(0)
cv2.destroyAllWindows()