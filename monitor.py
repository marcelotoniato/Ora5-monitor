import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

ITEM_ID = "MLB6864663498"

url = f"https://api.mercadolibre.com/items/{ITEM_ID}"

resposta = requests.get(url)

if resposta.status_code == 200:
    dados = resposta.json()
    status = dados.get("status", "").lower()

    if status == "active":
        mensagem = "✅ O anúncio do ORA 5 continua ATIVO."
    else:
        mensagem = (
            f"🚨 ATENÇÃO!\n\n"
            f"O anúncio mudou de status.\n"
            f"Status: {status}"
        )
else:
    mensagem = f"❌ Erro ao consultar o anúncio. Código: {resposta.status_code}"

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": mensagem
    }
)

print(mensagem)
