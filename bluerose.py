import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import requests
import rastreio as rastreio
from rastreio import Rastreioclass
import site_scanner
from PIL import ImageTk, Image
import threading
import tkinter.messagebox as mb
import tkinter.scrolledtext as scrolledtext

class Interface(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Blue Rose")
        self.iconbitmap("imagens/bluerose_icon.ico")
        self.geometry("500x500")
        self.resizable(False, False)
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

        label_by = ctk.CTkLabel(self.frame_menu, text="by SLR")
        label_by.grid(row=5, column=0, columnspan=2)

        # lista de botões
        self.botoes = [
            ("Rastreio de IP", self.mostrar_rastreio),
            ("Tool 3", None),
            ("Tool 5", None),
            ("Tool 7", None),
            ("Scanner de Site", self.mostrar_scanner),
            ("Tool 4", None),
            ("Tool 6", None),
            ("Quit", self.destroy)
        ]

        # adiciona os botões em 2 colunas e 4 linhas
        for i, (texto, comando) in enumerate(self.botoes):
            col = 0 if i < 4 else 1  # define a coluna (esquerda/direita)
            row = (i % 4) + 1        # linhas 1 a 4
            button = ctk.CTkButton(self.frame_menu, text=texto, font=("Arial", 20), width=200, height=80, command=comando)
            button.grid(row=row, column=col, padx=20, pady=(10, 20))

        # =====================
        # = FRAME DE RASTREIO =
        # =====================
        self.frame_rastreio = ctk.CTkFrame(self.container)
        self.frame_rastreio.place(relwidth=1, relheight=1)

        label_menuip = ctk.CTkLabel(self.frame_rastreio, text="Digite o IP:", font=("Arial", 20))
        label_menuip.pack(pady=(60, 10))

        self.entry_ip = ctk.CTkEntry(self.frame_rastreio, width=200, height=10, font=("Arial", 20))
        self.entry_ip.pack(pady=10)

        self.button_track = ctk.CTkButton(self.frame_rastreio, text="Rastreio", width=160, height=80, command=self.rastrear, font=("Arial", 20))
        self.button_track.pack(pady=(20, 15))

        button_menu_rastreio = ctk.CTkButton(self.frame_rastreio, text="Menu", width=120, height=80, command=self.mostrar_menu, font=("Arial", 20))
        button_menu_rastreio.pack(pady=(60, 15))

        self.label_by = ctk.CTkLabel(self.frame_rastreio, text="by SLR")
        self.label_by.pack(side="bottom")

        # ====================
        # = FRAME DO SCANNER =
        # ====================
        self.frame_scanner = ctk.CTkFrame(self.container)
        self.frame_scanner.place(relwidth=1, relheight=1)

        label_scanner = ctk.CTkLabel(self.frame_scanner, text="Digite o domínio (ex: example.com):", font=("Arial", 20))
        label_scanner.pack(pady=(20, 6))

        self.entry_site = ctk.CTkEntry(self.frame_scanner, width=300, height=30, font=("Arial", 20))
        self.entry_site.pack(pady=(4, 10))

        switches_frame = ctk.CTkFrame(self.frame_scanner)
        switches_frame.pack(pady=(4, 8))

        self.switch_sub_var = ctk.StringVar(value="0")
        self.switch_paths_var = ctk.StringVar(value="0")

        self.switch_sub = ctk.CTkSwitch(switches_frame, text="Subdomains", variable=self.switch_sub_var, onvalue="1", offvalue="0", command=self._switch_feedback)
        self.switch_sub.pack(side="left", padx=12)

        self.switch_paths = ctk.CTkSwitch(switches_frame, text="Paths", variable=self.switch_paths_var, onvalue="1", offvalue="0", command=self._switch_feedback)
        self.switch_paths.pack(side="left", padx=12)

        # label de instrução (avisa que é obrigatório selecionar pelo menos um)
        self.label_switch_req = ctk.CTkLabel(self.frame_scanner, text="Selecione Subdomains e/ou Paths antes de Scan", text_color="red",font=("Arial", 20))
        self.label_switch_req.pack(pady=(6, 6))

        self.button_scan = ctk.CTkButton(self.frame_scanner, text="Scan", width=160, height=80, command=self.scanner, font=("Arial", 20))
        self.button_scan.pack(padx=50, pady=5)

        self.button_cancel = ctk.CTkButton(self.frame_scanner, text="Menu", width=120, height=80, command=self.mostrar_menu, font=("Arial", 20))
        self.button_cancel.pack(padx=50, pady=5)

        self.label_by = ctk.CTkLabel(self.frame_scanner, text="by SLR")
        self.label_by.pack(side="bottom")

        # começa mostrando o menu
        self.mostrar_menu()

    def mostrar_menu(self):
        self.frame_menu.tkraise()

    def mostrar_rastreio(self):
        self.frame_rastreio.tkraise()

    def mostrar_scanner(self):
        self.frame_scanner.tkraise()

    def rastrear(self):
        ip = self.entry_ip.get()
        rastreio = Rastreioclass(ip)
        rastreio.rastrear()

    def _switch_feedback(self):
        sub = (self.switch_sub_var.get() == "1")
        paths = (self.switch_paths_var.get() == "1")
        if sub or paths:
            self.label_switch_req.configure(text="Pronto para scan", text_color="green")
        else:
            self.label_switch_req.configure(text="Selecione Subdomínios e/ou Paths antes de Scan", text_color="red")

    # output do scanner com janela separada
    def scanner(self):
        site = self.entry_site.get().strip()
        sub_on = (self.switch_sub_var.get() == "1")
        paths_on = (self.switch_paths_var.get() == "1")

        # validações mínimas
        if not site:
            mb.showerror("Erro", "Informe o domínio (ex: example.com)")
            return

        if not (sub_on or paths_on):
            mb.showerror("Erro", "Selecione Subdomínios e/ou Paths antes de iniciar o scan.")
            return

        # cria nova janela de output
        output_window = ctk.CTkToplevel(self)
        output_window.title(f"Scanner - {site}")
        output_window.geometry("700x500")
        output_window.resizable(False, False)

        output_box = scrolledtext.ScrolledText(
            output_window,
            width=80,
            height=25,
            wrap="word",
            font=("Consolas", 11)
        )
        output_box.pack(padx=10, pady=10, fill="both", expand=True)
        output_box.insert("end", f"[i] Iniciando scan em {site}\n")
        output_box.insert("end", f"Subdomínios: {sub_on} | Paths: {paths_on}\n\n")

        # --- função que roda em thread ---
        def _job():
            try:
                sc = site_scanner
                results_count = 0

                if sc:
                    # subdomínios
                    if sub_on and hasattr(sc, "scan_subdomains"):
                        output_box.insert("end", "[i] Escaneando subdomínios...\n")
                        subs = sc.scan_subdomains(site, lists_dir="listas", workers=25, timeout=4, do_http=True)
                        for r in subs:
                            if isinstance(r, dict) and r.get("host") == "__WILDCARD_DETECTED__":
                                output_box.insert("end", f"[AVISO] Wildcard detectado: {r.get('ip')}\n")
                                continue
                            line = f"{r.get('host', '')} -> {r.get('ip', '')}  HTTP: {r.get('http_status', '')}\n"
                            output_box.insert("end", line)
                            results_count += 1

                    # paths
                    if paths_on and hasattr(sc, "scan_paths"):
                        output_box.insert("end", "\n[i] Escaneando paths...\n")
                        paths = sc.scan_paths(site, lists_dir="listas", workers=25, timeout=4)
                        for p in paths:
                            line = f"[{p.get('http_status')}] {p.get('url')} size={p.get('size')}\n"
                            output_box.insert("end", line)
                            results_count += 1

                else:
                    output_box.insert("end", "[ERRO] Módulo site_scanner não encontrado.\n")

                output_box.insert("end", f"\n[i] Scan finalizado. Resultados aproximados: {results_count}\n")
                output_box.see("end")

            except Exception as e:
                output_box.insert("end", f"[ERRO] {e}\n")
                output_box.see("end")

        # roda em thread para não travar a UI
        threading.Thread(target=_job, daemon=True).start()

if __name__ == "__main__":
    app = Interface()
    app.mainloop()
