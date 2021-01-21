import numpy as np
from PIL import Image
from scipy import optimize as opt
from scipy.ndimage import interpolation as inter
import cv2
import time


class Preprocess:
    def __init__(self):
        pass

    def deskew_optimized(self, image, image_shape):

        # Optmized script.  ~98-99% correct.  ~15X faster than the original.
        # image = self.image
        bin_img = 1 - \
                  np.array(Image.fromarray(image).convert('1')).astype('uint8')
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

        #        print('[OPT] Best rotation angle:', round(best_angle, 2))

        #        Rotating the image
        #        image = cv2.imread(image_name)
        (h, w) = image_shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h),
                                 flags=cv2.INTER_CUBIC,
                                 borderMode=cv2.BORDER_REPLICATE)
        return rotated, round(best_angle, 2)

    def denoise(self, deskewed, denoise_strength):
        img = cv2.fastNlMeansDenoising(deskewed, h=denoise_strength)

        return (img)

    def set_processed_image(self, processed_image):
        self.processed_image = processed_image

    def preprocess2(self):
        t = time.time()

        # Choose one of the two -
        # out_im, angle  =  deskew_original('Pages/' + page_image)
        out_im, angle = deskew_optimized(self.image)
        adjusted = adjust_gamma(out_im, gamma=0.2)
        denoised_table = denoise(adjusted, denoise_strength=20)
        blured_table = cv2.bilateralFilter(denoised_table, 9, 30, 30)

        # cv2.imwrite(os.getcwd()+'/' + path[:-4] + '_prep_for_text.png', denoised_table)
        #     cv2.imwrite('Deskewed_Pages/' + page_image[:-4] + '__deskewed.png', out_im)

        time_taken = str(round(time.time() - t, 2)) + 's'

        print('\nDESKEWED FILENAME:', path,
              '\nANGLE OF ROTATION:', angle,
              '\nTIME TAKEN:', time_taken,
              '\nDENOISED IMAGE',
              '\nADJUSTED GAMMA')  # monitor progress.

        return blured_table

    def preprocess1(path):
        t = time.time()

        # Choose one of the two -
        # out_im, angle  =  deskew_original('Pages/' + page_image)
        out_im, angle = deskew_optimized(path)
        #     adjusted = adjust_gamma(image, gamma=0.2)
        denoised_table = denoise(out_im, denoise_strength=20)
        blured_table = cv2.bilateralFilter(denoised_table, 9, 30, 30)

        time_taken = str(round(time.time() - t, 2)) + 's'

        print('\nDESKEWED FILENAME:', path,
              '\nANGLE OF ROTATION:', angle,
              '\nTIME TAKEN:', time_taken,
              '\nDENOISED IMAGE',
              '\nADJUSTED GAMMA')  # monitor progress.
        return blured_table

    def parse(self, image, table_count, flag='BASE MODULE'):
        if flag == 'BASE MODULE':
            pass
        else:
            if table_count(image) >= 3:
                imagepp = preprocess1(path)
            else:
                imagepp = preprocess2(path)

    def pre_process(self, image, image_shape):
        deskewed, _ = self.deskew_optimized(image, image_shape)
        denoised = self.denoise(deskewed, 20)
        blured_table = cv2.bilateralFilter(denoised, 9, 30, 30)
        return deskewed, denoised, blured_table
