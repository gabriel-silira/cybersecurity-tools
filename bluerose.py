import customtkinter as ctk
import requests
import rastreio as rastreio
from rastreio import Rastreioclass
from PIL import ImageTk, Image

class Interface(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Blue Rose")
        self.iconbitmap("imagens/bluerose_icon.ico")
        self.geometry("500x500")
        self.resizable(False, False)

        # tema e cor padrão da app
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # frame container
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        # main menu
        self.frame_menu = ctk.CTkFrame(self.container)
        self.frame_menu.place(relwidth=1, relheight=1)

        # centraliza as colunas e linhas
        for i in range(6):  # linhas (label + 4 botões)
            self.frame_menu.grid_rowconfigure(i, weight=1)
        for j in range(2):  # duas colunas
            self.frame_menu.grid_columnconfigure(j, weight=1)

        # a parte escrita do Main Menu
        label_menu = ctk.CTkLabel(self.frame_menu, text="Main Menu", font=("Arial", 20))
        label_menu.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        # lista de botões
        self.botoes = [
            ("Rastreio de IP", self.mostrar_rastreio),
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
            button = ctk.CTkButton(self.frame_menu, text=texto, font=("Arial", 20), width=200, height=80, command=comando)
            button.grid(row=row, column=col, padx=20, pady=(10, 20))

        # frame do rastreio de ip
        self.frame_rastreio = ctk.CTkFrame(self.container)
        self.frame_rastreio.place(relwidth=1, relheight=1)

        # label do menu ip
        label_menuip = ctk.CTkLabel(self.frame_rastreio, text="Digite o IP:", font=("Arial", 20))
        label_menuip.pack(pady=(60, 10))
        # caixa de entrada do ip
        self.entry_ip = ctk.CTkEntry(self.frame_rastreio, width=200, height=10, font=("Arial", 20))
        self.entry_ip.pack(pady=10)
        # botão de rastreio
        self.button_track = ctk.CTkButton(self.frame_rastreio, text="Rastreio", width=160, height=80, command=self.rastrear, font=("Arial", 20))
        self.button_track.pack(pady=(20, 15))
        # botão de voltar para o menu
        button_back = ctk.CTkButton(self.frame_rastreio, text="Menu", width=120, height=80, command=self.mostrar_menu, font=("Arial", 20))
        button_back.pack(pady=(60, 15))
        # frame da progress bar pra deixar mais estético
        frameprogbar = ctk.CTkFrame(self.frame_rastreio, width=80, height=450)
        frameprogbar.place(x=380, y=50)
        # progress bar
        progbar1 = ctk.CTkProgressBar(frameprogbar, orientation="vertical", mode="indeterminate", indeterminate_speed=1)
        progbar1.start()
        progbar1.pack(padx=35, pady=100)

        # começa mostrando o menu
        self.mostrar_menu()

    # funções

    def mostrar_menu(self):
        self.frame_menu.tkraise()

    def mostrar_rastreio(self):
        self.frame_rastreio.tkraise()

    def rastrear(self):
        ip = self.entry_ip.get()
        rastreio = Rastreioclass(ip)
        rastreio.rastrear()

if __name__ == "__main__":
    app = Interface()
    app.mainloop()