import tkinter as tk
from tkinter import messagebox
import requests
import rastreio
from rastreio import Rastreioclass

class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Blue Rose")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        # frame container
        self.container = tk.Frame(root)
        self.container.pack(fill="both", expand=True)

        # main menu
        self.frm_menu = tk.Frame(self.container)
        self.frm_menu.place(relwidth=1, relheight=1)

        # centraliza as colunas e linhas
        for i in range(6):  # linhas (label + 4 botões)
            self.frm_menu.grid_rowconfigure(i, weight=1)
        for j in range(2):  # duas colunas
            self.frm_menu.grid_columnconfigure(j, weight=1)

        lbl_menu = tk.Label(self.frm_menu, text="Main Menu", font=("Arial", 18))
        lbl_menu.grid(row=0, column=0, columnspan=2, pady=10)

        # lista de botões
        self.botoes = [
            ("Track IP", self.mostrar_rastreio),
            ("Tool 2", None),
            ("Tool 3", None),
            ("Tool 4", None),
            ("Tool 5", None),
            ("Tool 6", None),
            ("Tool 7", None),
            ("Quit", root.destroy)
        ]

        # adiciona os botões em 2 colunas e 4 linhas
        for i, (texto, comando) in enumerate(self.botoes):
            col = 0 if i < 4 else 1  # define a coluna (esquerda/direita)
            row = (i % 4) + 1        # linhas 1 a 4
            btn = tk.Button(self.frm_menu, text=texto, font=("Arial", 12), width=15, height=2, command=comando)
            btn.grid(row=row, column=col, padx=20, pady=10)

        # ----------- FRAME DE RASTREIO -----------
        self.frm_rastreio = tk.Frame(self.container)
        self.frm_rastreio.place(relwidth=1, relheight=1)

        #label do menu ip
        lbl_menuip = tk.Label(self.frm_rastreio, text="Type IP:", font=("Arial", 14))
        lbl_menuip.pack(pady=(40, 20))

        self.entry_ip = tk.Entry(self.frm_rastreio, width=25, font=("Arial", 14))
        self.entry_ip.pack(pady=10)

        btn_track = tk.Button(self.frm_rastreio, text="Track", width=20, height=3, command=self.rastrear, font=("Arial", 14))
        btn_track.pack(pady=(20, 15))

        btn_back = tk.Button(self.frm_rastreio, text="Menu", width=15, height=2, command=self.mostrar_menu, font=("Arial", 14))
        btn_back.pack(pady=25)

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
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()
