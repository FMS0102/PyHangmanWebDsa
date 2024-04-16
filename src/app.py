from flask import Flask, jsonify, render_template, request
from services.hangman_service import HangmanService

app = Flask(__name__)

hangman_service = HangmanService()


@app.route("/", methods=["GET"])
def index():
    global tentativas_restantes
    hangman_service.resetar_listas()
    palavra_secreta = hangman_service.obter_palavra_aleatoria()
    letras_disponiveis = hangman_service.obter_letras_disponiveis()
    tentativas_erradas = hangman_service.tentativas_erradas
    tentativas_corretas = hangman_service.tentativas_corretas
    tentativas_restantes = 6 - len(tentativas_erradas)
    print(palavra_secreta)

    ano_formacao, top_albums_list, top_tracks = (
        hangman_service.obter_informacoes_artista(palavra_secreta)
    )

    return render_template(
        "index.html",
        letras_disponiveis=letras_disponiveis,
        palavra_secreta=palavra_secreta,
        tentativas_erradas=tentativas_erradas,
        tentativas_corretas=tentativas_corretas,
        tentativas_restantes=tentativas_restantes,
        ano_formacao=ano_formacao,
        top_albums_list=top_albums_list,
        top_tracks=top_tracks,
    )


@app.route("/adivinhar-letra", methods=["POST"])
def adivinhar_letra():
    letra_clicada = request.form["letra"]
    resultado, contagem, indices = hangman_service.adivinhar_letra(letra_clicada)

    palavra_secreta = hangman_service.palavra_aleatoria

    return jsonify(
        {
            "resultado": resultado,
            "contagem": contagem,
            "indices": indices,
            "palavra_secreta": palavra_secreta,
        }
    )


if __name__ == "__main__":
    app.run(debug=False)
