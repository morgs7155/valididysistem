from tkinter import *
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk

#####CORES#####
cor_root = '#FFCDD2'
cor_f = '#B31E1E'
cor_fg_f = '#F7F5F5'
cor_btn = '#D8D8D8'
cor_fg_buton = 'black'
new_cor = '#000000'
cor_f_list= '#FFFFFF'
###############

class Main_page():
    def __init__(self, master):
        self.master = master
        self.Setup()

    def Setup(self):
        # Configuração das labels
        self.l_title = Label(self.master, text='Deletar Produto', font='Fixedsys 22 bold', bg=cor_root, fg=cor_fg_f)
        self.l_id = Label(self.master, text='Digite o ID:', font='temple 12 bold', bg=cor_root, fg=new_cor)
        
        # Configuração das entrys
        self.e_id = Entry(self.master, font='temple 12 bold', relief='groove', width=15)
        
        # Botões
        self.btn_confirm_id = Button(self.master, text='SEARCH', font='temple 12 bold', bg=cor_btn, fg=cor_fg_buton, command=self.Search)

        # Posicionamento dos widgets
        self.l_title.place(x=110, y=10)
        self.l_id.place(x=10, y=100)
        self.e_id.place(x=98, y=100)
        self.btn_confirm_id.place(x=250, y=95)

    def Search(self):
        product_id = self.e_id.get()
        if product_id:
            conn = sqlite3.connect('database/stock.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, validity FROM products WHERE id=?", (product_id,))
            product = cursor.fetchone()
            conn.close()

            if product:
                self.Display_product(product)
            else:
                messagebox.showerror("Erro", "ID não encontrado.")
        else:
            messagebox.showwarning("Atenção", "Por favor, insira um ID.")

    def Display_product(self, product):
        #Remover o frame anterior
        if hasattr(self, 'frame_list'):
            self.frame_list.destroy()

        self.frame_list = Frame(self.master, bg=cor_f_list)
        self.frame_list.place(x=10, y=150, width=480, height=300)

        #Exibir informações do produto
        Label(self.frame_list, text=f"ID: {product[0]}", bg=cor_f_list).grid(row=0, column=0, padx=20, pady=5)
        Label(self.frame_list, text=f"Nome: {product[1]}", bg=cor_f_list).grid(row=0, column=1, padx=30, pady=5)
        Label(self.frame_list, text=f"Validade: {product[2]}", bg=cor_f_list).grid(row=0, column=2, padx=50, pady=5)

        #Carregar e adicionar ícone de lixeira
        trash_icon = Image.open("icons/Bin-1--Streamline-Ultimate.png")
        trash_icon = trash_icon.resize((30, 30), Image.LANCZOS)
        trash_img = ImageTk.PhotoImage(trash_icon)

        delete_button = Button(self.frame_list, image=trash_img, bg=cor_f_list, command=lambda: self.Delete_product(product[0]))
        delete_button.image = trash_img
        delete_button.grid(row=0, column=3, padx=10, pady=5)

    def Delete_product(self, product_id):
        result = messagebox.askquestion("Confirmar Exclusão", "Tem certeza que deseja excluir este produto?", icon='warning')
        if result == 'yes':
            conn = sqlite3.connect('database/stock.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
            self.frame_list.destroy()  #Remover o frame após a exclusao
            self.e_id.delete(0, END) #limpar a entry apos exclusao
        else:
            messagebox.showinfo("Cancelado", "Exclusão cancelada.")

# CONFIGURAÇÕES DE JANELA
if __name__ == '__main__':
    root = Tk()
    root.geometry('500x500')
    root.configure(bg=cor_root)
    root.title('Cadastro de Produtos')
    root.resizable(width=False, height=False)

    app = Main_page(root)

    root.mainloop()
