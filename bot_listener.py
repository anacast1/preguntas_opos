import json, os
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TELEGRAM_TOKEN")
SCORES_FILE = "scores.json"

def cargar_scores():
    if not os.path.exists(SCORES_FILE):
        return {}
    with open(SCORES_FILE) as f:
        return json.load(f)

def guardar_scores(scores):
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f, indent=2)

async def boton(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = str(query.from_user.id)
    elegida, correcta, explicacion, pregunta = query.data.split("|", 3)

    scores = cargar_scores()
    scores.setdefault(user, {})
    scores[user].setdefault(pregunta, {"ok":0,"ko":0})

    if elegida == correcta:
        scores[user][pregunta]["ok"] += 1
        msg = "✅ *Correcto*\n\n"
    else:
        scores[user][pregunta]["ko"] += 1
        msg = f"❌ *Incorrecto*\nCorrecta: {correcta}\n\n"

    msg += f"📖 {explicacion}\n\n"

    # Puntuación total por usuario
    total_ok = sum(v["ok"] for v in scores[user].values())
    total_ko = sum(v["ko"] for v in scores[user].values())
    msg += f"🏆 Aciertos totales: {total_ok} | Fallos totales: {total_ko}"

    guardar_scores(scores)
    await query.edit_message_text(msg, parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CallbackQueryHandler(boton))
    app.run_polling()

if __name__ == "__main__":
    main()
