from pathlib import Path

from torch import true_divide
from tqdm.auto import tqdm
from torch.utils import data
from torchvision import datasets, transforms

import sys, threading, time, os, gzip, shutil,requests
from threading import Thread

stop_down = False



class Downloader:



    def __init__(self):
        self.stop_down = False








    def download(self):
    
        urls = open("urls.txt").read().splitlines()
        download_dir = Path('mnist_data/EMNIST/raw')
        download_dir.mkdir(parents=True, exist_ok=True)
        

        while not self.stop_down:
        
            for url in tqdm(urls):
                
                filename = Path(url).name #get filename
                   
                response = requests.get(url) #download 
     
                download_dir.joinpath(filename).write_bytes(response.content) #download to the specific directory
                #os.chdir('mnist_data/MNIST/raw/')  # full directory name
                string1 = "mnist_data/MNIST/raw/" + filename
                with gzip.open(string1, 'rb') as f_in:   #unzip gz file into ubyte file
                    with open(string1[:string1.rfind(".")], 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
     
                #os.chdir("../../..") #change to upper directory 
            self.stop_down = True
                

    
           
        self.loadDataSet()


    def loadDataSet(self):
        batch_size = 128
    
        self.train_dataset = datasets.EMNIST(root='mnist_data/',train=True,split="byclass",
        transform=transforms.ToTensor(),download=True)
    
        self.test_dataset = datasets.EMNIST(root='mnist_data/',train=False,split="byclass",
        transform=transforms.ToTensor())
    



if __name__ == "__main__":
    down = Downloader()
    down.loadDataSet()


 


 
