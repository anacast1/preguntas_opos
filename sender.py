import os, json, random, requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TELEGRAM_TOKEN or not CHAT_ID:
    raise ValueError("No se encontró TELEGRAM_TOKEN o CHAT_ID")

# Cargar preguntas pre-generadas
with open("preguntas.json", "r", encoding="utf-8") as f:
    preguntas = json.load(f)

# Elegir un tema y pregunta aleatoria
tema = random.choice(list(preguntas.keys()))
pregunta = random.choice(preguntas[tema])

texto = (
    f"📚 *Pregunta tipo test* (Tema: {pregunta['tema']})\n\n"
    f"{pregunta['pregunta']}\n\n"
    f"A) {pregunta['A']}\n"
    f"B) {pregunta['B']}\n"
    f"C) {pregunta['C']}\n"
    f"D) {pregunta['D']}\n\n"
    f"✅ *Respuesta correcta:* {pregunta['correcta']}\n"
    f"📖 *Explicación:* {pregunta['explicacion']}"
)

requests.post(
    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
    json={"chat_id": CHAT_ID, "text": texto, "parse_mode": "Markdown"}
)
