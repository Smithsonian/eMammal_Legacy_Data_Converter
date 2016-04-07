
from Tkinter import *
import tkFileDialog
from ttk import Frame, Button, Style, Label, Entry
import subprocess
import os

# python create_manifest.py input_dir output_dir type
# python create_manifest.py input_dir output_dir type

class MainFrame(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def quit(self):
        self.parent.destroy()

    def input_askdirectory(self):
        select_dir = tkFileDialog.askdirectory()
        self.root_directory.set(select_dir)
        return select_dir

    def output_askdirectory(self):
        select_dir = tkFileDialog.askdirectory()
        self.output_directory.set(select_dir)
        return select_dir

    def get_type_value(self):
        return self.radio_type

    def run_process(self):
        if self.radio_type == 0:
            print 'wcs_validator_type'
        else:
            print 'emammal_validator_type'
        # print 'self.radio_type', self.radio_type, type(self.radio_type)
        # print 'self.root_directory', self.root_directory, type(self.root_directory)
        # print 'self.output_directory',self.output_directory,type(self.output_directory)

        create_manifest = os.path.join(os.path.dirname(os.path.realpath(__file__)),'create_manifest.py')
        proc = subprocess.Popen(["python", create_manifest,self.root_directory.get(), self.output_directory.get(), str(self.radio_type)])
        proc.wait()
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'error.log')) as f:
            content = f.readlines()
            for i in content:
                self.results.insert(END,i)


    def update_type_value(self):
        if self.radio_type == 0:
            self.radio_type = 1
            self.radio_type = 1
        else:
            self.radio_type = 0


    def initUI(self):

        self.parent.title("Emammal Legacy Data Converter")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=True)

        self.root_directory = StringVar(self.parent)
        self.output_directory = StringVar(self.parent)
        self.results = StringVar()
        self.radio_type = IntVar()
        self.radio_type = 0

        frame1 = Frame(self)
        frame1.pack(fill=X)

        lbl1 = Label(frame1, text="Input Directory", width=15)
        lbl1.pack(side=LEFT, padx=5, pady=5)

        select_dir = Button(frame1, text='Choose Directory', command=self.input_askdirectory)
        select_dir.pack(side=LEFT, padx=5, pady=5)

        entry1 = Entry(frame1,textvariable= self.root_directory)
        entry1.pack(fill=X, padx=5, expand=True)

        frame2 = Frame(self)
        frame2.pack(fill=X)

        lbl2 = Label(frame2, text="Output Directory", width=15)
        lbl2.pack(side=LEFT, padx=5, pady=5)

        output_dir = Button(frame2, text='Choose Directory', command=self.output_askdirectory)
        output_dir.pack(side=LEFT, padx=5, pady=5)

        entry2 = Entry(frame2, textvariable= self.output_directory)
        entry2.pack(fill=X, padx=5, expand=True)

        frameRadio = Frame(self)
        frameRadio.pack(fill=X)

        lbl2 = Label(frameRadio, text="Manifest Type", width=15)
        lbl2.pack(side=LEFT, padx=5, pady=5)

        radio_emammal = Radiobutton(frameRadio, text="Emmamal", variable=self.radio_type, value=1,command=self.update_type_value)
        radio_emammal.pack(side=LEFT, padx=5, pady=5)

        radio_classic = Radiobutton(frameRadio, text="Classic", variable=self.radio_type,value=0,command=self.update_type_value)
        radio_classic.pack(side=LEFT, padx=5, pady=5)

        radio_classic.select()

        frame3 = Frame(self)
        frame3.pack(fill=BOTH, expand=True)

        lbl3 = Label(frame3, text="Results", width=15)
        lbl3.pack(side=LEFT, anchor=N, padx=5, pady=5)

        self.results = Text(frame3)
        self.results.pack(fill=BOTH, pady=5, padx=5, expand=True)

        closeButton = Button(self, text="Close",command=self.quit)
        closeButton.pack(side=RIGHT, padx=5, pady=5)

        okButton = Button(self, text="Run",command=self.run_process)
        okButton.pack(side=RIGHT)


def main():

    root = Tk()
    root.geometry("600x600")
    app = MainFrame(root)
    root.mainloop()

if __name__ == '__main__':
    main()