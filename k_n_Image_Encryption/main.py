from datetime import datetime
import os
import pathlib
from PIL import Image
import numpy as np
import shutil
from simple_term_menu import TerminalMenu

from image_encryption import reconstruct_image, split_parts_list

if __name__ == "__main__":
    print('Select an image for encryption:')
    current_working_dir = os.getcwd()
    shadow_folder_path = current_working_dir + "/Shadows"

    pathlib.Path(shadow_folder_path).mkdir(parents=True, exist_ok=True)

    for file_object in os.listdir(shadow_folder_path):
        file_object_path = os.path.join(shadow_folder_path, file_object)
        if os.path.isfile(file_object_path) or os.path.islink(file_object_path):
            os.unlink(file_object_path)
        else:
            shutil.rmtree(file_object_path)

    print(" Encryption ".center(50, "-"))
    # path_image = input("Enter the name of the image: ")


if __name__ == "__main__":
    temo = "k_n_reconstructed_image.jpg"
    if os.path.isfile(temo):
        os.remove(temo)

    path_image = "sample2.jpg"
    flag = True
    while flag:
        options = os.listdir(os.getcwd())
        # options = ["entry 1", "entry 2", "entry 3"]
        terminal_menu = TerminalMenu(options)
        menu_entry_index = terminal_menu.show()
        if options[menu_entry_index].endswith(('.png', '.jpg', '.jpeg', '.tiff')):
            print(f"You have the image: {options[menu_entry_index]}!")
            path_image = options[menu_entry_index]
            flag = False

    if path_image is None:
        print("No image selected")
        exit(1)

    n = int(input("Enter the number of shares (n): "))
    k = int(input("Enter the number of required shares (k): "))

    t1 = datetime.now()
    pic = Image.open(path_image)
    matrix = np.array(pic, np.int32)
    shares = split_parts_list(n, k, 257, matrix, path_image)
    t2 = datetime.now()
    print("Time taken for encryption: ", t2 - t1)
    print("Encrypted images stored under Shadows folder")
    print()
    print(" Decryption ".center(50, "-"))
    print('Select shares for decryption:')
    t1 = datetime.now()

    # selected_shares = []
    # for _ in range(k):
    #     shr = input(f"Select share #{_ + 1}:")
    #     if shr not in os.listdir(shadow_folder_path):
    #         print("No such file!")
    #         continue
    #     else:
    #         selected_shares.append(shr)

    shadow_folder_content_name = os.listdir(shadow_folder_path)
    terminal_menu = TerminalMenu(shadow_folder_content_name, multi_select=True,
                                 show_multi_select_hint=True, multi_select_select_on_accept=False, multi_select_empty_ok=True)
    terminal_menu.show()
    selected_shares = terminal_menu.chosen_menu_entries
    user_shares = [shadow_folder_path + "/" +
                   i for i in selected_shares]
    if len(user_shares) == 0:
        raise Exception("No shares selected")
    elif len(user_shares) < k:
        flag = input("Not enough shares selected. Continue? (y/n): ")
        if flag == "y":
            # pad the input with last value
            print("Padding the shares with last selected image")
            for i in range(k - len(user_shares)):
                user_shares.append(user_shares[-1])
        else:
            raise Exception("Not enough shares selected")
    print(
        f'The shares selected by the user are: {selected_shares}')

    print("\nReconstructing the image...")
    reconstructed_matrix = reconstruct_image(user_shares, k, 257, shares)
    new_img = Image.fromarray(reconstructed_matrix.astype("uint8"), "RGB")
    new_img.save("k_n_reconstructed_image.jpg")
    t2 = datetime.now()
    print("Time taken for decryption: ", t2 - t1)
    print("Decrypted image stored at k_n_reconstructed_image.jpg")
