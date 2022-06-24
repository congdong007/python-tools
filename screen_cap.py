from pickle import TRUE
import pyaudio
import wave
from PIL import ImageGrab
import cv2
import threading
import time
from numpy import array
from moviepy.editor import *
import os

fileName = time.strftime('%Y-%m-%d',time.localtime(time.time())) 

file_path = os.getcwd() + r"/video"

if not os.path.exists(file_path):
    os.makedirs(file_path)

file_path = file_path + r"/" + fileName

file_path_tmp = file_path + r"/tmp_" + fileName

wav_file = file_path + r"/output.wav"

print(file_path)

fps = 24
record_seconds = 10*60


class PyRecord:
    def __init__(self, file_path="test"):
        self.allow_record = True
        self.file_path = file_path

    def record_audio(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        p = pyaudio.PyAudio()
        stream = p.open(rate=RATE,channels=1,format=FORMAT,input=True,frames_per_buffer=CHUNK)
        wf = wave.open(self.file_path + ".wav", "wb")
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)

        while self.allow_record:
            data = stream.read(CHUNK)
            wf.writeframes(data)

        stream.stop_stream()
        stream.close()
        p.terminate()
        wf.close()

    def record_screen(self):
        im = ImageGrab.grab()
        video = cv2.VideoWriter(
            self.file_path + ".mp4", cv2.VideoWriter_fourcc(*"MP4V"), fps, im.size
        )
        while self.allow_record:
            im = ImageGrab.grab()
            im = cv2.cvtColor(array(im), cv2.COLOR_RGB2BGR)
            video.write(im)
        video.release()

    def compose_file(self):
        print("combine video & audio file")
        print(self.file_path)
        audio = AudioFileClip(self.file_path + ".wav")
        video = VideoFileClip(self.file_path + ".mp4")
        ratio = audio.duration / video.duration
        video = video.fl_time(lambda t: t / ratio, apply_to=["video"]).set_end(
            audio.duration
        )
        video = video.set_audio(audio)
        video = video.volumex(10)
        video.write_videofile(self.file_path + "_out.mp4", codec='mpeg4')
        video.close()

    def remove_temp_file(self):
        print("delete tmp files")
        os.remove(self.file_path + ".wav")
        os.remove(self.file_path + ".mp4")

    def stop(self):
        print("stopping...")
        self.allow_record = False
        time.sleep(1)
        self.compose_file()
        self.remove_temp_file()

    def run(self):
        t = threading.Thread(target=self.record_screen)
        t1 = threading.Thread(target=self.record_audio)
        t.start()
        t1.start()
        print("start capturing...")

def main():
    try:
        print(file_path)

        pr = PyRecord(file_path)
        pr.run()
        time.sleep(2)

        for i in range(int(record_seconds * fps)):
            if cv2.waitKey(1) == ord("q"):
                break  
    except KeyboardInterrupt:
        print('**************************')
        pass
    
    pr.stop()

  
        
if __name__ == "__main__":
    main()           

