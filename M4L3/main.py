
import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random

recognizer = sr.Recognizer()
translator = Translator()

# INTRODUÇÃO
lang = input("Para qual idioma quer jogar? (en, es, fr): ").strip().lower()

dificuldade = input(
    "Escolha a dificuldade (1-fácil, 2-médio, 3-difícil): "
)

palavrasfaceis = [
    "cachorro", "gato", "bola", "peixe",
    "pássaro", "papel", "mesa", "cadeira", "caneta"
]

palavrasmedias = [
    "sapato", "jarro", "cabeça", "braço",
    "coração", "porta", "dinheiro"
]

palavrasdificeis = [
    "estrela", "formiga", "goleiro", "sol"
]

# ESCOLHA DA DIFICULDADE
if dificuldade == "1":
    lista = palavrasfaceis
elif dificuldade == "2":
    lista = palavrasmedias
elif dificuldade == "3":
    lista = palavrasdificeis
else:
    print("Dificuldade inválida.")
    exit()

# CONFIGURAÇÕES
pontuacao = 0
rodadas = 0
acertos = 0

duration = 5
sample_rate = 44100

print("\n========== JOGO DE IDIOMAS ==========")
print("Acerte as traduções e acumule pontos!")
print("Cada acerto vale 10 pontos.")
print("Digite 'sair' para encerrar o jogo.")

# FUNÇÃO PARA NORMALIZAR AS RESPOSTAS
def normalizar(texto):
    texto = texto.lower().strip()
    return texto

# LOOP PRINCIPAL
while True:

    comando = input("\nPressione ENTER para começar uma rodada ou digite 'sair': ")

    if comando.lower().strip() == "sair":
        break

    # ESCOLHER PALAVRA
    palavra = random.choice(lista)

    # TRADUZIR
    try:
        traducao = translator.translate(
            palavra,
            dest=lang
        ).text

    except Exception as e:
        print("Erro na tradução:", e)
        continue

    print(f"\nTraduza: {palavra}")
    print("Você tem 5 segundos!")

    # GRAVAR ÁUDIO
    try:
        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16"
        )

        sd.wait()

        wav.write("output.wav", sample_rate, recording)

    except Exception as e:
        print("Erro na gravação:", e)
        continue

    print("Reconhecendo sua resposta...")

    # RECONHECER VOZ
    try:
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        resposta = recognizer.recognize_google(
            audio,
            language=lang
        )

        print("Você disse:", resposta)

        # VERIFICAR RESPOSTA
        rodadas += 1

        if normalizar(resposta) == normalizar(traducao):

            print("CORRETO! +10 pontos")
            pontuacao += 10
            acertos += 1

        else:
            print("Resposta incorreta!")
            print("Resposta correta:", traducao)

    except sr.UnknownValueError:
        rodadas += 1
        print("Não consegui reconhecer sua fala.")

    except sr.RequestError as e:
        print("Erro no serviço de reconhecimento:", e)
        continue

    # PLACAR
    print("\n---------- PLACAR ----------")
    print("Pontuação:", pontuacao)
    print("Acertos:", acertos)
    print("Rodadas:", rodadas)
    print("----------------------------")

# RESULTADO FINAL
print("\n========== RESULTADO FINAL ==========")
print("Pontuação total:", pontuacao)
print("Acertos:", acertos)
print("Rodadas:", rodadas)

if rodadas > 0:
    aproveitamento = (acertos / rodadas) * 100
    print(f"Aproveitamento: {aproveitamento:.1f}%")

print("Obrigado por jogar!")
