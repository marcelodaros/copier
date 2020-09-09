from tkinter import *
import tkinter.ttk as ttk
from PIL import ImageTk, Image


class CopierGui:

    def __init__(self, master):
        self.master = master
        self.master.title("Copier v0.1a")
        self.master.geometry("500x460+200+200")
        self.master.iconbitmap("copier_icon.ico")
        self.master.resizable(0, 0)

        # Top
        top_frame = Frame(self.master, bg="#333333")
        top_frame.pack(fill=X)
        logo_frame = Frame(top_frame, bg="#333333")
        self.logo = ImageTk.PhotoImage(Image.open("copier_logo.png"))
        self.logo_l = Label(logo_frame, image=self.logo, bg="#333333")
        self.logo_l.grid()
        logo_frame.pack(side=LEFT, fill=X, padx=5, pady=5)
        name_frame = Frame(top_frame, bg="#333333")
        self.name = Label(name_frame, text="Copier", font="Verdana 25 bold", bg="#333333", fg="#ffffff")
        self.name.grid(row=0, column=0, sticky=S+E)
        self.version = Label(name_frame, text="v0.1a", font="Verdana 10 bold", bg="#333333", fg="#ffffff")
        self.version.grid(row=1, column=0, sticky=N+E)
        name_frame.pack(side=RIGHT, fill=X, padx=5, pady=5)

        # Middle
        mid_frame = Frame(self.master)
        mid_frame.pack()

        mid_frame_top = Frame(mid_frame)
        mid_frame_top.pack(side=TOP)
        self.source_label = ttk.Label(mid_frame_top, text="Source Folder", font="Verdana 10 bold")
        self.source_label.grid(row=0, column=0, columnspan=2, pady=5)
        self.source_entry = ttk.Entry(mid_frame_top, text="Source Folder", font="Verdana 10 bold", width=35)
        self.source_entry.grid(row=1, column=1)
        self.btn_source = ttk.Button(mid_frame_top, text="Browse", width=15)
        self.btn_source.grid(row=1, column=0)
        self.dest_label = ttk.Label(mid_frame_top, text="Destination Folder", font="Verdana 10 bold")
        self.dest_label.grid(row=2, column=0, columnspan=2, pady=5)
        self.dest_entry = ttk.Entry(mid_frame_top, text="Destination Folder", font="Verdana 10 bold", width=35)
        self.dest_entry.grid(row=3, column=1)
        self.btn_source = ttk.Button(mid_frame_top, text="Browse", width=15)
        self.btn_source.grid(row=3, column=0)

        mid_frame_bottom = Frame(mid_frame)
        mid_frame_bottom.pack(pady=10)
        self.folder_label = ttk.Label(mid_frame_bottom, text="Folders Actions", font="Verdana 10 bold")
        self.folder_label.grid(row=0, column=0, columnspan=2, stick=W, pady=5)
        self.btn_copy = ttk.Button(mid_frame_bottom, text="Copy Folder", width=15, command=self.start_bar)
        self.btn_copy.grid(row=1, column=0, columnspan=2, stick=W, pady=5)
        self.btn_verify = ttk.Button(mid_frame_bottom, text="Verify Folders", width=15)
        self.btn_verify.grid(row=2, column=0, columnspan=2, stick=W, pady=5)

        self.folder_label = ttk.Label(mid_frame_bottom, text="MHL Actions", font="Verdana 10 bold")
        self.folder_label.grid(row=0, column=4, columnspan=2, padx=50, pady=5)
        self.btn_copy = ttk.Button(mid_frame_bottom, text="Generate MHL", width=15)
        self.btn_copy.grid(row=1, column=4, columnspan=2, padx=85, pady=5)

        self.h = IntVar()

        self.folder_label = ttk.Label(mid_frame_bottom, text="Hash Mode", font="Verdana 10 bold")
        self.folder_label.grid(row=0, column=6, columnspan=2, stick=E)
        self.btn_copy = ttk.Radiobutton(mid_frame_bottom, text="MD5", variable=self.h, value=1, command=self.selected)
        self.btn_copy.grid(row=1, column=6, columnspan=2, stick=E)
        self.btn_copy = ttk.Radiobutton(mid_frame_bottom, text="xxHash64", variable=self.h, value=2, command=self.selected)
        self.btn_copy.grid(row=2, column=6, columnspan=2, stick=NE)

        bottom_frame = Frame(mid_frame)
        bottom_frame.pack(side=BOTTOM)
        self.progress_bar = ttk.Progressbar(bottom_frame, length=450)
        self.progress_bar.grid(row=0, pady=10)
        self.status = ttk.Label(bottom_frame, text="Olá", font="Verdana 8 bold")
        self.status.grid(row=1, pady=10)

    def selected(self):
        text = "None Selected"
        if self.h.get() == 1:
            text = "MD5 Selected"
        elif self.h.get() == 2:
            text = "xxHash64 Selected"

        self.status.config(text=text)

    def start_bar(self):
        self.progress_bar.start()


root = Tk()
copier_gui = CopierGui(root)
root.mainloop()
