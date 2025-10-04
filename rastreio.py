from tkinter import messagebox
import requests

class Rastreioclass:
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
