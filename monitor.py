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

if (
    "pausado" in texto
    or "finalizado" in texto
    or "vendido" in texto
    or "não está disponível" in texto
    or "nao esta disponivel" in texto
):
    mensagem = (
        "🚨 Atenção!\n\n"
        "O anúncio do ORA 5 mudou de status.\n"
        f"{URL}"
    )
else:
    mensagem = "✅ O anúncio do ORA 5 continua ativo."

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": mensagem
    }
)

print(mensagem)
