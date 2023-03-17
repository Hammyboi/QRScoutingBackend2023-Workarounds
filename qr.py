import argparse
import numpy as np
from pyzbar.pyzbar import decode
import cv2
import tomllib

parser = argparse.ArgumentParser(description="qr code scanner to text file")
parser.add_argument("-v", "--verbose", action="store_true")
args = parser.parse_args()


# def save(values):
#     with open(args.file, "a") as output_file:
#         if len(v) != 0:
#             for i in values:
#                 output_file.write(i + "\n")
#             print("SAVED! ( ͡° ͜ʖ ͡°)\n")
#         else:
#             print("SAVED NOTHING! ¯\\_(ツ)_/¯\n")


def main():
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)
    # data = pd.read_csv(config["output_file"], sep='\t')
    cap = cv2.VideoCapture(config["camera_id"])
    data_submitted = []
    while True:
        ret, frame = cap.read()
        gray_img = cv2.cvtColor(frame, 0)
        barcode = decode(gray_img)
        for obj in barcode:
            points = obj.polygon
            (x, y, w, h) = obj.rect
            pts = np.array(points, np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, (0, 255, 0), 3)
            barcode_data = obj.data.decode("utf-8")
            barcode_type = obj.type
            string = str(barcode_data) + " | Type " + str(obj.type)
            cv2.putText(
                frame, string, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2
            )
            if args.verbose:
                print("QR: " + barcode_data + " | Type: " + barcode_type)
            if barcode_data not in data_submitted:
                data_submitted.append(barcode_data)
                with open(config["output_file"], "a") as output_file:
                    for char in range(0, len(string)):
                        try:
                            output_file.write(string[char])
                        except:
                            output_file.write("'")

                    output_file.write("\n")
                print("QR:" + barcode_data)
                print("SAVED! ( ͡° ͜ʖ ͡°)")

        cv2.imshow("QR SCANNER", frame)
        code = cv2.waitKey(10)
        if code == ord("s"):
            pass
        elif code == ord("p"):
            for data in data_submitted:
                print(data)
        elif code == ord("q"):
            break


if __name__ == "__main__":
    main()
