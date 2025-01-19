import cv2
import numpy as np
from ultralytics import YOLO

# Load the YOLO model
model = YOLO("yolov8n.pt")  # Using YOLOv8n with COCO dataset

def process_object(frame, box, show_mask=False, show_bbox=True):
    """
    Process a detected object for bounding box, mask, and orientation.
    """
    x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates

    # Extract the ROI for mask processing
    roi = frame[y1:y2, x1:x2]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # Create a mask using adaptive thresholding
    mask = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                 cv2.THRESH_BINARY_INV, 11, 2)

    # Find contours within the ROI
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # Take the largest contour
        largest_contour = max(contours, key=cv2.contourArea)

        # Compute minimum area rectangle for orientation
        rect = cv2.minAreaRect(largest_contour)
        (center_x, center_y), (width, height), angle = rect
        box_points = cv2.boxPoints(rect)
        box_points = np.int0(box_points)

        if show_mask:
            # Create and display the mask
            object_mask = np.zeros_like(mask)
            cv2.drawContours(object_mask, [largest_contour], -1, 255, -1)
            cv2.imshow("Object Mask", object_mask)

        if show_bbox:
            # Draw bounding box and orientation
            color = (0, 255, 0)
            cv2.drawContours(frame, [box_points + [x1, y1]], 0, color, 2)
            cv2.circle(frame, (int(center_x) + x1, int(center_y) + y1), 5, (0, 0, 255), -1)
            label = f"Angle: {angle:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    return frame

def list_available_cameras(max_tested=5):
    """
    List available camera indices up to a maximum tested index.
    """
    available = []
    for i in range(max_tested):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available.append(i)
            cap.release()
    return available

# Get a list of available camera indices
available_cameras = list_available_cameras(max_tested=5)
if not available_cameras:
    print("No camera found in the range tested.")
    exit()

print("Available camera indices:", available_cameras)


def main():
    selected_camera = None
    while True:
        try:
            user_input = input("Enter camera index to use (or 'q' to quit): ").strip()
            if user_input.lower() == 'q':
                print("Exiting...")
                exit()

            cam_idx = int(user_input)
            if cam_idx in available_cameras:
                selected_camera = cam_idx
                break
            else:
                print(f"Camera index {cam_idx} not in available list. Try again.")
        except ValueError:
            print("Invalid input. Please enter a valid integer camera index or 'q' to quit.")

    # Now open the selected camera for live processing
    cap = cv2.VideoCapture(selected_camera)
    if not cap.isOpened():
        print(f"Could not open camera index {selected_camera}.")
        exit()

    print("Press 'q' to quit the video feed.")

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Run YOLO inference on the frame
        results = model.predict(source=frame, conf=0.65, save=False, show=False)

        # Process each detected object
        for result in results:
            for box in result.boxes:
                # TODO: Add specific object detection and ignore or process accordingly 
                # Skip if the detected object is a person
                if int(box.cls) == 0:  # Class index 0 corresponds to "person" in YOLO models
                    continue

                # Process and annotate the frame for the detected object
                frame = process_object(frame, box, show_mask=False, show_bbox=True)

        # Display the frame
        cv2.imshow("Real-Time Detection", frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()