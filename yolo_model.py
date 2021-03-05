import numpy as np 
import os 
from darknet import *
import cv2

class Detector():
    def __init__(self, config):
        self.config = config
        self.conf_threshold = config.confidence
        self.nms_threshold = config.nms_threshold
        self.hier_threshold = config.hier_threshold
        self.net = load_net(str.encode(config.config), str.encode(config.weight), 0)
        self.darknet_image = make_image(network_width(self.net), network_height(self.net), 3)
        self.size = config.input_size
        self.network, self.class_names, self.class_colors = load_network(
            config.config,
            config.meta,
            config.weight,
            batch_size=1
        )
        
    def resize_padding(self, im):
        im_h, im_w = im.shape[:2]
        longer_edge = max(im_h, im_w)
        ratio = longer_edge/self.size
        new_h = int(im_h/ratio)
        new_w = int(im_w/ratio)
        im = cv2.resize(im, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
		
        delta_w = self.size - new_w
        delta_h = self.size - new_h
        top, bottom = delta_h//2, delta_h - delta_h//2
        left, right = delta_w//2, delta_w - delta_w//2
        color = [0, 0, 0]
        new_im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
        return new_im, ratio, top, left

    def detect(self, image):
        image, ratio, top_pad, left_pad = self.resize_padding(image.copy())
        copy_image_from_bytes(self.darknet_image, image.tobytes())
        res = detect_image(network=self.network,
                    class_names=self.class_names,
                    image=self.darknet_image,
                    thresh=self.conf_threshold, 
                    hier_thresh=self.hier_threshold,
                    nms=self.nms_threshold)
        boxes = []
        labels = []
        confident_scores = []
        for r in res:
            label, confident_score, box = r
            x, y, w, h = box
            xmin = (x - w//2 - left_pad)*ratio
            ymin = (y - h//2 - top_pad)*ratio
            xmax = (x + w//2 - left_pad)*ratio
            ymax = (y + h//2 - top_pad)*ratio
            boxes.append([xmin, ymin, xmax, ymax])
            labels.append(label)
            confident_scores.append(confident_score)
        boxes = np.array(boxes).astype('int').reshape(-1, 4)
        return boxes, labels, confident_scores

if __name__ == "__main__":
    import anyconfig
    import munch
    cfg = anyconfig.load("configs/cfg2.yaml")
    cfg = munch.munchify(cfg)
    detector = Detector(cfg.detector)
    detector.detect(np.zeros((416, 416, 3)))
