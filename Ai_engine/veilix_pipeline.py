import cv2
import os

from Ai_engine.face_detector_dnn import detect_faces
from Ai_engine.watermark import encode_watermark
from Ai_engine.adversarial import apply_smart_adversarial


def process_veilix(input_path, output_path, watermark=True, adversarial=True):
    print("DEBUG: Pipeline started")

    # Load image
    image = cv2.imread(input_path)

    if image is None:
        print("Error: Image not found!")
        return

    # Step 1: Detect faces
    faces = detect_faces(input_path)
    print(f"Detected {len(faces)} face(s)")

    # Step 2: Apply watermark (ONLY if enabled)
    if watermark:
        print("Applying watermark...")
        encode_watermark(input_path, output_path, "VeilixSecret", faces)

        # Reload updated image
        image = cv2.imread(output_path)
    else:
        print("Skipping watermark...")
        cv2.imwrite(output_path, image)

    # Step 3: Apply adversarial protection (ONLY if enabled)
    if adversarial:
        print("Applying adversarial protection...")
        image = apply_smart_adversarial(image)
    else:
        print("Skipping adversarial...")

    # Final save
    cv2.imwrite(output_path, image)

    print("Veilix processing complete!")
