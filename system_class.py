import Yolov4
import classify_model as ClassifyModel

class HandGestureClassifier:
    def __init__(self, yolov4_model, classify_model):
        """
        Constructor
        Our system includes 2 main attributes: YoloV4 model and classification model
        """

        self.yolov4_model = yolov4_model
        self.classify_model = classify_model

    @staticmethod
    def preprocess_image(bounding_boxes, input_image):
        """
        Preprocess image by Vu's method.
        Note that len(bounding_boxes) <= 2. In case of YoloV4 returns 3 or more boundingbox, 
        you must choose 2 bounding boxes by their confident_score
        """
        pass

    def predict(self, input_image):
        """
        Input image: full image
        This function takes an image, then preprocessing it by YoloV4.
        If YoloV4 returns no hand detected, we consider it "No Gesture"
        """

        hand_boundingbox = self.yolov4_model.detect(input_image)

        if hand_boundingbox == None:
            # Consider it "No Gesture"
            return 31 
        
        # Preprocessing
        processed_image = self.preprocess_image(input_image, hand_boundingbox)

        gesture = self.classify_model.predict(processed_image)
        return gesture
