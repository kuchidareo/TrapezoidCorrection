import numpy as np
import cv2
import os,sys
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import threading
import re
import pathlib
import itertools

def analyze():
    def finished():
        q.set("")
        button2.config(state="active")
        messagebox.showinfo("ImageAnalysis", "終了しました")
    q.set("Converting...")
    i=0
    for original_path in original_paths:
        original_img= cv2.imread(original_path,1)
        original_img = original_img / 255
        imgBox = original_img[L[0]: L[1],L[2]: L[3]]
        b = imgBox[:,:,0].flatten().mean()
        g = imgBox[:,:,1].flatten().mean()
        r = imgBox[:,:,2].flatten().mean()
        original_img[:, :, 0] = 100 / 255 * (original_img[:, :, 0] / b)
        original_img[:, :, 1] = 100 / 255 * (original_img[:, :, 1] / g)
        original_img[:, :, 2] = 170 / 255 * (original_img[:, :, 2] / r)
        original_img[original_img > 1] = 1
        z = original_img / base_img
        z[z>1] = 1
        z = z * 255

        #path設定
        original_path=original_path.replace(os.sep,"/")
        previous_path=original_path[:original_path.rfind("/")]
        previous_path=previous_path[:previous_path.rfind("/")]
        image_name=original_path[original_path.rfind("/")+1:]
        image_name=image_name[:image_name.rfind(".")]
        if not os.path.exists(previous_path+"/homography"):
            os.mkdir(previous_path+"/homography")

        
        dst = []

        '''pts1 = np.float32([[1227,999],[367,1802],[3932,1810],[3056,999]])
        pts2 = np.float32([[595,431],[582,1458],[1632,1450],[1635,436]])
        M = cv2.getPerspectiveTransform(pts1,pts2)'''
        dst = cv2.warpPerspective(z,M,(N[0],N[1]))
        dst = dst.transpose(1,0,2)
        dst = dst[::-1]
        cv2.imwrite(previous_path+"/homography/"+image_name+"_homography.jpg", dst)
        i+=1
        q.set(str(i)+"/"+str(len(original_paths)))
        del original_img,dst,z,imgBox
    finished()

def callback():
    button2.config(state="disable")
    th = threading.Thread(target=analyze)
    th.start()

def sansyou1_clicked():
    iDir = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Desktop"
    global filepath1
    global original_paths
    original_paths=[]
    filepath1 = filedialog.askdirectory(initialdir = iDir)
    path = pathlib.Path(filepath1)
    for file_or_dir in path.iterdir():
        original_paths.append(str(file_or_dir))
    file1.set(filepath1)


def sansyou2_clicked():
    fTyp = [("","*.jpg")]
    iDir = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Desktop"
    global filepath2
    global base_img
    filepath2 = filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
    base_img=cv2.imread(filepath2,1)
    base_img = base_img / 255
    file2.set(filepath2)

def sansyou3_clicked():
    fTyp = [("","*.csv")]
    iDir = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Desktop"
    global filepath3
    global M
    global N
    global L
    filepath3 = filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
    file3.set(filepath3)
    M = np.genfromtxt(fname=filepath3,delimiter=",",dtype = None)
    M = list(itertools.chain.from_iterable(M))
    print(M)
    N = [int(M[9]),int(M[10])]
    L = [int(M[11]),int(M[12]),int(M[13]),int(M[14])]
    M = np.array([[M[0],M[1],M[2]], [M[3],M[4],M[5]], [M[6],M[7],M[8]]])
if __name__ == '__main__':
    # rootの作成
    root = Tk()
    root.title('Image Analysis')
    root.resizable(False, False)

    # Frame1
    frame1 = ttk.Frame(root, padding=20)
    frame1.grid(row=0)
    s1 = StringVar()
    s1.set('MIJ camera FOLDER')
    label1 = ttk.Label(frame1, textvariable=s1)
    label1.grid(row=0, column=0,sticky=W)

    file1 = StringVar()
    file1_entry = ttk.Entry(frame1, textvariable=file1, width=50)
    file1_entry.grid(row=0, column=1,padx=20)

    button1 = ttk.Button(frame1, text=u'OPEN', command=sansyou1_clicked)
    button1.grid(row=0, column=2)

    s2 = StringVar()
    s2.set('Gray Board FILE')
    label2 = ttk.Label(frame1, textvariable=s2)
    label2.grid(row=1, column=0,sticky=W)

    file2 = StringVar()
    file2_entry = ttk.Entry(frame1, textvariable=file2, width=50)
    file2_entry.grid(row=1, column=1)

    button2 = ttk.Button(frame1, text=u'OPEN', command=sansyou2_clicked)
    button2.grid(row=1, column=2)

    s3 = StringVar()
    s3.set('Conversion Matrix FILE')
    label3 = ttk.Label(frame1, textvariable=s3)
    label3.grid(row=2, column=0,sticky=W)

    file3 = StringVar()
    file3_entry = ttk.Entry(frame1, textvariable=file3, width=50)
    file3_entry.grid(row=2, column=1)

    button3 = ttk.Button(frame1, text=u'OPEN', command=sansyou3_clicked)
    button3.grid(row=2, column=2)

    # Frame3 startボタン
    frame3 = ttk.Frame(root, padding=(0,0,0,10))
    frame3.grid(row=1)
    button2 = ttk.Button(frame3, text='Start', command=callback)
    button2.pack()

    global q
    q= StringVar()
    q.set("")
    progress_entry = ttk.Entry(frame3, textvariable=q, width=20)
    progress_entry.pack(pady=10)
    
    root.mainloop()