from PyPDF2 import PdfFileReader,PdfMerger,PdfWriter,PageObject
import tkinter as tk
from tkinter.filedialog import askopenfilename,asksaveasfilename

def chooseFile(root):
    filepath = askopenfilename(
        filetypes=[("PDF Files", "*.pdf"),("PDF Files", "*.PDF")]
    )
    if not filepath:
        return
    root.pdfFile.label['text']=filepath

def movePagesFunc(inputs,file):
    filePath=file.getPath()
    pagesToMoveInput=inputs.movePages.get().split(',')
    destination=inputs.toPage.get().strip()
    if(not destination.isdigit()):
        return
    try:
        reader=PdfFileReader(filePath)
        allPages=reader.pages
        pagesToMove=[]
        resultPages=[]
        pagesRecorded={}
        for input in pagesToMoveInput:
            input=input.split('-')
            if(len(input)==1 and input[0].strip().isdigit()):
                index=int(input[0].strip())-1
                if(not pagesRecorded.get(index)):
                    pagesToMove.append(allPages[index])
                    pagesRecorded[index]=True
            elif(len(input)==2 and input[0].strip().isdigit() and input[1].strip().isdigit()):
                start=int(input[0].strip())-1
                end=int(input[1].strip())
                for pageNum in range(start,end):
                    if(not pagesRecorded.get(pageNum)):
                        pagesToMove.append(allPages[pageNum])
                        pagesRecorded[pageNum] = True
        for pageNum in range(len(allPages)):
            if(not pagesRecorded.get(pageNum)):
                resultPages.append(allPages[pageNum])
        resultPages[int(destination)-1:int(destination)-1]=pagesToMove
        writer=PdfWriter()
        for page in resultPages:
            writer.add_page(page)
        with open(filePath,'wb') as outputFile:
            writer.write(outputFile)
        inputs.status['text'] = 'Success'
        inputs.status['fg'] = 'green'
    except:
        inputs.status['text'] = 'Failed'
        inputs.status['fg'] = 'red'

def deletePagesFunc(inputs,file):
    filePath = file.getPath()
    pagesToDelete = inputs.deletePages.get().split(',')
    try:
        reader=PdfFileReader(filePath)
        allPages=reader.pages
        pagesRecorded={}
        for input in pagesToDelete:
            input=input.split('-')
            if (len(input) == 1 and input[0].strip().isdigit()):
                index = int(input[0].strip()) - 1
                pagesRecorded[index]=True
            elif (len(input) == 2 and input[0].strip().isdigit() and input[1].strip().isdigit()):
                start = int(input[0].strip()) - 1
                end = int(input[1].strip())
                for pageNum in range(start, end):
                    pagesRecorded[pageNum] = True
        writer=PdfWriter()
        for i in range(len(allPages)):
            if(not pagesRecorded.get(i)):
                writer.add_page(allPages[i])
        with open(filePath,'wb') as outputFile:
            writer.write(outputFile)
        inputs.status['text']='Success'
        inputs.status['fg'] = 'green'
    except:
        inputs.status['text'] = 'Failed'
        inputs.status['fg'] = 'red'

class MoveDeleteFrame():
    def __init__(self, root):
        self.root=root
        self.frame = tk.Frame(root, relief=tk.RAISED, bd=2)
        self.buttonFrame = tk.Frame(self.frame)
        self.choose = tk.Button(self.buttonFrame, text='Choose file', command=lambda root=self: chooseFile(root))

        self.frame.pack(fill='both', expand=True)
        self.buttonFrame.pack()
        self.choose.pack(padx=5, pady=3, side='left')

        self.pdfFile = FileFrame(self)
        self.Input=InputFrame(self)


    def terminate(self):
        self.frame.destroy()


class FileFrame():
    def __init__(self,root):
        self.frame=tk.Frame(root.frame,relief=tk.RAISED,bd=2)
        self.label=tk.Label(self.frame,text='',width=60)

        self.frame.pack()
        self.label.grid(row=0,column=0,padx=5, pady=3)
    def getPath(self):
        return self.label['text']

class InputFrame:
    def __init__(self,root):
        self.root=root
        self.frame = tk.Frame(root.frame, relief=tk.RAISED, bd=2)

        self.frame.pack()


        self.moveLabel = tk.Label(self.frame, text='Move', width=60)
        self.moveInputs = tk.Frame(self.frame, relief=tk.RAISED, bd=4)
        self.move = tk.Label(self.moveInputs, text='Pages (E.g. 1, 3-5, 7)')
        self.movePages = tk.Entry(self.moveInputs)
        self.to=tk.Label(self.moveInputs, text='to')
        self.toPage=tk.Entry(self.moveInputs)
        self.moveButton=tk.Button(
            self.moveInputs,
            text='Move',command=lambda inputs=self,file=root.pdfFile:movePagesFunc(inputs,file)
        )

        self.moveLabel.grid(row=0, column=0, padx=5, pady=3)
        self.moveInputs.grid(row=1, column=0, padx=5, pady=3,sticky='w')
        self.move.grid(row=0, column=0, padx=5, pady=3)
        self.movePages.grid(row=0,column=1, padx=5, pady=3)
        self.to.grid(row=0,column=2, padx=5, pady=3)
        self.toPage.grid(row=0, column=3, padx=5, pady=3)
        self.moveButton.grid(row=0, column=4, padx=5, pady=3)


        self.deleteLabel=tk.Label(self.frame, text='Delete', width=60)
        self.deleteInputs = tk.Frame(self.frame, relief=tk.RAISED, bd=4)
        self.delete = tk.Label(self.deleteInputs, text='Pages (E.g. 1, 3-5, 7)')
        self.deletePages = tk.Entry(self.deleteInputs)
        self.deleteButton = tk.Button(
            self.deleteInputs,
            text='Delete',
            command=lambda inputs=self, file=root.pdfFile: deletePagesFunc(inputs, file)
        )

        self.deleteLabel.grid(row=3, column=0, padx=5, pady=3)
        self.deleteInputs.grid(row=4, column=0, padx=5, pady=3,sticky='w')
        self.delete.grid(row=0, column=0, padx=5, pady=3)
        self.deletePages.grid(row=0, column=1, padx=5, pady=3)
        self.deleteButton.grid(row=0,column=2, padx=5, pady=3)

        self.status=tk.Label(self.frame,text='')

        self.status.grid(row=5, column=0, padx=5, pady=3)
