import numpy as np
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors

PERCENT_OF_NEAREST_NEIGHBOURS = 0.01
CLASSIFIERS = {

    "kNN": KNeighborsClassifier,
    "NearestNeighbors": NearestNeighbors
}
DEFAULT_CLASSIFIER = CLASSIFIERS["NearestNeighbors"]

RGB_MASK_FILLING_COLOR = np.array([255, 255, 255], dtype=np.uint8)
