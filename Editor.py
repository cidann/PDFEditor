from PyPDF2 import PdfFileReader,PdfMerger,PdfWriter,PageObject
import tkinter as tk
from tkinter.filedialog import askopenfilename,asksaveasfilename

window = tk.Tk()
window.title("PDF Editor")
window.geometry('800x600')

window.rowconfigure(1)
window.columnconfigure(1,minsize=300)

paths=[]
pdfs=[]
def addFile():
    """Open a file for editing."""
    filepath =askopenfilename(
        filetypes=[("PDF Files", "*.pdf")]
    )
    if not filepath:
        return
    paths.append(filepath)
    pdfs.append(fileFrame(filepath))

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
class mergeFrame():
    def __init__(self):
        self.frame=tk.Frame(window,relief=tk.RAISED,bd=2)
        self.buttonFrame=tk.Frame(self.frame)
        self.add=tk.Button(self.buttonFrame,text='Add file',command=addFile)
        self.merge=tk.Button(self.buttonFrame,text='Merge',command=mergeFile)
        self.pdfFiles=tk.Frame(self.frame)

        self.frame.pack(fill='both', expand=True)
        self.buttonFrame.pack()
        self.add.pack(padx=5, pady=3, side='left')
        self.merge.pack(padx=5, pady=3, side='left')
        self.pdfFiles.pack(padx=5, pady=8)


class fileFrame():
    def __init__(self,path):
        self.path=path
        self.frame=tk.Frame(a.pdfFiles,relief=tk.RAISED,bd=2)
        self.label=tk.Label(self.frame,text=path)
        self.remove=tk.Button(self.frame,text='Remove',command=lambda pdf=self:removePDF(pdf))

        self.frame.pack(fill='both',expand=True)
        self.label.grid(row=0,column=0,padx=5, pady=3)
        self.remove.grid(row=0, column=1, padx=5, pady=8)




pdf_toolbar=tk.Frame(window,relief=tk.RAISED,bd=2)
mergeButton=tk.Button(pdf_toolbar,text='Merge',)
moveDeleteButton=tk.Button(pdf_toolbar,text='Move/Delete')

pdf_toolbar.pack(fill='x')
mergeButton.grid(row=0,column=0,padx=5, pady=3)
moveDeleteButton.grid(row=0,column=1,padx=5, pady=3)

a=mergeFrame()


window.mainloop()