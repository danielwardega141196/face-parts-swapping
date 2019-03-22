from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors
import numpy as np

PERCENT_OF_NEAREST_NEIGHBOURS = 0.01
CLASSIFIERS = {

    "kNN": KNeighborsClassifier,
    "NearestNeighbors": NearestNeighbors
}
DEFAULT_CLASSIFIER = CLASSIFIERS["NearestNeighbors"]

MASK_FILLING_COLOR = np.array([255, 255, 255], dtype=np.uint8)

ALLOWED_MODES_OF_WARP_MATS = ["raw_polygon", "cropped_polygon"]
DEFAULT_MODE_OF_WARP_MATS = "raw_polygon"