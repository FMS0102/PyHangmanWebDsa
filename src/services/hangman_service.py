import random, string, requests, re, os
from dotenv import load_dotenv

class HangmanService:

    def __init__(self):
        
        load_dotenv()
        
        self.lista_palavras = [
            "QUEEN",
            "KISS",
            "BLIND-GUARDIAN",
            "HAMMERFALL",
            "HELLOWEEN",
            "IRON-MAIDEN",
            "METALLICA",
            "NIGHTWISH",
            "DRAGONFORCE",
            "MANOWAR",
            "MEGADETH",
            "DIO",
            "ACCEPT",
            "EPICA",
            "SONATA-ARCTICA",
            "SABATON",
            "JUDAS-PRIEST",
            "AMON-AMARTH",
            "STRATOVARIUS",
            "GRAVE-DIGGER",
            "SONIC-SYNDICATE",
            "ICED-EARTH",
            "FREEDOM-CALL",
            "RHAPSODY",
            "BLIND-GUARDIAN",
            "HAMMERFALL",
            "HELLOWEEN",
            "IRON-MAIDEN",
            "METALLICA",
            "NIGHTWISH",
            "DRAGONFORCE",
            "MANOWAR",
        ]
        self.tentativas_erradas = []
        self.tentativas_corretas = []
        self.palavra_aleatoria = self.obter_palavra_aleatoria()
        self.api_key = os.environ.get("API_KEY")

    def obter_palavra_aleatoria(self):
        self.palavra_aleatoria = random.choice(self.lista_palavras)
        return self.palavra_aleatoria

    def resetar_listas(self):
        self.tentativas_erradas = []
        self.tentativas_corretas = []

    def obter_letras_disponiveis(self):
        alfabeto = string.ascii_uppercase
        letras_disponiveis = [letra for letra in alfabeto]
        return letras_disponiveis

    def adivinhar_letra(self, letra):
        letra = letra.upper()
        indices = []

        for i, char in enumerate(self.palavra_aleatoria):
            # obter o indice de cada letra da palavra
            if char == letra:
                indices.append(i)

        if indices:
            # verifica se a letra informada é um idx dos indices
            for idx in indices:
                self.tentativas_corretas.append(letra)
                return "Correto", self.contar_erros(), indices
        else:
            self.tentativas_erradas.append(letra)
            return "Incorreto", self.contar_erros(), indices

    def contar_erros(self):
        return len(self.tentativas_erradas)

    def obter_informacoes_artista(self, nome_banda):
        nome_artista = nome_banda.replace("-", "+")

        url_info = "http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={}&api_key={}&format=json".format(
            nome_artista, self.api_key
        )
        
        url_top_albums = "http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist={}&api_key={}&format=json".format(
            nome_artista, self.api_key
        )
        
        url_top_tracks = "http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist={}&api_key={}&format=json".format(
            nome_artista, self.api_key
        )
        
        print(url_top_albums)
        response_info = requests.get(url_info)
        response_top_albums = requests.get(url_top_albums)
        response_top_tracks = requests.get(url_top_tracks)

        if response_info.status_code == 200:
            data_info = response_info.json()
            data_top_albums = response_top_albums.json()
            data_top_tracks = response_top_tracks.json()

            # Extrair informações do artista
            artist_info = data_info["artist"]
            name = artist_info["name"]

            formed_year_summary = (
                re.search(r"(\d{4})", data_info["artist"]["bio"]["summary"]).group(1)
                if re.search(r"(\d{4})", data_info["artist"]["bio"]["summary"])
                else None
            )
            
            formed_year_content = (
                re.search(r"(\d{4})", data_info["artist"]["bio"]["content"]).group(1)
                if re.search(r"(\d{4})", data_info["artist"]["bio"]["content"])
                else None
            )
            
            ano_formacao = formed_year_summary if formed_year_summary is not None else formed_year_content
            
            top_albums = data_top_albums["topalbums"]["album"][:3]
            top_albums_list = []

            for album in top_albums:
                album_name = album["name"]
                album_large_image = [img["#text"] for img in album["image"] if img["size"] == "large"][0]
                top_albums_list.append({"name": album_name, "large_image": album_large_image})
            
            top_tracks = data_top_tracks["toptracks"]["track"][:5]
            top_tracks_list = []
            
            for track in top_tracks:
                track_name = track["name"]
                top_tracks_list.append(track_name)
            
            return ano_formacao, top_albums_list, top_tracks_list  
        else:
            print("Erro ao acessar a API:", response_info.status_code)
