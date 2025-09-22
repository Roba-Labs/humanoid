import copy
import cv2
import numpy as np
import pyrealsense2 as rs

class RealSenseCamera:
    """
    A class to interact with an Intel RealSense 3D camera.
    It handles the configuration, data streaming, and frame retrieval.
    """

    def __init__(self, width=848, height=480, fps=30):
        """
        Initializes the RealSense camera.
        Args:
            width (int): The width of the video stream.
            height (int): The height of the video stream.
            fps (int): The frames per second of the video stream.
        """
        self.width = width
        self.height = height
        self.fps = fps
        self.break_loop = False

        # Configure depth and color streams
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        self.config.enable_stream(rs.stream.depth, self.width, self.height, rs.format.z16, self.fps)
        self.config.enable_stream(rs.stream.color, self.width, self.height, rs.format.bgr8, self.fps)

        # Start streaming
        self.pipeline.start(self.config)

        # Create an align object
        # rs.align allows us to perform alignment of depth frames to others frames
        # The "align_to" is the stream type to which we plan to align depth frames.
        self.aligned_stream = rs.align(rs.stream.color)
        self.point_cloud = rs.pointcloud()

    def get_frames(self):
        """
        Waits for and retrieves the next set of frames from the camera.
        It returns the color image and the 3D vertex points (point cloud).
        Returns:
            A tuple containing:
            - image (np.ndarray): The color image.
            - verts (np.ndarray): The 3D vertex points.
        """
        # Wait for a coherent pair of frames: depth and color
        frames = self.pipeline.wait_for_frames()
        frames = self.aligned_stream.process(frames)
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame().as_depth_frame()

        if not depth_frame or not color_frame:
            return None, None

        # Calculate the point cloud
        points = self.point_cloud.calculate(depth_frame)
        verts = np.asanyarray(points.get_vertices()).view(np.float32).reshape(-1, self.width, 3)  # (x,y,z)

        # Convert images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())
        image = copy.deepcopy(color_image)

        return image, verts

    def display_image(self, img, window_name="Roba Robot"):
        """
        Displays an image in a CV2 window.
        Args:
            img (np.ndarray): The image to display.
            window_name (str): The name of the window.
        """
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.imshow(window_name, img)

        key = cv2.waitKey(1)
        if key in (27, ord("q")) or cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            self.break_loop = True
            cv2.destroyAllWindows()

    def stop_pipeline(self):
        """Stops the camera pipeline."""
        self.pipeline.stop()