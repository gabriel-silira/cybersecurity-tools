from CTkMessagebox import CTkMessagebox
import requests

class Rastreioclass:
    def __init__(self, ip):
        self.ip = ip

    def rastrear(self):
        # se o campo estiver vazio vai usar o próprio IP
        # senão vai usar o IP que for digitado
        if self.ip == "":
            url = "http://ip-api.com/json/"
        else:
            url = f"http://ip-api.com/json/{self.ip}"

        print("IP recebido:", self.ip)
        resposta = requests.get(url).json()

        # informações que vão aparecer na janela "CTkMessagebox"
        if resposta["status"] == "success":
            resultado = (
                f"IP: {resposta['query']}\n"
                f"País: {resposta['country']}\n"
                f"Região: {resposta['regionName']}\n"
                f"Cidade: {resposta['city']}\n"
                f"Provedor (ISP): {resposta['isp']}\n"
                f"Zona: {resposta['timezone']}\n"
                f"Zip: {resposta['zip']}\n"
                f"Latitude: {resposta['lat']}\n"
                f"Longitude: {resposta['lon']}"
            )
            CTkMessagebox(title="IP Info", message=resultado, icon="info", option_1="Ok", border_width=5)
        else:
            CTkMessagebox(title="Error", message="IP not found (Private)", icon="cancel", option_1="Ok", border_width=5)
