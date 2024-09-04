from tkinter import *
import subprocess

cor_page= '#9E9E9E'
cor_f_list= '#FFFFFF'
cor_button= '#4CAF50'
cor_fg_button= '#FFFFFF'



class Mainpage():
    def __init__(self, master):
        self.master = master
        self.Setup()
    
    def Setup(self):
        self.l_title = Label(self.master, text='Controle de validade', font='temple 22 bold', relief='flat', bg=cor_page, fg='white')
        self.l_title.place(x=90, y=10)

        self.btn_cadastro = Button(self.master, text='Cadastrar', command=self.Open_cadastro,font='temple 22 bold', relief='groove', bg=cor_button, fg=cor_fg_button, width=20, height=1)
        self.btn_delete =  Button(self.master, text='deletar', font='temple 22 bold', relief='groove', bg=cor_button, fg=cor_fg_button, width=20, height=1, command=self.Open_delete)
        self.btn_list =  Button(self.master, text='listagem', font='temple 22 bold', relief='groove', bg=cor_button, fg=cor_fg_button, width=20, height=1, command=self.Open_list)

        self.btn_cadastro.place(x=60, y=100)
        self.btn_delete.place(x=60, y=180)
        self.btn_list.place(x=60, y=260)

    
    def Open_cadastro(self):
        p = subprocess.Popen("python cadastro.py", 
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True)
        
    def Open_delete(self):
        p = subprocess.Popen("python delete.py", 
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True)
        
    def Open_list(self):
        p = subprocess.Popen("python list.py", 
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True)



if __name__ == '__main__':
    root = Tk()
    root.geometry('500x400')
    root.configure(bg=cor_page)
    root.title('Pagina principal')
    root.resizable(width=False, height=False)

    app = Mainpage(root)

    root.mainloop()
        