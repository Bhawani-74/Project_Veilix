import cv2
import numpy as np

def encode_watermark(input_path, output_path, secret, faces=None):
    image = cv2.imread(input_path)

    if image is None:
        print("Error: Image not found!")
        return

    # Convert to YCrCb (better for watermarking)
    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    y_channel = ycrcb[:, :, 0]

    # Convert secret to binary
    binary_secret = ''.join(format(ord(c), '08b') for c in secret)
    data_index = 0

    height, width = y_channel.shape

    # Function to embed watermark in a region
    def embed_region(region):
        nonlocal data_index

        h, w = region.shape

        for i in range(0, h - 8, 8):
            for j in range(0, w - 8, 8):
                if data_index >= len(binary_secret):
                    return region

                block = region[i:i+8, j:j+8]
                dct_block = cv2.dct(np.float32(block))

                # Modify one mid-frequency coefficient
                if binary_secret[data_index] == '1':
                    dct_block[4][4] += 10
                else:
                    dct_block[4][4] -= 10

                region[i:i+8, j:j+8] = cv2.idct(dct_block)
                data_index += 1

        return region

    # Face-aware embedding
    if faces and len(faces) > 0:
        print(f"Embedding strong watermark in {len(faces)} face(s)")

        for (x1, y1, x2, y2) in faces:
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(width, x2), min(height, y2)

            region = y_channel[y1:y2, x1:x2]
            region = embed_region(region)

            y_channel[y1:y2, x1:x2] = region
    else:
        print("No face found, embedding in full image")
        y_channel = embed_region(y_channel)

    # Merge channels back
    ycrcb[:, :, 0] = y_channel
    watermarked = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)

    cv2.imwrite(output_path, watermarked)

    print("Strong watermark embedded successfully!")