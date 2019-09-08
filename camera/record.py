import cv2
import time
import sounddevice as sd
from scipy.io.wavfile import write
import os


def record_video():
    tstamp = int(time.time())
    out = cv2.VideoWriter('output/output_{}.mp4'.format(tstamp), fourcc, 20.0, (width, height))
    ret, frame = cap.read()
    if ret:
        out.write(frame)
    rec = sd.rec(int(10 * fs), samplerate=fs, channels=2)
    while(tstamp + 10 >= int(time.time())):
        ret, frame = cap.read()
        if ret:
            out.write(frame)
        else:
            break
    write('output/output_{}.wav'.format(tstamp), fs, rec)
    out.release()
    os.system("ffmpeg -i output/output_{}.mp4 -i output/output_{}.wav -c:v copy -shortest -c:a aac -strict  experimental output/output_joined_{}.mp4".format(tstamp, tstamp, tstamp))


if __name__ == "__main__":
    fs = 44100 # audio sample rate
    cap = cv2.VideoCapture(0) # Capture video from camera
    # Get the width and height of frame
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
    # Define the codec and create VideoWriter object
    while(1):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use the lower case
        record_video()
    cap.release()
    cv2.destroyAllWindows()
