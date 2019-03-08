import cv2
import numpy as np
from sklearn import metrics
import warnings
import sys


def get_binary_image_for_color(im, color):
    """
    img : image. color challel is in the order of b, g, r
    color : string, either of 'yellow', 'blue', 'brown'
    """
    b = im[:, :, 0]
    g = im[:, :, 1]
    r = im[:, :, 2]

    if color == 'yellow':
        im_bin = (r == 255) & (g == 242) & (b == 0)
    elif color == 'blue':
        im_bin = (r == 0) & (g == 162) & (b == 232)
    elif color == 'brown':
        im_bin = (r == 185) & (g == 122) & (b == 87)
    else:
        sys.exit("color input error")

    return im_bin


def F1s(file_true, file_pred):

    """
    :param file_true: full file path to the true image
    :param file_pred: full file path to the predicted image
    :return: 5 F1 scores
			- F1 score of the Clastic detection (yellow. R G B = 255 242 0)
			- F1 score of the Carbonate detection (blue. R G B = 0 162 232)
			- F1 score of the Other detection (brown. R G B = 185 122 87)
			- Average of 1,2,3
			- F1 score of the integral of the Clastic, Carbonate, Other detection. This corresponds to the column detection
    """

    print('Evaluating image {} against {}'.format(file_pred, file_true))
    im_true = cv2.imread(file_true, cv2.IMREAD_COLOR)
    im_pred = cv2.imread(file_pred, cv2.IMREAD_COLOR)

    # check predicted image size
    if im_true.shape != im_pred.shape:
        warnings.warn("Size of the predicted image does not correspond to the size of the true image.", Warning)
        return 0, 0, 0, 0, 0

    bim_integral_true = np.zeros(im_true.shape[:2], dtype=bool)
    bim_integral_pred = np.zeros(im_true.shape[:2], dtype=bool)

    # For each color
    score_list = np.zeros(3)
    for i, c in enumerate(['yellow', 'blue', 'brown']):
        bim_true = get_binary_image_for_color(im_true, c)
        bim_integral_true = np.logical_or(bim_integral_true, bim_true)
        bim_pred = get_binary_image_for_color(im_pred, c)
        bim_integral_pred = np.logical_or(bim_integral_pred, bim_pred)
        if np.sum(bim_true) == 0:
            #print('{} does not exist in the true image'.format(c))
            score_list[i] = np.nan
        else:
            score_list[i] = metrics.f1_score(bim_true.ravel(), bim_pred.ravel(), pos_label=1)

    score_yellow = score_list[0]
    score_blue = score_list[1]
    score_brown = score_list[2]
    score_ave = np.nanmean(score_list)
    score_integral = metrics.f1_score(bim_integral_true.ravel(), bim_integral_pred.ravel(), pos_label=1)

    return score_yellow, score_blue, score_brown, score_ave, score_integral
