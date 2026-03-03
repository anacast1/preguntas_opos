import os, json, random
import requests
from openai import OpenAI

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)
HISTORIAL_FILE = "preguntas_recientes.txt"

# Lista de temas (puedes tener 50)
TEMAS = [
    "RGPD","ENS","Contratación pública","Transparencia","Interoperabilidad",
    "Gestión de proyectos","ITIL","Firma electrónica","Protección de datos",
    "Desarrollo de software","Gestión documental","Calidad","Mantenimiento de sistemas",
    "Seguridad informática","Ciberseguridad","Leyes TIC","Servicios digitales",
    "Administración electrónica","Planificación urbana","Finanzas públicas",
    "Derecho administrativo","Contratos públicos","Normativa europea",
    "Auditoría","Gestión de riesgos","Seguridad física","Accesibilidad",
    "Innovación tecnológica","Open data","Blockchain","Inteligencia artificial",
    "Big data","IoT","Cloud computing","Gestión ambiental","Sostenibilidad",
    "Transporte público","Educación","Salud pública","Turismo","Cultura",
    "Urbanismo","Vivienda","Emergencias","Protección civil","Comunicación",
    "Participación ciudadana","Inclusión social","Igualdad","Economía",
    "Investigación científica","Servicios sociales"
]

# -----------------------
# historial para no repetir
# -----------------------
def cargar_historial():
    if not os.path.exists(HISTORIAL_FILE):
        return []
    with open(HISTORIAL_FILE, encoding="utf-8") as f:
        return [x.strip() for x in f.readlines()]

def guardar_historial(pregunta):
    historial = cargar_historial()
    historial.append(pregunta)
    historial = historial[-100:]  # últimas 100
    with open(HISTORIAL_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(historial))

# -----------------------
# elegir tema y generar pregunta
# -----------------------
def generar_pregunta():
    tema = random.choice(TEMAS)
    prompt = f"""
Genera UNA pregunta tipo test para oposiciones sobre el tema "{tema}".
Devuelve JSON EXACTO:
{{
  "pregunta": "...",
  "A": "...",
  "B": "...",
  "C": "...",
  "D": "...",
  "correcta": "A",
  "explicacion": "..."
}}
Nivel medio, español de España, clara, concisa.
"""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9
    )
    import json
    return json.loads(resp.choices[0].message.content)

# -----------------------
# enviar Telegram
# -----------------------
def enviar(p):
    texto = (
        f"📚 *Pregunta tipo test* (Tema: {p.get('tema','General')})\n\n"
        f"{p['pregunta']}\n\n"
        f"A) {p['A']}\n"
        f"B) {p['B']}\n"
        f"C) {p['C']}\n"
        f"D) {p['D']}\n\n"
        f"✅ *Respuesta correcta:* {p['correcta']}\n"
        f"📖 *Explicación:* {p['explicacion']}"
    )
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": texto,
            "parse_mode": "Markdown"
        }
    )

# -----------------------
# main
# -----------------------
def main():
    historial = cargar_historial()
    for _ in range(3):
        p = generar_pregunta()
        if p["pregunta"] not in historial:
            break
    guardar_historial(p["pregunta"])
    enviar(p)

if __name__ == "__main__":
    main()
