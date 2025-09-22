import math

class EuclideanDistTracker:
    """
    A simple object tracker based on Euclidean distance.
    It assigns a unique ID to each detected object and tracks it based on the proximity
    of its center point in consecutive frames.
    """

    def __init__(self, max_distance=25):
        """
        Initializes the tracker.
        Args:
            max_distance (int): The maximum distance (in pixels) between the center points
                                of an object in consecutive frames to be considered the same object.
        """
        # Store the center positions of the objects, mapping object ID to its center point.
        self.center_points = {}
        # Counter for assigning new object IDs.
        self.id_count = 0
        self.max_distance = max_distance

    def update(self, object_rectangles):
        """
        Updates the tracker with the new set of detected object rectangles.
        Args:
            object_rectangles (list): A list of rectangles, where each rectangle is a list [x, y, w, h].
        Returns:
            list: A list of tracked objects, where each object is a list [x, y, w, h, object_id].
        """
        tracked_objects = []

        # Get the center point of each new object rectangle.
        for rect in object_rectangles:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Check if the object was detected in the previous frame.
            same_object_detected = False
            for object_id, center_point in self.center_points.items():
                distance = math.hypot(cx - center_point[0], cy - center_point[1])

                if distance < self.max_distance:
                    # The object was detected before, so update its center point.
                    self.center_points[object_id] = (cx, cy)
                    tracked_objects.append([x, y, w, h, object_id])
                    same_object_detected = True
                    break

            # If it's a new object, assign a new ID.
            if not same_object_detected:
                self.center_points[self.id_count] = (cx, cy)
                tracked_objects.append([x, y, w, h, self.id_count])
                self.id_count += 1

        # Remove IDs of objects that are no longer being tracked.
        current_object_ids = {obj[4] for obj in tracked_objects}
        self.center_points = {obj_id: center for obj_id, center in self.center_points.items() if obj_id in current_object_ids}

        return tracked_objects



