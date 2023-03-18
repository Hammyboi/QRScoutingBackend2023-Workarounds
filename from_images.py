import os
from pyzbar.pyzbar import decode
import cv2
import tomllib

with open("config.toml", "rb") as f:
    config = tomllib.load(f)
with open(config["output_file"], "r") as file:
    data_submitted = file.read().splitlines()

for filename in os.listdir(os.path.join(os.getcwd(), config["image_dir"])):
    image = cv2.imread(os.path.join(os.getcwd(), config["image_dir"], filename), cv2.IMREAD_GRAYSCALE)
    try:
        barcode = decode(image)
        for obj in barcode:
            barcode_data = obj.data.decode("utf-8")
            barcode_type = obj.type
            string = str(barcode_data) + " | Type " + str(obj.type)
        if barcode_data not in data_submitted and string not in data_submitted:
            data_submitted.append(barcode_data)
            with open(config["output_file"], "a") as output_file:
                for char in range(0, len(string)):
                    try:
                        output_file.write(string[char])
                    except:
                        output_file.write("'") # if error, ignore the error

                output_file.write("\n")
            print("QR:" + barcode_data)
            print("SAVED! ( ͡° ͜ʖ ͡°)")
        else:
            print("duplicate")
    except TypeError:
        pass

# checking for duplicates AGAIN (Can't have enough checking)
file = open(config["output_file"], "r")
in_lines = file.readlines()
file.close()
out_file = open(config["output_file"], "w")
write_lines = []
lines = []
num_dupes = 0
num_copied = 0
for line in in_lines:
    duplicate = False
    for line_line in lines:
        if line == line_line:
            duplicate = True
    lines.append(line)
    if not duplicate:
        write_lines.append(line)
        num_copied += 1
    else:
        num_dupes += 1
print("Duplicates: " + str(num_dupes) + " Copied: " + str(num_copied))
out_file.writelines(write_lines)
out_file.close()