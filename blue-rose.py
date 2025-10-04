import tkinter as tk
from tkinter import messagebox
import requests

class Rastreio:
    def __init__(self, ip):
        self.ip = ip

    def rastrear(self):
        url = f"http://ip-api.com/json/{self.ip}"
        resposta = requests.get(url).json()
        if resposta["status"] == "success":
            resultado = (
                f"IP: {resposta['query']}\n"
                f"País: {resposta['country']}\n"
                f"Região: {resposta['regionName']}\n"
                f"Cidade: {resposta['city']}\n"
                f"Provedor (ISP): {resposta['isp']}\n"
                f"Latitude: {resposta['lat']}\n"
                f"Longitude: {resposta['lon']}"
            )
            messagebox.showinfo("IP info", resultado)
        else:
            messagebox.showerror("Error", "IP not found (Private)")

class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("blue rose")
        self.root.geometry("500x400")
        self.root.resizable(False, False)


        # label
        self.label = tk.Label(root, text="Type IP ", width= 10, height= 5, font=("", 14))
        self.label.place(x=200, y=10)

        # campo de entrada
        self.entry = tk.Entry(root, width=20, font=("Arial", 14))
        self.entry.place(x=145, y=100)

        # botão
        self.botao = tk.Button(root, text="Track", command=self.rastrear, width= 20, height= 3, font=("Arial", 10))
        self.botao.place(x=170, y=150)
        self.botaoq = tk.Button(root, text="Quit", command=root.destroy, width= 20, height= 3, font=("Arial", 10))
        self.botaoq.place(x=170, y=250)
        
    def rastrear(self):
        ip_digitado = self.entry.get()
        rastreio_obj = Rastreio(ip_digitado)  # cria o objeto da classe
        rastreio_obj.rastrear()               # chama o método que faz o rastreio

if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()