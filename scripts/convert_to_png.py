import sys,os,shutil
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout,QFormLayout,QScrollArea,QGroupBox,QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from torch.utils import data
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np 

class MyApp(QWidget):



    def __init__(self):
        super().__init__()
        self.initUI()
        



    def initUI(self):

        self.full_img_dir = Path('mnist_img/full')
        self.filter_img_dir = Path('mnist_img/filter')
        self.full_img_dir.mkdir(parents=True, exist_ok=True)
        self.filter_img_dir.mkdir(parents=True, exist_ok=True)

        if os.path.exists(self.full_img_dir):
            shutil.rmtree(self.full_img_dir)
            self.full_img_dir.mkdir(parents=True, exist_ok=True)
        else:
            self.full_img_dir.mkdir(parents=True, exist_ok=True)
        
        if os.path.exists(self.filter_img_dir):
            shutil.rmtree(self.filter_img_dir)
            self.filter_img_dir.mkdir(parents=True, exist_ok=True)
        else:
            self.filter_img_dir.mkdir(parents=True, exist_ok=True)




        # self.files_it = iter([os.path.join(img_dire, file) for file in os.listdir(img_dire)])
        # while True:
        #     try:
        #         file = next(self.files_it)
        #         pixmap = QtGui.QPixmap(file)
        #         self.add_pixmap(pixmap)
        #         lbl_img = QLabel()
            
        #         lbl_img.setPixmap(pixmap)
        #         lbl_img.setp
        #     except StopIteration:
        #         break
        

        self.vbox = QHBoxLayout()
        self.vbox2 = QHBoxLayout()

        self.viewData()

            
        # pixmap = QPixmap('C:\\Users\\XuhanLiu\\Desktop\\A4\\project1-team_34\\debug_img\\full\\100batch_size0.png')
        # pixmap1 = QPixmap('C:\\Users\\XuhanLiu\\Desktop\\A4\\project1-team_34\\debug_img\\full\\100batch_size1.png')
        # lbl_img = QLabel()
        # lbl_img1 = QLabel()
        # lbl_img.setPixmap(pixmap)
        # lbl_img1.setPixmap(pixmap1)

        # lbl_size = QLabel('Width: '+str(pixmap.width())+', Height: '+str(pixmap.height()))
        # lbl_size.setAlignment(Qt.AlignCenter)


        
        scrollArea = QScrollArea()
        
        scrollArea.setVerticalScrollBar
        groupBox = QGroupBox()
        


        # self.vbox.addWidget(lbl_img)
        # self.vbox.addWidget(lbl_img1) 
        groupBox.setLayout(self.vbox)
        # vbox.addWidget(lbl_size)
        scrollArea.setWidget(groupBox)
        self.vbox2.addWidget(scrollArea)
        self.setLayout(self.vbox2)
        # self.setWindowTitle('QPixmap')
        # self.move(300, 300)
        self.show()



    def viewData(self):
        batch_size = 50

        train_dataset = datasets.MNIST(root='mnist_data/',train=True,
        transform= transforms.Compose([transforms.ToTensor()]))
        
        test_dataset = datasets.MNIST(root='mnist_data/',train=False,
        transform= transforms.Compose([transforms.ToTensor()]),download=True)
        
        train_loader = data.DataLoader(dataset=train_dataset,
        batch_size=batch_size,shuffle=False)
        
        test_loader = data.DataLoader(dataset=test_dataset,
        batch_size=batch_size,shuffle=False)
        
        dataiter = iter(train_loader)

        print(train_loader.__sizeof__())
        

        
        i = 0

        while True:
            try:
                
                images, labels = dataiter.next() 
                npimg = images.numpy()
                self.nplb = labels.numpy()


                zero_filter = np.where(self.nplb == 0,)

                zeroimgs = images[zero_filter].numpy()
                k = zeroimgs.shape[0]



                #print(type(npimg))
                #print(npimg.shape)
                #plt.figure(figsize = (0.56,7))
                PIL_image = npimg.reshape(1400,28)
                filter_img = zeroimgs.reshape(28*k,28)

                filename = "{}batch_size{}.png".format(batch_size,i) 
                filterfilename = "{}filterImg{}.png".format(0,i) 
                results_dir = os.path.join(self.full_img_dir,filename)
                filter_dir = os.path.join(self.filter_img_dir,filterfilename)
                #plt.imshow(PIL_image, cmap='gray') 

                #plt.imsave(results_dir,PIL_image,cmap='gray')
                if not k==0:
                    plt.imsave(filter_dir,filter_img,cmap='gray')

                pixmap = QPixmap(results_dir)
                filterpixmap = QPixmap(filter_dir)

                lbl_img = QLabel()
                fil_img = QLabel()
                lbl_size = QLabel("{}".format(i))

                lbl_img.setPixmap(pixmap)
                fil_img.setPixmap(filterpixmap)

                lbl_size.setAlignment(Qt.AlignCenter)
                
                
                self.vbox.addWidget(lbl_img) 
                self.vbox.addWidget(lbl_size)



                #plt.savefig(results_dir)
                i = i+1

               
            except StopIteration:
                i =0
                break



        # npimg = images.numpy()
        
        # PIL_image = npimg.reshape(700,56)

        # plt.figure(figsize = (0.56,7))

        # filename = "40batch_size" + str(i)
        # results_dir = os.path.join(self.full_img_dir,filename)

    
        # plt.imshow(PIL_image, cmap='gray')
        # #plt.imsave('saved_figure.png',PIL_image,cmap='gray')
        # plt.savefig(results_dir +'40batch_size1.png')






if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()


    sys.exit(app.exec_())
