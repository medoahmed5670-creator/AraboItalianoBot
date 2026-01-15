from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from gtts import gTTS
from apscheduler.schedulers.background import BackgroundScheduler
import os

TOKEN = os.getenv("TOKEN")
users = {}

lessons = {
    1: {
        "title": "A1 – Day 1 | التعارف",
        "text": "Ciao! Mi chiamo Mohamed. Come ti chiami?"
    },
    2: {
        "title": "A1 – Day 2 | التحيات",
        "text": "Buongiorno! Buonasera! Arrivederci!"
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    users[chat_id] = 1
    await update.message.reply_text(
        "🇮🇹 Ciao Mohamed!\n"
        "أنا مدرسك الإيطالي اليومي 👨‍🏫\n"
        "📘 الدروس هتوصلك تلقائيًا كل يوم"
    )

async def send_lesson(context: ContextTypes.DEFAULT_TYPE):
    for chat_id, day in users.items():
        lesson = lessons.get(day)
        if not lesson:
            continue

        tts = gTTS(text=lesson["text"], lang="it")
        file = f"day{day}.mp3"
        tts.save(file)

        await context.bot.send_message(
            chat_id=chat_id,
            text=f"📘 {lesson['title']}"
        )
        await context.bot.send_voice(chat_id=chat_id, voice=open(file, "rb"))
        users[chat_id] += 1

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

scheduler = BackgroundScheduler(timezone="Europe/Rome")
scheduler.add_job(lambda: app.create_task(send_lesson(app.bot)), "cron", hour=9)
scheduler.start()

app.run_polling()
