
from PyPDF2 import PdfFileReader,PdfMerger,PdfWriter,PageObject
import tkinter as tk
from tkinter.filedialog import askopenfilename,asksaveasfilename


paths=[]
pdfs=[]
def addFile(root):
    """Open a file for editing."""
    filepath =askopenfilename(
        filetypes=[("PDF Files", "*.pdf")]
    )
    if not filepath:
        return
    paths.append(filepath)
    pdfs.append(fileFrame(root,filepath))

def removePDF(pdf):
    paths.remove(pdf.path)
    pdfs.remove(pdf)
    pdf.frame.destroy()
def mergeFile():
    """Save the current file as a new file."""
    filepath = asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf"),("PDF Files", "*.PDF")],
    )
    if not filepath:
        return
    merger=PdfMerger()
    for path in paths:
        with open(path,'rb') as rfile:
            reader = PdfFileReader(rfile)
            merger.append(reader)
    with open(filepath,'wb') as mfile:
        merger.write(mfile)

    while(pdfs):
        removePDF(pdfs[0])


class mergeFrame():
    def __init__(self,root):
        self.frame=tk.Frame(root,relief=tk.RAISED,bd=2)
        self.buttonFrame=tk.Frame(self.frame)
        self.add=tk.Button(self.buttonFrame,text='Add file',command=lambda root=self:addFile(self))
        self.merge=tk.Button(self.buttonFrame,text='Merge',command=mergeFile)
        self.pdfFiles=tk.Frame(self.frame)

        self.frame.pack(fill='both', expand=True)
        self.buttonFrame.pack()
        self.add.pack(padx=5, pady=3, side='left')
        self.merge.pack(padx=5, pady=3, side='left')
        self.pdfFiles.pack(padx=5, pady=8)
    def terminate(self):
        while (pdfs):
            removePDF(pdfs[0])
        self.frame.destroy()



class fileFrame():
    def __init__(self,root,path):
        self.path=path
        self.frame=tk.Frame(root.pdfFiles,relief=tk.RAISED,bd=2)
        self.label=tk.Label(self.frame,text=path,width=90)
        self.remove=tk.Button(self.frame,text='Remove',command=lambda pdf=self:removePDF(pdf))

        self.frame.pack(fill='both',expand=True)
        self.label.grid(row=0,column=0,padx=5, pady=3)
        self.remove.grid(row=0, column=1, padx=5, pady=8)
