import os
import re
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://carro.mercadolivre.com.br/MLB-6864663498-ora-5-_JM"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )
}

try:
    r = requests.get(URL, headers=headers, timeout=20, allow_redirects=True)
    html = r.text.lower()

    alerta = False
    mensagem = ""

    # Anúncio indisponível
    termos = [
        "página não encontrada",
        "pagina nao encontrada",
        "este anúncio terminou",
        "este anúncio foi finalizado",
        "publicação finalizada",
        "publicacao finalizada",
        "não está disponível",
        "nao esta disponivel",
        "produto não encontrado",
        "produto nao encontrado"
    ]

    if any(t in html for t in termos):
        alerta = True
        mensagem = "🚨 O anúncio do ORA 5 não está mais disponível."

    # Detecta alteração do preço
    preco = re.search(r'159[\.,]900', html)

    if not alerta and preco is None:
        alerta = True
        mensagem = "💰 O preço do ORA 5 mudou."

    if alerta:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": f"{mensagem}\n\n{URL}"
            },
            timeout=20
        )
        print(mensagem)
    else:
        print("Sem alterações.")

except Exception as e:
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": f"❌ Erro no monitor:\n{e}"
        },
        timeout=20
    )
    print(e)
