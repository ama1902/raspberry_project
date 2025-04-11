import cv2

def main():
    # Initialize the camera
    cap = cv2.VideoCapture(0)  # 0 is the default camera (Raspberry Pi camera)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            if not ret:
                print("Error: Failed to capture image.")
                break

            # Display the resulting frame
            cv2.imshow('Camera Preview', frame)

            # Press 'q' to exit the preview
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # Release the camera and close all OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()