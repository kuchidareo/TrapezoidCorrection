import numpy as np
import cv2
import os,sys
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import threading
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
        original_path=original_path.replace(os.sep,"/")
        previous_path=original_path[:original_path.rfind("/")]
        previous_path=previous_path[:previous_path.rfind("/")]
        image_name=original_path[original_path.rfind("/")+1:]
        image_name=image_name[:image_name.rfind(".")]
        if not os.path.exists(previous_path+"/homography"):
            os.mkdir(previous_path+"/homography")

        original_img = cv2.imread(original_path)     
        size = original_img.shape[0] * original_img.shape[1]
        aimg = cv2.imread(original_path)     
        aimg[aimg[:,:,0]>200]= 0
        aimg[aimg[:,:,2]*0.8 < aimg[:,:,0]]= 0
        img = cv2.cvtColor(aimg, cv2.COLOR_BGR2HLS)
        img[img[:,:,0]<20]= 0
        img[80<img[:,:,0]]= 0
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        contours, hierarchy = cv2.findContours(gray, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        max_area = 10000000
        approxs = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            epsilon = 0.1 * cv2.arcLength(cnt, True)
            tmp = cv2.approxPolyDP(cnt, epsilon, True)
            if 4 == len(tmp):
                approxs.append(tmp)
                if size * 0.005 <= area\
                    and area <= size * 0.99\
                    and max_area > area:
                    best_approx = tmp
                    max_area = area
        l_top = best_approx[0][0] 
        l_btm = best_approx[1][0]
        r_btm = best_approx[2][0]
        r_top = best_approx[3][0]
        l_top_total = l_top[0] + l_top[1]
        l_btm_total = l_btm[0] + l_btm[1]
        r_btm_total = r_btm[0] + r_btm[1]
        r_top_total = r_top[0] + r_top[1]
        if min(l_top_total,l_btm_total,r_btm_total,r_top_total) == l_btm_total:
            l_top = best_approx[1][0]
            l_btm = best_approx[0][0]
        elif min(l_top_total,l_btm_total,r_btm_total,r_top_total) == r_btm_total:
            l_top = best_approx[2][0]
            r_btm = best_approx[0][0]
        elif min(l_top_total,l_btm_total,r_btm_total,r_top_total) == r_top_total:
            l_top = best_approx[3][0]
            r_top = best_approx[0][0]

        if max(l_top_total,l_btm_total,r_btm_total,r_top_total) == l_btm_total:
            r_btm = best_approx[1][0]
            l_btm = best_approx[2][0]
        elif max(l_top_total,l_btm_total,r_btm_total,r_top_total) == r_top_total:
            r_btm = best_approx[3][0]
            r_top = best_approx[2][0]
        
        if abs((l_top[0] - l_btm[0]) ^ 2) > abs((l_top[1] - l_btm[1]) ^ 2):
            l_btm = best_approx[3][0]
            r_top = best_approx[1][0]

        btm_line   = (abs(l_btm[0] - r_btm[0]) ^ 2) + (abs(l_btm[1] - r_btm[1]) ^ 2)
        top_line   = (abs(l_top[0] - r_top[0]) ^ 2) + (abs(l_top[1] - r_top[1]) ^ 2)
        right_line  = (abs(r_btm[0] - r_top[0]) ^ 2) + (abs(r_btm[1] - r_top[1]) ^ 2)
        left_line = (abs(l_btm[0] - l_top[0]) ^ 2) + (abs(l_btm[1] - l_top[1]) ^ 2)
        max_x = btm_line  if btm_line  > top_line   else top_line
        max_y = right_line if right_line > left_line else left_line

        pts1 = np.float32([[l_top[0],l_top[1]],[l_btm[0],l_btm[1]],[r_btm[0],r_btm[1]],[r_top[0],r_top[1]]])
        pts2 = np.float32([[0,0], [0, max_y], [max_x, max_y], [max_x,0]])

        M = cv2.getPerspectiveTransform(pts1, pts2)
        dst = cv2.warpPerspective(original_img, M, (max_x, max_y))
        dst = dst.transpose(1,0,2)
        dst = dst[:,::-1]
        dst = cv2.rotate(dst, cv2.ROTATE_180)
        width,height =2150,1720
        dst = cv2.resize(dst,(width,height))
        cv2.imwrite(previous_path+"/homography/"+image_name+"_corrected.jpg", dst)
        i+=1
        q.set(str(i)+"/"+str(len(original_paths)))
        del original_img,dst,img,gray,M,area,aimg
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


if __name__ == '__main__':
    # rootの作成
    root = Tk()
    root.title('TrapezoidCorrection')
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