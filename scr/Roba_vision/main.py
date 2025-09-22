"""
This script performs object detection and tracking on a video file.
It is an example of how to use the object tracking functionality.
"""
import cv2
from tracker import EuclideanDistTracker

def main():
    """
    Main function to run the object detection and tracking.
    """
    # Create tracker object
    object_tracker = EuclideanDistTracker()

    # Open video file
    cap = cv2.VideoCapture("highway.mp4")

    # Object detection from Stable camera
    background_subtractor = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=50)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Define Region of Interest (ROI)
        # The values are hardcoded for the 'highway.mp4' video
        roi = frame[340:720, 500:800]

        # 1. Object Detection
        # Apply background subtraction to get a mask of moving objects
        mask = background_subtractor.apply(roi)
        # Remove shadows
        _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
        # Find contours of the detected objects
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        detections = []

        for cnt in contours:
            # Calculate area and remove small elements
            area = cv2.contourArea(cnt)
            if area > 130:
                x, y, w, h = cv2.boundingRect(cnt)
                detections.append([x, y, w, h])

        # 2. Object Tracking
        # Update the tracker with the new detections
        boxes_ids = object_tracker.update(detections)
        for box_id in boxes_ids:
            x, y, w, h, obj_id = box_id
            # Draw bounding box and ID on the ROI
            cv2.putText(roi, str(obj_id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)

        # Display the frames
        cv2.imshow("Region of Interest", roi)
        cv2.imshow("Frame", frame)
        cv2.imshow("Mask", mask)

        # Break the loop if 'ESC' is pressed
        key = cv2.waitKey(30)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
