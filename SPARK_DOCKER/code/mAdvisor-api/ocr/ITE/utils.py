import cv2
import numpy as np
from PIL import Image
from scipy import optimize as opt
from scipy.ndimage import interpolation as inter


def adjust_gamma(image, gamma):  # TODO: Give Abishek's Autogamma correction code also.
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)


def denoise(image, denoise_strength):
    img = cv2.fastNlMeansDenoising(image, h=denoise_strength)
    return img


def deskew_optimized(image_name):
    # Optmized script.  ~98-99% correct.  ~15X faster than the original.

    bin_img = 1 - np.array(Image.open(image_name).convert('1')).astype('uint8')
    bin_img = bin_img[~np.all(bin_img == 0, axis=1)]
    bin_img = bin_img[~np.all(bin_img == 1, axis=1)]
    bin_img = bin_img[:, ~np.all(bin_img == 0, axis=0)]
    bin_img = bin_img[:, ~np.all(bin_img == 1, axis=0)]

    def find_score(angle):
        data = inter.rotate(bin_img, angle, reshape=False, order=0)
        hist = np.sum(data, axis=1)
        score = np.sum((hist[1:] - hist[:-1]) ** 2)
        return -1 * score

    best_angle = opt.fminbound(lambda x: find_score(x), -5, 5, xtol=0.1)

    # print('[OPT] Best rotation angle:', round(best_angle, 2))

    # Rotating the image
    image = cv2.imread(image_name)
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h),
                             flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated, round(best_angle, 2)


def extract_mask(bw, scalev=40, scaleh=20):  ## OVERLAP OF HORIZONTAL AND VERTICAL MASKS
    # Scalev and Scaleh are Used to increase/decrease the amount of lines to be detected

    horizontal = bw.copy()
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal.shape[1] // int(scaleh), 1))
    horizontal = cv2.erode(horizontal, horizontalStructure, iterations=1)
    horizontal = cv2.dilate(horizontal, horizontalStructure, iterations=1)
    # horizontal = cv2.dilate(horizontal, np.ones((4, 4)))
    horizontal = horizontal + cv2.morphologyEx(horizontal, cv2.MORPH_GRADIENT, np.ones((4, 4)))

    vertical = bw.copy()
    verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, vertical.shape[0] // int(scalev)))
    vertical = cv2.erode(vertical, verticalStructure, iterations=1)
    vertical = cv2.dilate(vertical, verticalStructure, iterations=1)
    # vertical = cv2.dilate(vertical, np.ones((4, 4)))
    vertical = vertical + cv2.morphologyEx(vertical, cv2.MORPH_GRADIENT, np.ones(
        (4, 4)))  ## ADDDING OUTPUT TO ADDITIONAL LAYER OF EXO SKELETON OF THE LINES

    return horizontal, vertical


def countour_count(bw, scalev=40, scaleh=20, task='table'):
    horizontal, vertical = extract_mask(bw, scalev=scalev, scaleh=20)
    mask = horizontal + vertical

    if task == 'table':
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        parent_area = mask.shape[0] * mask.shape[1]
        areaThr = 0.003 * parent_area
        count = 0
        table_count_dict = {}
        for cnt in contours:
            area = cv2.contourArea(cnt)
            x, y, width, height = cv2.boundingRect(cnt)
            # if  area > areaThr  and  min(width, height) > 12  and  is_single_celled(x, y, x+width, y+height, intersection_coordinates):
            if area > areaThr and min(width, height) > 12:
                table_count_dict[count] = [x, y, x + width - 1, y + height - 1]
                count += 1

        return count

    else:

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        areaThr = 1200
        count = 0
        table_count_dict = {}
        for cnt in contours:
            area = cv2.contourArea(cnt)
            x, y, width, height = cv2.boundingRect(cnt)
            # if  area > areaThr  and  min(width, height) > 12  and  is_single_celled(x, y, x+width, y+height, intersection_coordinates):
            if area > areaThr and min(width, height) > 12:
                table_count_dict[count] = [x, y, x + width - 1, y + height - 1]
                count += 1

        return count


def optimal_params(bw, task='table', scalev=40, scaleh=20):
    if task == 'table':

        vals_v = {i: countour_count(bw, scalev=i, scaleh=20, task='table') for i in np.linspace(30, 60, 10)}
        optimal_scalev = max(vals_v, key=vals_v.get)

        #         optimal_scalev = opt.fminbound(lambda x: countour_count(scalev = x,task = 'table'), 40, 60,xtol=5)

        vals_h = {i: countour_count(bw, scalev=optimal_scalev, scaleh=i, task='table') for i in [10, 20]}
        optimal_scaleh = max(vals_h, key=vals_h.get)

        return round(optimal_scalev), optimal_scaleh

    else:

        vals_v = {i: countour_count(bw, scalev=i, scaleh=20, task='cells') for i in np.linspace(scalev, scalev + 20, 5)}
        max_cnt = max(vals_v.values())
        optimal_scalev = min([int(k) for k in vals_v.keys() if vals_v[k] == max_cnt])

        return optimal_scalev, 20
