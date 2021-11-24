import matplotlib.pyplot as plt
import numpy as np
from cv2 import cv2
from polynomial import Polynomial
from polynomial_utils import *
from math import ceil, floor, sqrt


class Image_Encryption(object):
    def __init__(self, n, t, k, img, plot_histogram=True, show_image=True, self_debug=True):

        # n: total number of shares
        # t: number of shares required to reconstruct the image
        # k: number of essential shares required to reconstruct the image
        # t-k: minimum number of non-essential shares required to reconstruct the image
        # n-k: total number of non essential shares

        # img = cv2.imread(img_destination)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        # converts to black and white scale
        print("Shape of the image is {}".format(img.shape))
        if show_image == True:  # if showimage was given as 1
            # Display the data as an image  , cmap = gray sets the colormap to grayscale
            plt.imshow(img, cmap="gray")
            plt.xlabel("INPUT IMAGE")  # label the x-axis
            # plt. show() starts an event loop, looks for all currently active figure objects,
            # and opens one or more interactive windows that display the figure.
            plt.show()
        # cv2.imwrite("Original_Image/Image.jpg", img)  # overwriting the image into the orignal images folder

        # Initialising the Class variables
        self.img_info = {}
        if n <= t or t < k:  # checks for the condition of Shamir's algorithm
            raise ValueError("Does not satisfy parameter constraints")
            quit()
        self.n, self.t, self.k = n, t, k
        self.debug = self_debug

        # Initialising alpha for secret shares(shadow images)
        # alpha is n random values from [0,256] for constructing n shares
        self.alpha = []
        temp11 = [i for i in range(257)]  # stores values form 0 to 256
        for i in range(n):
            temp_variable = np.random.choice(
                temp11)  # random element from temp11
            # removing the genrated random elemnt from the possible vals
            temp11.remove(temp_variable)
            self.alpha += [temp_variable]  # append alpha with random variable
        if self_debug == True:
            print("Alpha initialised to --> ", self.alpha)

        # Initialising e (Same procedure as alpha)
        # e is k random values from [0,256] for constructing k essential shares
        temp11 = [i for i in range(257)]  # stores values form 0 to 256
        self.e = []
        for i in range(k):
            temp_variable = np.random.choice(temp11)
            temp11.remove(temp_variable)
            self.e += [temp_variable]
        if self_debug == True:
            print("e initialised to --> ", self.e)

        # Initialising q(x) #Lagrange's Polynomial
        # poly_q is t-k random values from [0,256] for constructing t-k non essential shares
        temp11 = [i for i in range(257)]
        self.poly_q = []
        for i in range(t - k):
            temp_variable = np.random.choice(temp11)
            temp11.remove(temp_variable)
            self.poly_q += [temp_variable]
        self.poly_q = [np.random.randint(1, 257)] + self.poly_q
        if self_debug == True:
            print("q(x) initialised to --> ", self.poly_q)

        if plot_histogram == True:
            s = []
        # img_info is a dict with key as grey scal val & val = [count for that grey scale, list of coordinates each of length k]
        for x in range(img.shape[0]):  # height of ip image
            for y in range(img.shape[1]):  # width of ip image
                if img[x, y] in self.img_info:  # maps the list of points corresponding to the gray value
                    # incrementing count of grey value (for histogram)
                    self.img_info[img[x, y]][0] += 1
                    if (self.img_info[img[x, y]][0] - 1) % k == 0:
                        # increment the value
                        self.img_info[img[x, y]][1] += [[(x, y)]]
                    else:
                        # // integer division
                        self.img_info[img[x, y]][1][(
                            self.img_info[img[x, y]][0] - 1) // k] += [(x, y)]
                else:
                    self.img_info[img[x, y]] = [1, [[(x, y)]]]
                if plot_histogram == True:  # add the value as a bar in the histogram
                    s += [img[x, y]]

        if self_debug == True:
            # Debugging generation of self.img_info
            for i in self.img_info.keys():
                # list of postions (y-coordinate)
                list_of_pos = self.img_info[i][1]
                # traverse the list of list of positions
                for j in range(len(list_of_pos)):
                    if len(list_of_pos[j]) != k:
                        if len(list_of_pos[j]) > k:
                            raise ValueError(
                                "Error cutting the bins of the histogram")
                        elif len(list_of_pos[j]) < k:
                            if j != len(list_of_pos) - 1:
                                raise ValueError(
                                    "Error cutting the bars of the histogram")
                    for p in list_of_pos[j]:
                        # set of points (x , y coordinates)
                        x_pos_var, y_pos_var = p
                        if img[x_pos_var, y_pos_var] != i:  # i is the key of the img_info
                            raise ValueError(
                                "Incorrect encoding of image into image info")
            print("Perfectly encoded the image information into self.img_info")

        # open the info.txt file in write mode.
        info = open("Logs/info.txt", "w")
        # open the img-info.txt file in write mode.
        img_info_file = open("Logs/img_info.txt", "w")

        for i in self.img_info.keys():  # key values of img_info
            # writing i:self.img_info[i][0] in img_info_file
            img_info_file.write("{}:{}\n".format(i, self.img_info[i][0]))
            # -1 is last index
            for j in range(k - len(self.img_info[i][1][-1])):
                # adds from the last index with random (x,y)
                self.img_info[i][1][-1] += [(np.random.randint(0, 256),
                                             np.random.randint(0, 256))]
            if self_debug == True:
                # Debugging padding self.img_info
                if len(self.img_info[i][1][-1]) != k:
                    raise ValueError(
                        "Incorrect padding of the bars of self.img_info")
            info.write("Pixel_value -> {}, number of positions -> {}, locations by bars -> {}\n".format(
                i, self.img_info[i][0], self.img_info[i][1]))
        info.close()  # close the info.txt
        img_info_file.close()  # close the img_info_file.txt
        if self_debug == True:
            print("Perfectly padded self.img_info")

        if plot_histogram == True:  # plotting the histogram:
            s = np.array(s)
            plt.hist(s, bins=255)  # points to be considered on x-axis
            plt.xlabel("Grey scale values")
            plt.ylabel("Number of occurrences")
            plt.show()

    # shares of Shamir alg.
    def generate_shadow_images(self, store_shadows=True):
        print("Encryption begins!")
        img_info = self.img_info
        n, t, k = self.n, self.t, self.k
        # alpha is of dimension n, values where we evaluate lagrange's polynomial
        # e is of dimension k
        # poly_q is of dimension t-k
        alpha = self.alpha
        e = self.e
        poly_q = self.poly_q

        shadow_image_size = None
        shadow_images = []

        for i in range(n):  # n is total number of shares
            print("Shadow Image no :- {}".format(i))
            x_secrets = []
            y_secrets = []
            # Generating Lagrange's Polynomial
            lagrange = get_Lagrange_Polynomials(e)
            prod_fun = get_prod_funs(e)

            temp_poly = Polynomial(poly_q)  # create object class polynomial
            temp_poly = temp_poly.multiply(prod_fun)

            # e values should be root of temp_poly
            if self.debug == True:
                # For debugging whether the first term of the generated polynomial is correct
                for m in range(len(e)):
                    # evaluating temp_poly for e[m]
                    value = temp_poly.eval(e[m])
                    if value != 0:
                        raise ValueError(
                            "First term of the encrypting polynomial is wrong")
                        quit()

                # For debugging whether the generated Lagrange Polynomial is correct
                # delta function in lagrange's polynomial
                for n in range(len(e)):
                    for j in range(len(lagrange)):
                        if n != j:
                            if lagrange[j].eval(e[n]) != 0:
                                raise ValueError("Lagrange Polynmial is wrong")
                        else:
                            if lagrange[j].eval(e[n]) != 1:
                                raise ValueError(
                                    "Lagrange Polynomial is wrong")
            # iterating through all grey values
            for x in img_info.keys():
                # coordinates arranged in list of size k, having grey val x
                for y in range(len(img_info[x][1])):
                    sum_polyx = Polynomial([0])
                    sum_polyy = Polynomial([0])
                    for u in range(k):
                        s_x = img_info[x][1][y][u][0]  # x coordinate
                        s_y = img_info[x][1][y][u][1]  # y coordinate
                        tempx = (lagrange[u]).multiply(Polynomial([s_x]))
                        tempy = (lagrange[u]).multiply(Polynomial([s_y]))
                        sum_polyx = sum_polyx.add(tempx)
                        sum_polyy = sum_polyy.add(tempy)
                    x_poly = temp_poly.add(sum_polyx)
                    y_poly = temp_poly.add(sum_polyy)
                    x_secrets += [x_poly.eval(alpha[i])]
                    y_secrets += [y_poly.eval(alpha[i])]
            temp_shadow = x_secrets + y_secrets
            if shadow_image_size is None:
                temp_size = len(temp_shadow)
                # finding closest perfect square greater than temp_size
                while 1:
                    if floor(sqrt(temp_size)) == ceil(sqrt(temp_size)):
                        break
                    else:
                        temp_size += 1
                        # maybe temp_size -= 1
                shadow_image_size = temp_size
            # padding new shadow image to generate remaining pixel values
            temp_shadow = temp_shadow + \
                [np.random.randint(0, 256) for u in range(
                    len(x_secrets + y_secrets), shadow_image_size)]
            temp_shadow = np.array(temp_shadow).astype(int)
            # resizing to 2d matrix
            temp_shadow = temp_shadow.reshape(
                (int(sqrt(shadow_image_size)), int(sqrt(shadow_image_size))))
            invalid_positions = []
            for x in range(temp_shadow.shape[0]):
                for y in range(temp_shadow.shape[1]):
                    if temp_shadow[x, y] == 256:
                        invalid_positions += [(x, y)]
                        temp_shadow[x, y] = 255
            if store_shadows == True:
                cv2.imwrite("Shadows/{}.jpg".format(i), temp_shadow)
            shadow_images += [(temp_shadow, invalid_positions)]
        print("Encryption ends!")

        return shadow_images

    def decrypt_image(self, shadow_images, num_shadow_images_available, show_decrypted_image=True):
        print("Decryption begins!")
        n, k, alpha, e, img_info = self.n, self.k, self.alpha, self.e, self.img_info
        t = num_shadow_images_available + 1

        content_ = get_content_from_file("Logs\\img_info.txt")

        new_img_info = {}
        total_num_bars = 0

        # To get the actual number of information encrypted pixels in the original image
        for i in range(len(content_)):
            if content_[i][1] % k == 0:
                total_num_bars += content_[i][1] // k
            else:
                total_num_bars += (content_[i][1] // k) + 1

        # Obtain required number of shadow images
        shadows, final_invalid_pos, final_alpha = get_random_t_images(
            shadow_images, alpha, t)

        count_x = 0
        count_y = total_num_bars
        file_open = open("Logs\\reconstructed_img_info.txt", "w")
        for i in range(len(content_)):
            new_img_info[content_[i][0]] = []
            for j in range(0, content_[i][1], k):
                alpha_poly_x = []
                alpha_poly_y = []
                for p in range(t):
                    poly_alpha_x = shadows[p][count_x]
                    poly_alpha_y = shadows[p][count_y]
                    if count_x in final_invalid_pos[p]:
                        poly_alpha_x = 256
                    if count_y in final_invalid_pos[p]:
                        poly_alpha_y = 256
                    alpha_poly_x += [poly_alpha_x]
                    alpha_poly_y += [poly_alpha_y]
                x_reconstructed_polynomial = reconstruct_polynomial(
                    final_alpha, alpha_poly_x)
                y_reconstructed_polynomial = reconstruct_polynomial(
                    final_alpha, alpha_poly_y)
                if self.debug == True:
                    if count_x == 0:
                        debug_reconstructed_polynomial(
                            x_reconstructed_polynomial, final_alpha, alpha_poly_x)
                        print("Debugged Reconstructed x polynomial")
                        debug_reconstructed_polynomial(
                            y_reconstructed_polynomial, final_alpha, alpha_poly_y)
                        print("Debugged Reconstructed y polynomial")
                iterator = k if (content_[i][1] - j >=
                                 k) else (content_[i][1] - j)
                for p in range(iterator):
                    new_img_info[content_[
                        i][0]] += [(x_reconstructed_polynomial.eval(e[p]), y_reconstructed_polynomial.eval(e[p]))]
                count_x += 1
                count_y += 1

        for i in new_img_info.keys():
            file_open.write(
                "Pixel value --> {} at positions --> {}\n".format(i, new_img_info[i]))
        file_open.close()

        original_image = np.array(get_original_image_back(
            new_img_info, 256)).reshape((256, 256))
        print("Decryption ends!")

        cv2.imwrite("decrypted.jpg", original_image)

        if show_decrypted_image == True:
            plt.imshow(original_image, cmap="gray")
            plt.xlabel("DECRYPTED IMAGE")
            plt.show()

        return original_image
