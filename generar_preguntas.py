import os, json
from openai import OpenAI
from temas import TEMAS  # <-- Importamos la lista de temas

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("No se encontró OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

preguntas_json = {}

for tema in TEMAS:
    preguntas_tema = []
    for _ in range(10):  # 10 preguntas por tema
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
Nivel medio, español de España, clara y concisa.
"""
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        pregunta = json.loads(resp.choices[0].message.content)
        pregunta["tema"] = tema
        preguntas_tema.append(pregunta)
    preguntas_json[tema] = preguntas_tema

with open("preguntas.json", "w", encoding="utf-8") as f:
    json.dump(preguntas_json, f, ensure_ascii=False, indent=2)

print("✅ Preguntas generadas y guardadas en preguntas.json")
