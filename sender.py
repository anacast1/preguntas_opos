import os, json, random, requests
from openai import OpenAI

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

TEMAS_FILE = "temas.json"
HISTORIAL_FILE = "preguntas_recientes.txt"

# -----------------------
# Cargar historial
# -----------------------
def cargar_historial():
    if not os.path.exists(HISTORIAL_FILE):
        return []
    with open(HISTORIAL_FILE, encoding="utf-8") as f:
        return [x.strip() for x in f.readlines()]

def guardar_historial(pregunta):
    historial = cargar_historial()
    historial.append(pregunta)
    historial = historial[-100:]  # Últimas 100
    with open(HISTORIAL_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(historial))

# -----------------------
# Elegir tema aleatorio
# -----------------------
def elegir_tema():
    with open(TEMAS_FILE, encoding="utf-8") as f:
        temas = json.load(f)
    return random.choice(temas)

# -----------------------
# Generar pregunta IA
# -----------------------
def generar_pregunta(tema):
    prompt = f"""
Genera UNA pregunta tipo test sobre el tema "{tema['tema']}".
Nivel: {tema['nivel']}.
Formato JSON EXACTO:
{{
  "pregunta": "...",
  "A": "...",
  "B": "...",
  "C": "...",
  "D": "...",
  "correcta": "A",
  "explicacion": "..."
}}
Reglas:
- Español España
- Clara y concisa
- Nunca repetir pregunta reciente
"""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9
    )
    import json
    return json.loads(resp.choices[0].message.content)

# -----------------------
# Enviar a Telegram
# -----------------------
def enviar(p):
    teclado = {
        "inline_keyboard": [[
            {"text":"A","callback_data":f"A|{p['correcta']}|{p['explicacion']}|{p['pregunta']}"},
            {"text":"B","callback_data":f"B|{p['correcta']}|{p['explicacion']}|{p['pregunta']}"},
            {"text":"C","callback_data":f"C|{p['correcta']}|{p['explicacion']}|{p['pregunta']}"},
            {"text":"D","callback_data":f"D|{p['correcta']}|{p['explicacion']}|{p['pregunta']}"},
        ]]
    }

    texto = (
        f"📚 *Pregunta tipo test* (Tema: {p.get('tema', 'General')})\n\n"
        f"{p['pregunta']}\n\n"
        f"A) {p['A']}\n"
        f"B) {p['B']}\n"
        f"C) {p['C']}\n"
        f"D) {p['D']}"
    )

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": texto,
            "parse_mode": "Markdown",
            "reply_markup": teclado
        }
    )

# -----------------------
# MAIN
# -----------------------
def main():
    tema = elegir_tema()
    historial = cargar_historial()
    for _ in range(3):  # Evitar repetidas
        p = generar_pregunta(tema)
        if p["pregunta"] not in historial:
            break
    guardar_historial(p["pregunta"])
    enviar(p)

if __name__ == "__main__":
    main()
