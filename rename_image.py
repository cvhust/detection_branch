import os

working_dir = "./all_data_hand_detect/"
file_list = os.listdir(working_dir)
file_list = sorted(file_list)
for file_name in file_list:
    splitted = file_name.split(".")
    if len(splitted) > 2:
        splitted.pop(1)
        new_name = ".".join(splitted)
        os.rename(os.path.join(working_dir, file_name), os.path.join(working_dir, new_name))
    else:
        print("OK")
