import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://carro.mercadolivre.com.br/MLB-6864663498-ora-5-_JM"

headers = {
    "User-Agent": "Mozilla/5.0"
}

pagina = requests.get(URL, headers=headers)

texto = pagina.text.lower()

alerta = False
mensagem = ""

# anúncio saiu do ar
if (
    "página não encontrada" in texto
    or "pagina nao encontrada" in texto
    or "este anúncio terminou" in texto
    or "este anúncio foi finalizado" in texto
):
    alerta = True
    mensagem = "🚨 O anúncio do ORA 5 foi encerrado ou removido."

# preço mudou
elif "159.900" not in texto and "159900" not in texto:
    alerta = True
    mensagem = "💰 O preço do ORA 5 mudou."

if alerta:
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": mensagem + "\n\n" + URL
        }
    )

print(mensagem if alerta else "Sem alterações.")
