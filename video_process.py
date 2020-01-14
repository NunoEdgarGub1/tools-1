
import cv2
import os

def convert_video_to_images (input_file, output_folder):
    try:
        os.mkdir (output_folder)
    except OSError:
        pass

    cap = cv2.VideoCapture (input_file)
    nr_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))-1
    print ("Number of frames:", nr_frames)
    count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        cv2.imwrite (output_folder + "/%#05d.jpg" % (count+1), frame)
        count += 1
        
        if (count > (nr_frames-1)):
            cap.release()
            print ("Done!")
            break


if __name__ == '__main__':
    input_file = r'C:\Users\cristian\Downloads\2020-01-15_25_33.avi'
    output_folder = r"C:\Users\cristian\Downloads\test"
    convert_video_to_images (input_file = input_file, output_folder = output_folder)

