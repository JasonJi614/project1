import sys,string
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QProgressBar
from PyQt5.QtCore import QBasicTimer
from pathlib import Path

from torch import true_divide
from tqdm.auto import tqdm
from torch.utils import data 
from torchvision import datasets, transforms
from torchvision.datasets.utils import extract_archive,download_and_extract_archive,check_integrity
import sys, threading, time, os, shutil
from urllib.error import URLError
import urllib.request

import math as m


class MyApp(QWidget):

    url = "https://www.itl.nist.gov/iaui/vip/cs_links/EMNIST/gzip.zip"
    #url = "http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz"
    
    md5 = "58c8d27c78d21e728a6bc7b3cc06412e"
    splits = ("byclass", "bymerge", "balanced", "letters", "digits", "mnist")
    filename = os.path.basename(url)
    # Merged Classes assumes Same structure for both uppercase and lowercase version
    _merged_classes = {"c", "i", "j", "k", "l", "m", "o", "p", "s", "u", "v", "w", "x", "y", "z"}
    _all_classes = set(string.digits + string.ascii_letters)
    classes_split_dict = {
        "byclass": sorted(list(_all_classes)),
        "bymerge": sorted(list(_all_classes - _merged_classes)),
        "balanced": sorted(list(_all_classes - _merged_classes)),
        "letters": ["N/A"] + list(string.ascii_lowercase),
        "digits": list(string.digits),
        "mnist": list(string.digits),
    }


    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.pbar1 = QProgressBar(self)
        self.pbar1.setGeometry(30, 40, 200, 25)

        self.btn = QPushButton('Download', self)
        self.btn.move(40, 80)
        self.btn.clicked.connect(self.doAction)

        self.directory_location = 'mnist_data/EMNIST/raw'
        self.download_dir = Path(self.directory_location)
        self.full_size = 64985
        self.buttonLock = False
        self.stopdownload = False
        self.total_dir_size =0
 
        self.setWindowTitle('QProgressBar')
        self.setGeometry(300, 300, 300, 200)
        self.show()




    def iniDirectory(self):
        if os.path.exists(self.directory_location):
            shutil.rmtree(self.directory_location)
            self.download_dir.mkdir(parents=True, exist_ok=True)
        else:
            self.download_dir.mkdir(parents=True, exist_ok=True)



    def doAction(self):
        if self.buttonLock:
            self.buttonLock = False
            self.stopdownload = True
            self.btn.setText('Restart')

        else:
            self.restart()
            self.btn.setText('Stop')
            #self.iniDirectory() 
            time.sleep(0.5)
            if not self.stopdownload :
                t1 = threading.Thread(target = self.downloadDataSet)
                #t2 = threading.Thread(target = self.updatepbar)
                t1.start()
                #t2.start()

            self.buttonLock = True
            self.stopdownload = False
            
    def restart(self):
        self.pbar1.setValue(0)
        self.total_dir_size =0
        

    # def updatepbar(self):

    #     self.total_dir_size =0
    #     while self.total_dir_size < 561753746:
    #         if self.stopdownload:
    #             break

    #         self.total_dir_size =  0
    #         for file in os.scandir(self.directory_location):
    #             self.total_dir_size += file.stat().st_size /1024    
               
    #         percentage = self.total_dir_size / 5617537.46
    #         number = m.trunc(percentage)
    #         self.pbar1.setValue(number)
               
    #     if not self.stopdownload:
    #         self.btn.setText('Finished')


    def downloadDataSet(self):

        os.makedirs(self.directory_location, exist_ok=True)
        #download_and_extract_archive(self.url, download_root=self.directory_location, md5=self.md5)
        self.directory_location = os.path.expanduser(self.directory_location)

        fpath = os.path.join(self.directory_location, self.filename)
        i = 0

        # with urllib.request.urlopen(urllib.request.Request(self.url, headers={"User-Agent": "pytorch/vision"})) as response:
        #     with open(fpath, "wb") as fh, tqdm(total=response.length) as pbar:
        #         for chunk in iter(lambda: response.read(1024*32), b""):
        #             i = i+1

        #             # filter out keep-alive new chunks
        #             if not chunk:
        #                 continue

        #             if not self.stopdownload:
        #                 fh.write(chunk)
        #                 pbar.update(len(chunk))
        #                 x = m.trunc((len(chunk) *i)/5617537.46)
        #                 print(x)
        #                 self.pbar1.setValue(x)
                        
        #             else:
                        
        #                 while self.stopdownload:
        #                     n =1
                            
        self.train_dataset = datasets.EMNIST(root='mnist_data/',train=True,split="byclass",
        transform=transforms.ToTensor(),download=True)
      
        self.test_dataset = datasets.EMNIST(root='mnist_data/',train=False,split="byclass",
        transform=transforms.ToTensor())
        # if not self.stopdownload:
        #     archive = os.path.join(self.directory_location, self.filename)
        #     extract_archive(archive, self.directory_location)

        #     gzip_folder = os.path.join(self.directory_location, "gzip")
        #     os.makedirs(gzip_folder, exist_ok=True)

        #     for gzip_file in os.listdir(gzip_folder):
        #         print(gzip_file)
        #         if gzip_file.endswith(".gz"):
        #             extract_archive(os.path.join(gzip_folder, gzip_file), self.directory_location)

        #     shutil.rmtree(gzip_folder)


        
        # os.makedirs(self.directory_location, exist_ok=True)

        # # download files

        # for filename, md5 in self.resources:
        #     for mirror in self.mirrors:
        #         url = f"{mirror}{filename}"
              
        #         try:
        #             self.directory_location = os.path.expanduser(self.directory_location)

        #             fpath = os.path.join(self.directory_location, filename)
        #             if not self.stopdownload:
        #                 with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "pytorch/vision"})) as response:   
        #                     with open(fpath, "wb") as fh, tqdm(total=response.length) as pbar:
        #                         for chunk in iter(lambda: response.read(500), b""):
        #                             if not chunk:
        #                                 continue

        #                             if not self.stopdownload:
        #                                  fh.write(chunk)
        #                                  pbar.update(len(chunk))

        #             if not self.stopdownload: 
        #                 archive = os.path.join(self.directory_location, filename)
        #                 extract_archive(archive, self.directory_location, False)
                      
        #         except URLError as error:
        #             print(f"Failed to download (trying next):\n{error}")
        #             continue
        #         finally:
        #             print()
        #         break
        #     else:
        #         raise RuntimeError(f"Error downloading {filename}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
