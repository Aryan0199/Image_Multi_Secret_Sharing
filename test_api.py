from Encrypt import *
import cv2
import os
import shutil
import pathlib

current_working_dir = os.getcwd()
shadow_folder_path = current_working_dir + "\Shadows"
logs_folder_path = current_working_dir + "\Logs"

pathlib.Path(shadow_folder_path).mkdir(parents=True, exist_ok=True)
pathlib.Path(logs_folder_path).mkdir(parents=True, exist_ok=True)

for file_object in os.listdir(shadow_folder_path):
    file_object_path = os.path.join(shadow_folder_path, file_object)
    if os.path.isfile(file_object_path) or os.path.islink(file_object_path):
        os.unlink(file_object_path)
    else:
        shutil.rmtree(file_object_path)


print("Please enter the filename of the image to be encrypted")

file_name = "img.jpg"
img = cv2.imread(file_name)
# print(img)
# cv2.imwrite("img1.jpg", img)  # overwriting the file name with img1.jpg
# a, b, c = cv2.split(img)
print("The initial shape of the image is {} and the type of the matrix is {}".format(img.shape, type(img)))
print("Please enter the value of n, t and k seperated by spaces")
n, t, k = list(map(int, input().split(" ")))

# whether to show the histogram or not
print("Enter 1 to display the histogram else enter 0")
temp = int(input())
plot_hist = True if temp == 1 else False

# whether to display the input image or not
print("Enter 1 to show the input image else enter 0")
temp = int(input())
show_image = True if temp == 1 else False

test = Image_Encryption(n=n, t=t, k=k, img=img, plot_histogram=plot_hist, show_image=temp, self_debug=True)
shadow_imagesa = test.generate_shadow_images(store_shadows=True)
print("Shadow Images stored in folder Shadows")
