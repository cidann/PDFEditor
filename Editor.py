import tkinter as tk
import Merge,moveDelete

def toMerge(editor):
    editor.current.terminate()
    editor.current=Merge.MergeFrame(editor.root)
def toMoveDelete(editor):
    editor.current.terminate()
    editor.current=moveDelete.MoveDeleteFrame(editor.root)
window = tk.Tk()
window.title("PDF Editor")
window.geometry('800x600')

window.rowconfigure(1)
window.columnconfigure(1,minsize=300)

class pdfEditor():
    def __init__(self,root):
        self.root=root
        self.pdf_toolbar = tk.Frame(root, relief=tk.RAISED, bd=2)
        self.mergeButton = tk.Button(self.pdf_toolbar, text='Merge', command=lambda editor=self:toMerge(self))
        self.moveDeleteButton = tk.Button(self.pdf_toolbar, text='Move/Delete', command=lambda editor=self:toMoveDelete(self))

        self.pdf_toolbar.pack(fill='x')
        self.mergeButton.grid(row=0, column=0, padx=5, pady=3)
        self.moveDeleteButton.grid(row=0, column=1, padx=5, pady=3)

        self.current=Merge.MergeFrame(window)

editor=pdfEditor(window)
window.mainloop()
