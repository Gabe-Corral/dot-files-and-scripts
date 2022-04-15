import sys
import os
import tkinter as tk
from PIL import Image, ImageTk
from itertools import count

class ImageViewer:

    def __init__(self, image_path):
        self.root = tk.Tk()
        self.root.wm_title(image_path)
        self.img_path = image_path


    def load_gif(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.canvas_gif.create_image(0, 0, anchor=tk.NW, image=self.frames[0])
        else:
            self.next_frame()
            

    def unload(self):
        self.canvas_gif.create_image(0, 0, anchor=tk.NW, image="")
        self.frames = None
        

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.canvas_gif.create_image(0, 0, anchor=tk.NW, image=self.frames[self.loc])
            self.root.after(self.delay, self.next_frame)


    def resize_image(self, event):
        image = self.image_copy.resize((self.root.winfo_width(),self.root.winfo_height()))
        self.image1 = ImageTk.PhotoImage(image)
        self.cur_img.config(image = self.image1)


    def load_image(self):
        image = Image.open(self.img_path)
        self.image_copy = image.copy()
        photo = ImageTk.PhotoImage(image)
        self.cur_img = tk.Label(self.root, image = photo)
        self.cur_img.bind('<Configure>', self.resize_image)
        self.cur_img.pack(fill=tk.BOTH, expand=tk.YES)


    def set_res(self, gif=False):
        image = Image.open(self.img_path)
        width, height = image.size
        self.root.geometry(f"{width}x{height}")
        if gif:
            self.canvas_gif = tk.Canvas(self.root, width=width, height=height, highlightthickness=0)
            self.canvas_gif.pack()


    def check_file_type(self):
        file = os.path.splitext(self.img_path)
        if file[1] == '.jpg' or file[1] == '.jpeg' or file[1] == '.png':
            self.load_image()
        elif file[1] == '.gif':
            self.set_res(gif=True)
            self.load_gif(self.img_path)
        else:
            print("ERROR: File type not supported.")


    def main(self):
        self.set_res()
        self.check_file_type()
        self.root.mainloop()


if __name__=="__main__":
    ImageViewer(sys.argv[1]).main()
    
