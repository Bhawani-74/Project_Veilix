import cv2
import numpy as np

def apply_smart_adversarial(image_path, output_path, faces):
    image = cv2.imread(image_path)

    if image is None:
        print("Error: Image not found!")
        return

    img = image.astype(np.float32)

    for (x1, y1, x2, y2) in faces:
        face = img[y1:y2, x1:x2]

        gray = cv2.cvtColor(face.astype(np.uint8), cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)

        edges = edges / 255.0
        edges = (edges * 2) - 1
        edges = np.stack([edges]*3, axis=-1)

        epsilon = 3.0
        perturbation = epsilon * np.sign(edges)

        face_adv = np.clip(face + perturbation, 0, 255)

        alpha = 0.9
        blended = alpha * face + (1 - alpha) * face_adv

        img[y1:y2, x1:x2] = blended

    cv2.imwrite(output_path, img.astype(np.uint8))

    print("Smart adversarial applied!")