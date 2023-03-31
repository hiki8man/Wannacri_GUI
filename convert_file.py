from pathlib import Path
from subprocess import Popen ,PIPE , STDOUT ,call
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication
from time import sleep
import wannacri
import pythonjsonlogger
import sys
import os
import json

star_str = "*"*39
#convert file
class convert_video():
    _translate = QCoreApplication.translate
    ffmpeg_cmd = []
    ffmpeg_path = str(Path("ffmpeg/ffmpeg.exe"))
    ffprobe_path = str(Path("ffmpeg/ffprobe.exe"))
    h264_encode = ""
    file_name = ""
    output_path = ""
    output_name = ""
    file_path = ""
    get_option = ""
    set_message = ""
    set_progress = ""

    def __init__(self,option,progress,message):
        self.get_option = option
        self.set_message = message
        self.set_progress = progress
        self.file_path = str(Path(self.get_option["input"]))
        self.file_name = str(Path(self.get_option["input"]).stem)
        self.output_path = str(self.get_option["output"])
        self.output_name = str(Path.joinpath(Path(self.output_path),Path(self.file_name)))
        self.is_sound_convert = False
    
    def run(self):
        #if crf can't setting, this file is audio or usm
        if self.get_option["is_usm"]:
            self.extractusm(self.file_path)
        elif self.get_option["is_sound"]:
            self.is_sound_convert = True
            self.set_message.emit("Convert OGG......")
            self.OGG_audio()
            self.convert_run()
        else:
            #convert vp9
            if self.get_option["is_vp9"]:
                self.set_message.emit("Convert VP9......")
                self.VP9_video()
                self.convert_run()
            #convert h264
            else:
                self.set_message.emit("Convert H264......")
                self.H264_video()
                self.convert_run_h264()
            #check video sound
            if self.get_option["video_sound"]:
                self.is_sound_convert = True
                self.set_message.emit("Convert OGG......")
                self.OGG_audio()
                self.convert_run()
            os.chdir(str(Path(".\\ffmpeg")))
            self.set_message.emit("Pack to USM......")
            self.createusm(self.output_path)
            Path(self.output_path).unlink()
        #Nuitka use
        os.chdir(sys.path[0])
        #Pyinstaller use
        #os.chdir(os.path.dirname(sys.executable))

    def OGG_audio(self):
        ffmpeg_main = [self.ffmpeg_path,"-i"]
        ffmpeg_input = [self.file_path,"-vn"]
        vol_val = self.get_option["volume"]
        bit_val = str(self.get_option["song_bit"])
        if vol_val < 100:
            vol_val = vol_val / 100
            ffmpeg_input = ffmpeg_input + ["-af","volume="+str(vol_val)]
        ffmpeg_output = ["-b:a",bit_val,
                        "-ar","44100",
                        "-y",
                        self.output_name + ".ogg"]
        self.ffmpeg_cmd = ffmpeg_main + ffmpeg_input + ffmpeg_output
    
    def H264_video(self):
        ffmpeg_main = [self.ffmpeg_path,"-i"]
        ffmpeg_input = [self.file_path,"-an"]
        crf_val = str(self.get_option["crf"])
        bright_val = self.get_option["brightness"]
        self.output_path = self.output_name + ".h264"
        if bright_val != 100:
            bright_val = str(bright_val / 100)
            ffmpeg_input = ffmpeg_input + ["-vf","curves=all='0/0 1/" + bright_val + "'"]
        #use self.h264_encode to change file encode
        if self.get_option["file_codec"].lower() == "h264"  and bright_val == 100:
            self.h264_encode = "copy"
        else:
            self.h264_encode = "libx264"
        ffmpeg_output = ["-c:v",self.h264_encode,
                        "-crf",crf_val,
                        "-y",
                        self.output_path]
        self.ffmpeg_cmd = ffmpeg_main + ffmpeg_input + ffmpeg_output
    
    def VP9_video(self):
        ffmpeg_main = [self.ffmpeg_path,"-i"]
        ffmpeg_input = [self.file_path,"-an"]
        crf_val = str(self.get_option["crf"])
        bright_val = self.get_option["brightness"]
        self.output_path = self.output_name + ".ivf"
        if bright_val != 100:
            bright_val = str(bright_val / 100)
            ffmpeg_input = ffmpeg_input + ["-vf","curves=all='0/0 1/" + bright_val + "'"]
        if self.get_option["file_codec"].lower() == "vp9" and bright_val == 100:
            ffmpeg_output = ["-c:v","copy",
                                "-crf",crf_val,
                                "-y",
                                self.output_path]
        else:
            ffmpeg_output = ["-c:v","vp9",
                            "-crf",crf_val,
                            "-b:v","5000k",
                            "-minrate","2500k","-maxrate","7500k",
                            "-y",
                            self.output_path]
        self.ffmpeg_cmd = ffmpeg_main + ffmpeg_input + ffmpeg_output
    
    def time_convert(self,time):
        time_h = float(time[0:2])
        time_m = float(time[3:5])
        time_s = float(time[6:11])
        time_convert_s = (time_h * 60 * 60) + (time_m * 60) + time_s
        return time_convert_s

    def convert_run(self):
        get_time_start = False
        self.set_progress.emit(0)
        process = Popen(self.ffmpeg_cmd, 
                        shell=True, 
                        stdout=PIPE, 
                        stderr=STDOUT, 
                        encoding="utf-8",
                        text=True)
        for time in process.stdout:
            print(time)
            if time.find("Duration:") != -1:
                file_time_start = time.find("Duration: ") + 10
                file_time_end = time[file_time_start:].find(",") + file_time_start
                time_all = self.time_convert(time[file_time_start:file_time_end])
            if  self.is_sound_convert == True:
                if time.startswith("size=",0,6):
                    get_time_start = True
                else:
                    get_time_start = False
            else:
                if time.startswith("frame",0,6):
                    get_time_start = True
                else:
                    get_time_start = False
            if get_time_start and time.find("time=-") == -1:
                convert_time_str_start = time.find("time") + 5
                convert_time_str_end = time.find(" bitrate=")
                time_now = self.time_convert(time[convert_time_str_start:convert_time_str_end])
                convert_process = (time_now / time_all) * 100
                self.set_progress.emit(int(convert_process))
    
    def convert_run_h264(self):
        self.convert_run()
        #check h264 file
        try:
            check_cmd = [self.ffprobe_path,"-loglevel quiet",self.output_path,"-show_streams","-of","json"]
            file_info = Popen(check_cmd, 
                        shell=True, 
                        stdout=PIPE, 
                        stderr=STDOUT, 
                        encoding="utf-8",
                        text=True)
            get_info = json.load(file_info)
        except:
            self.set_message.emit("Unknow error,use crf convert...")
            self.h264_encode = "libx264"
            self.convert_run()
    
    def createusm(self,file):
        sys.argv=["wannacri","createusm",file,"--output",str(Path(self.get_option["output"]))]
        wannacri.main()
    
    def extractusm(self,file):
        sys.argv=["wannacri","extractusm",file,"--output",str(Path(self.get_option["output"]))]
        print(str(self.get_option["output"]))
        wannacri.main()
