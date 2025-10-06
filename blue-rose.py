import customtkinter as ctk
import requests
import rastreio
from rastreio import Rastreioclass

class Interface(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Blue Rose")
        self.geometry("500x450")
        self.resizable(False, False)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # frame container
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        # main menu
        self.frm_menu = ctk.CTkFrame(self.container)
        self.frm_menu.place(relwidth=1, relheight=1)

        # centraliza as colunas e linhas
        for i in range(6):  # linhas (label + 4 botões)
            self.frm_menu.grid_rowconfigure(i, weight=1)
        for j in range(2):  # duas colunas
            self.frm_menu.grid_columnconfigure(j, weight=1)

        lbl_menu = ctk.CTkLabel(self.frm_menu, text="Main Menu", font=("Arial", 20))
        lbl_menu.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        # lista de botões
        self.botoes = [
            ("Track IP", self.mostrar_rastreio),
            ("Tool 2", None),
            ("Tool 3", None),
            ("Tool 4", None),
            ("Tool 5", None),
            ("Tool 6", None),
            ("Tool 7", None),
            ("Quit", self.destroy)
        ]

        # adiciona os botões em 2 colunas e 4 linhas
        for i, (texto, comando) in enumerate(self.botoes):
            col = 0 if i < 4 else 1  # define a coluna (esquerda/direita)
            row = (i % 4) + 1        # linhas 1 a 4
            btn = ctk.CTkButton(self.frm_menu, text=texto, font=("Arial", 20), width=200, height=80, command=comando)
            btn.grid(row=row, column=col, padx=20, pady=(10, 20))

        # frame do rastreio de ip
        self.frm_rastreio = ctk.CTkFrame(self.container)
        self.frm_rastreio.place(relwidth=1, relheight=1)

        #label do menu ip
        lbl_menuip = ctk.CTkLabel(self.frm_rastreio, text="Type IP:", font=("Arial", 20))
        lbl_menuip.pack(pady=(60, 10))

        self.entry_ip = ctk.CTkEntry(self.frm_rastreio, width=200, height=10, font=("Arial", 20))
        self.entry_ip.pack(pady=10)

        btn_track = ctk.CTkButton(self.frm_rastreio, text="Track", width=160, height=80, command=self.rastrear, font=("Arial", 20))
        btn_track.pack(pady=(20, 15))

        btn_back = ctk.CTkButton(self.frm_rastreio, text="Menu", width=120, height=80, command=self.mostrar_menu, font=("Arial", 20))
        btn_back.pack(pady=(60, 15))

        # começa mostrando o menu
        self.mostrar_menu()

    def mostrar_menu(self):
        self.frm_menu.tkraise()

    def mostrar_rastreio(self):
        self.frm_rastreio.tkraise()

    def rastrear(self):
        ip = self.entry_ip.get()
        rastreio = Rastreioclass(ip)
        rastreio.rastrear()

if __name__ == "__main__":
    app = Interface()
    app.mainloop()
