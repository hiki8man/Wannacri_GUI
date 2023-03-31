#convert option

from sys import argv , exit
from pathlib import Path
from PySide6.QtWidgets import QMainWindow
class convert_option():
    MyGUi = ""
    def __init__(self,MyUi):
        self.MyGUi = MyUi
    def run(self):
        print(len(argv))
        if len(argv) > 1:
            file_check = Path(argv[1])
            if file_check.is_file():
                self.MyGUi.lineEdit.setText(str(Path(argv[1]).absolute()))
                self.codec(argv)
                self.volume(argv)
                self.CRF(argv)
                self.brightness(argv)
    def is_number(self,s):    
        try:    
            float(s)        
            return True    
        except ValueError:
            pass   
        try:        
            import unicodedata   
            unicodedata.numeric(s)     
            return True    
        except (TypeError, ValueError):        
            pass    
            return False

    def codec(self,codec_check=[]):
        if codec_check.count("-vp9") != 0 or codec_check.count("vp9") != 0:
            self.MyGUi.radioButton_4.setChecked(True)
        elif codec_check.count("-h264") != 0 or codec_check.count("h264") != 0:
            self.MyGUi.radioButton_5.setChecked(True)

    def volume(self,volume_check=[]):
        if volume_check.count("-vol") != 0 and volume_check[volume_check.index("-vol") + 1].isdigit():
            volume = float(volume_check[volume_check.index("-vol") + 1])
            self.MyGUi.doubleSpinBox.setValue(volume)
        elif volume_check.count("vol") != 0 and volume_check[volume_check.index("vol") + 1].isdigit():
            volume = float(volume_check[volume_check.index("vol") + 1])
            self.MyGUi.doubleSpinBox.setValue(volume)

    def CRF(self,crf_check=[]):
        #set crf
        if crf_check.count("-crf") != 0 and crf_check[crf_check.index("-crf") + 1].isdigit():
            crf_val = int(crf_check[crf_check.index("-crf") + 1])
            self.MyGUi.spinBox.setValue(crf_val)
        elif crf_check.count("crf") != 0 and crf_check[crf_check.index("crf") + 1].isdigit():
            crf_val = int(crf_check[crf_check.index("crf") + 1])
            self.MyGUi.spinBox.setValue(crf_val)
    
    def brightness(self,brightness_check=[]):
        #set crf
        if brightness_check.count("-brightness") != 0 and brightness_check[brightness_check.index("-brightness") + 1].isdigit():
            brightness_val = float(brightness_check[brightness_check.index("-brightness") + 1])
            self.MyGUi.doubleSpinBox_2.setValue(brightness_val)
        elif brightness_check.count("brightness") != 0 and brightness_check[brightness_check.index("brightness") + 1].isdigit():
            brightness_val = float(brightness_check[brightness_check.index("brightness") + 1])
            self.MyGUi.doubleSpinBox_2.setValue(brightness_val)

    def outpath(self,outpath_check=[]):
        #set crf
        if outpath_check.count("-output") != 0:
            output_val = outpath_check[outpath_check.index("-output") + 1]
            Path(output_val).mkdir(parents=True, exist_ok=True)
            self.MyGUi.lineEdit_2.setText(str(Path(output_val).absolute()))
            return True
        elif outpath_check.count("output") != 0:
            output_val = outpath_check[outpath_check.index("-output") + 1]
            Path(output_val).mkdir(parents=True, exist_ok=True)
            self.MyGUi.lineEdit_2.setText(str(Path(output_val).absolute()))
            return True
        return False

if __name__ == "__main__":
    test = convert_option()
    test.run
    
