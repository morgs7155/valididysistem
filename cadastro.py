from tkinter import *
from tkinter import messagebox
from tkcalendar import  DateEntry
from datetime import datetime
import sqlite3

#variavels
ano_atual = datetime.now().year

#####CORES#####
cor_root = '#FFCDD2'
cor_f = '#B31E1E'
cor_fg_f = '#F7F5F5'
cor_btn = '#D8D8D8'
cor_fg_buton = 'black'
###############

class Main_page():
    def __init__(self, master):
        self.master = master
        self.Setup()

    def Setup(self):
        #FRAMES
        self.f_center = Frame(self.master, width=400, height=300, bg=cor_f)
        self.f_center.place(x=50, y=100)
        
        #LABELS
        self.l_title = Label(self.master, text='CADASTRO DE PRODUTOS', font='impact 22 bold', relief='flat', bg=cor_root, fg=cor_f)
        self.l_title.place(x=100, y=50)

        self.l_product = Label(self.f_center, text='produto:', font='temple 12 bold', relief='flat', bg=cor_f, fg=cor_fg_f)
        self.l_product.place(x=10, y=50)

        self.l_valididy = Label(self.f_center, text='validade:', font='temple 12 bold', relief='flat', bg=cor_f, fg=cor_fg_f)
        self.l_valididy.place(x=10, y=100)

        #ENTRYS
        self.e_product = Entry(self.f_center, width=40, bg='white', relief='groove')
        self.e_product.place(x=90, y=52)

        #BUTTONS
        
        self.calendario = DateEntry(self.f_center,  width=12,  background='darkblue', foreground='white',  borderwidth=2, year=ano_atual)
        self.calendario.place(x=100, y=100)
        self.calendario.bind("<<DateEntrySelected>>", self.Select_date)

        self.b_salvad = Button(self.f_center, text='SALVAR', command=self.Saved, font='Fixedsys 12 bold', relief='groove', fg=cor_fg_buton, bg=cor_btn, width=10, height=2)
        self.b_salvad.place(x=150, y=250)





        #################
        #config datetime#
    def Select_date(self, event=None):
        try:
            self.name = self.e_product.get()
            selected_date = self.calendario.get_date()

            global data_de_vencimento
            data_de_vencimento = datetime(day=selected_date.day, month=selected_date.month, year=selected_date.year)

            # Formatando a data para o formato "dd/mm/yyyy"
            self.format_date = data_de_vencimento.strftime("%d/%m/%Y")

            # Exibindo a data formatada em um label
            self.l_date_valididy = Label(self.f_center, text='data de validade: ' + self.format_date, font='temple 12 bold', relief='flat', bg=cor_f, fg=cor_fg_f)
            self.l_date_valididy.place(x=10, y=130)

            messagebox.showinfo("Atenção", "data " + self.format_date +  " selecionada com sucesso")

        except:
            messagebox.showerror("Atenção", "erro:" + ValueError)

    def Saved(self):
        try:
            conn = sqlite3.connect('database/stock.db')
            cursor = conn.cursor()
            #status seria a data de validade
            cursor.execute("INSERT INTO products(name, validity) VALUES(?, ?)", (self.name, self.format_date))
            conn.commit()
            conn.close()

            messagebox.showinfo("Atenção", "Produto cadastrado com sucesso")

        except:
            messagebox.showerror("Atenção", "Erro ao cadastrar produto:" + ValueError)

        


#CONFIGURAÇÕES DE JANELA
if __name__ == '__main__':
    root = Tk()
    root.geometry('500x500')
    root.configure(bg= cor_root )
    root.title('Cadastro de produtos')
    root.resizable(width=False, height=False)

    app = Main_page(root)

    root.mainloop()