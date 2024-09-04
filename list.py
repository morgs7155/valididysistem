from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

cor_page= '#EEEEEE'
cor_f_cabecalho= '#9E9E9E'
cor_f_list= '#FFFFFF'
cor_button= '#4CAF50'
cor_fg_button= '#FFFFFF'

class List_page():
    def __init__(self, master):
        self.master = master
        self.Setup()
    
    def Setup(self):
        ####### Canvas e Scrollbar #########
        self.canvas = Canvas(self.master, bg=cor_page)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.scroll_bar = Scrollbar(self.master, orient='vertical', command=self.canvas.yview)
        self.scroll_bar.pack(side=RIGHT, fill=Y)

        self.canvas.configure(yscrollcommand=self.scroll_bar.set)

        # Frame dentro do Canvas para conter toda a interface
        self.main_frame = Frame(self.canvas, bg=cor_page)
        self.canvas.create_window((0, 0), window=self.main_frame, anchor='nw')

        ########## Cabeçalho ###########
        self.f_cabecalho = Frame(self.main_frame, width=500, height=100, bg=cor_f_cabecalho)
        self.f_cabecalho.pack(fill=X)

        ########## Data Atual ##########
        data_atual = datetime.now()
        format_date = data_atual.strftime("%d/%m/%Y")

        self.l_date = Label(self.main_frame, text='Data: ' + format_date, relief='solid', bg='white', fg='black')
        self.l_date.place(x=380, y=20)

        self.l_title = Label(self.main_frame, text='Lista de produtos', font='temple 22 bold', relief='flat', bg=cor_f_cabecalho, fg='white')
        self.l_title.place(x=10, y=10)

        ########## Conteúdo Rolável ##########
        self.frame_list = Frame(self.main_frame, bg=cor_f_list)
        self.frame_list.pack(fill=BOTH, expand=True)

        # Configurar scroll region após adicionar o conteúdo
        self.main_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        ######################### Criar a lista de produtos ###############################
        self.Create_list()

    def Create_list(self):
        conn = sqlite3.connect('database/stock.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, validity FROM products ORDER BY validity ASC")
        products = cursor.fetchall()
        conn.close()

        for idx, (product_id, name, validity) in enumerate(products):
            Label(self.frame_list, text=f"ID: {product_id}", bg=cor_f_list).grid(row=idx, column=0, padx=20, pady=5)
            Label(self.frame_list, text=f"Nome: {name}", bg=cor_f_list).grid(row=idx, column=1, padx=30, pady=5)
            Label(self.frame_list, text=f"Validade: {validity}", bg=cor_f_list).grid(row=idx, column=2, padx=50, pady=5)

            # Botão de editar
            edit_button = Button(self.frame_list, text="✎", bg=cor_button, fg=cor_fg_button, width=2, height=1, command=lambda p_id=product_id: self.Edit_product(p_id))
            edit_button.grid(row=idx, column=3, padx=10, pady=5)

        # Verifica e envia emails
        self.Send_email_reminders(products)

    def Edit_product(self, product_id):
        # Abrir nova janela para edição
        edit_window = Toplevel(self.master)
        edit_window.title(f"Editar Produto ID: {product_id}")
        edit_window.geometry("300x200")

        Label(edit_window, text="Nova Validade (dd/mm/yyyy):").pack(pady=10)
        new_validity = Entry(edit_window)
        new_validity.pack(pady=10)

        def update_date():
            new_date = new_validity.get()
            try:
                # Validar o formato da data
                datetime.strptime(new_date, '%d/%m/%Y')
                conn = sqlite3.connect('database/stock.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE products SET validity = ? WHERE id = ?", (new_date, product_id))
                conn.commit()
                conn.close()
                messagebox.showinfo("Sucesso", "Validade atualizada com sucesso!")
                edit_window.destroy()
                self.Refresh_list()  # Atualizar a lista após edição
            except ValueError:
                messagebox.showerror("Erro", "Formato de data inválido. Use dd/mm/yyyy.")

        Button(edit_window, text="Salvar", command=update_date).pack(pady=10)

    def Refresh_list(self):
        # Limpar a lista e recarregar os produtos
        for widget in self.frame_list.winfo_children():
            widget.destroy()
        self.Create_list()

    def Send_email_reminders(self, products):
        # Define a data de corte para o envio de e-mails
        cut_off_date = datetime.now() + timedelta(days=3)
        produtos_para_email = [(name, validity) for _, name, validity in products if datetime.strptime(validity, '%d/%m/%Y') <= cut_off_date]

        if produtos_para_email:
            sender_email = "evertonjohn097@gmail.com"
            receiver_email = "Peixotonatanael21@gmail.com"
            password = "123^^^john"

            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = "Aviso de produtos próximos ao vencimento"

            body = "Os seguintes produtos estão próximos do vencimento:\n\n"
            for name, validity in produtos_para_email:
                body += f"Produto: {name} - Validade: {validity}\n"

            message.attach(MIMEText(body, "plain"))

            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
                server.quit()
                print("Email enviado com sucesso!")
            except Exception as e:
                print(f"Erro ao enviar email: {e}")

if __name__ == '__main__':
    root = Tk()
    root.geometry('500x600')
    root.configure(bg=cor_page)
    root.title('Lista de produtos')
    root.resizable(width=False, height=False)

    app = List_page(root)

    root.mainloop()
