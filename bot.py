import logging
import os
import datetime
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

DATA = {
    "week_days": [
        "Dushanba",
        "Seshanba",
        "Chorshanba",
        "Payshanba",
        "Juma",
        "Shanba",
        "Yakshanba",
    ],
    "schedule": {
        "7A": {
            "Dushanba": ["Kelajak soati", "Jismoniy tarbiya", "Fizika", "Matematika", "Ingliz tili", "Ona tili"],
            "Seshanba": ["Fizika", "Kimyo", "Matematika", "Texnologiya", "Tasviriy san'at", "Ingliz tili"],
            "Chorshanba": ["Matematika", "O`zbekiston tarixi", "Texnologiya", "Ona tili", "Ingliz tili", "Tarbiya"],
            "Payshanba": ["O`zbekiston tarixi", "Geografiya", "Ona tili", "Geografiya", "Ingliz tili", "Jismoniy tarbiya"],
            "Juma": ["Rus til va adabiyoti", "Informatika", "Matematika", "Biologiya", "Adabiyot", "Musiqa"],
            "Shanba": ["Kimyo", "Biologiya", "Adabiyot", "Matematika", "Rus til va adabiyoti", "Jahon tarixi"],
            "Yakshanba": ["Bugun dam olish kuni 😊"],
        },
        "7B": {
            "Dushanba": ["Kelajak soati", "Fizika", "Rus til va adabiyoti", "Matematika", "Ingliz tili", "Texnologiya"],
            "Seshanba": ["Tasviriy san'at", "Fizika", "Kimyo", "Ingliz tili", "Matematika", "Geografiya"],
            "Chorshanba": ["Jismoniy tarbiya", "O`zbekiston tarixi", "Matematika", "Ona tili", "Musiqa", "Rus til va adabiyoti"],
            "Payshanba": ["Ingliz tili", "Tarbiya", "Kimyo", "Biologiya", "Ona tili", "Ona tili"],
            "Juma": ["Jismoniy tarbiya", "Matematika", "Biologiya", "Texnologiya", "Adabiyot", "Jahon tarixi"],
            "Shanba": ["Ingliz tili", "Matematika", "Informatika", "Adabiyot", "O`zbekiston tarixi", "Geografiya"],
            "Yakshanba": ["Bugun dam olish kuni 😊"],
        },
        "7V": {
            "Dushanba": ["Kelajak soati", "Geografiya", "Matematika", "Informatika", "Ona tili", "Ingliz tili"],
            "Seshanba": ["Texnologiya", "Matematika", "Jahon tarixi", "Ingliz tili", "Biologiya", "Tasviriy san'at"],
            "Chorshanba": ["O`zbekiston tarixi", "Matematika", "Ona tili", "Jismoniy tarbiya", "Adabiyot", "Ingliz tili"],
            "Payshanba": ["Ingliz tili", "Kimyo", "O`zbekiston tarixi", "Jismoniy tarbiya", "Fizika", "Adabiyot"],
            "Juma": ["Texnologiya", "Biologiya", "Matematika", "Rus til va adabiyoti", "Tarbiya", "Fizika"],
            "Shanba": ["Geografiya", "Ona tili", "Rus til va adabiyoti", "Matematika", "Musiqa", "Kimyo"],
            "Yakshanba": ["Bugun dam olish kuni 😊"],
        },
        "8A": {
            "Dushanba": ["Kelajak soati", "Jismoniy tarbiya", "Kimyo", "Adabiyot", "Biologiya", "Ona tili"],
            "Seshanba": ["Davlat va huquq asoslari", "Informatika", "Texnologiya", "Algebra", "Ingliz tili", "Geometriya"],
            "Chorshanba": ["Adabiyot", "Chizmachilik", "Rus til va adabiyoti", "Algebra", "Jismoniy tarbiya"],
            "Payshanba": ["Geografiya", "O`zbekiston tarixi", "Fizika", "Ingliz tili", "Ona tili", "Rus til va adabiyoti"],
            "Juma": ["Fizika", "Kimyo", "O`zbekiston tarixi", "Ona tili", "Jahon tarixi", "Geometriya"],
            "Shanba": ["Tarbiya", "Ingliz tili", "Algebra", "Biologiya", "IBA"],
            "Yakshanba": ["Bugun dam olish kuni 😊"],
        },
        "8B": {
            "Dushanba": ["Kelajak soati", "Algebra", "Geometriya", "Ona tili", "Informatika", "Ingliz tili"],
            "Seshanba": ["Geografiya", "Jismoniy tarbiya", "Algebra", "Davlat va huquq asoslari", "Texnologiya", "Ingliz tili"],
            "Chorshanba": ["Ona tili", "O`zbekiston tarixi", "Ingliz tili", "Algebra", "Rus til va adabiyoti"],
            "Payshanba": ["Biologiya", "Jismoniy tarbiya", "Jahon tarixi", "Biologiya", "Kimyo", "Tarbiya"],
            "Juma": ["Ona tili", "Chizmachilik", "Adabiyot", "O`zbekiston tarixi", "Rus til va adabiyoti"],
            "Shanba": ["Adabiyot", "Geometriya", "Fizika", "Geografiya", "Kimyo", "Fizika"],
            "Yakshanba": ["Bugun dam olish kuni 😊"],
        },
        "9A": {
            "Dushanba": ["Kelajak soati", "Adabiyot", "Algebra", "Rus til va adabiyoti", "Ona tili", "Geografiya"],
            "Seshanba": ["Ingliz tili", "Algebra", "Davlat va huquq asoslari", "Fizika", "Informatika"],
            "Chorshanba": ["Jahon tarixi", "Algebra", "Rus til va adabiyoti", "Texnologiya", "O`zbekiston tarixi", "Ingliz tili"],
            "Payshanba": ["Adabiyot", "Geografiya", "Jismoniy tarbiya", "Chizmachilik", "Biologiya", "Kimyo"],
            "Juma": ["Fizika", "Ona tili", "Jismoniy tarbiya", "Geometriya", "Biologiya", "Tarbiya"],
            "Shanba": ["Informatika", "Kimyo", "Ingliz tili", "Ona tili", "Geometriya", "O`zbekiston tarixi"],
            "Yakshanba": ["Bugun dam olish kuni 😊"],
        },
        "9B": {
            "Dushanba": ["Kelajak soati", "Ingliz tili", "Informatika", "Biologiya", "Kimyo", "Adabiyot"],
            "Seshanba": ["O`zbekiston tarixi", "Geografiya", "Jismoniy tarbiya", "Informatika", "Algebra", "Jahon tarixi"],
            "Chorshanba": ["Algebra", "Jismoniy tarbiya", "O`zbekiston tarixi", "Ingliz tili", "Geometriya"],
            "Payshanba": ["Chizmachilik", "Adabiyot", "Biologiya", "Rus til va adabiyoti", "Geografiya", "Texnologiya"],
            "Juma": ["Davlat va huquq asoslari", "Ona tili", "Rus til va adabiyoti", "Ona tili", "Fizika", "Tarbiya"],
            "Shanba": ["Geometriya", "Algebra", "Kimyo", "Ingliz tili", "Fizika", "Ona tili"],
            "Yakshanba": ["Bugun dam olish kuni 😊"],
        },
        "9V": {
            "Dushanba": ["Kelajak soati", "Geografiya", "Biologiya", "Jismoniy tarbiya", "Algebra", "Ona tili"],
            "Seshanba": ["Ingliz tili", "Biologiya", "Informatika", "Davlat va huquq asoslari", "Kimyo", "Algebra"],
            "Chorshanba": ["Adabiyot", "Ingliz tili", "Ona tili", "Algebra", "Informatika"],
            "Payshanba": ["Jahon tarixi", "Chizmachilik", "IBA", "Jismoniy tarbiya", "Adabiyot", "Ingliz tili"],
            "Juma": ["Kimyo", "Fizika", "Geometriya", "Rus til va adabiyoti", "O`zbekiston tarixi", "Texnologiya"],
            "Shanba": ["Fizika", "Rus til va adabiyoti", "O`zbekiston tarixi", "Geometriya", "Ona tili", "Tarbiya"],
            "Yakshanba": ["Bugun dam olish kuni 😊"],
        },
    },
    "announcements": [],
}

WEEK_DAYS = DATA["week_days"]
SCHEDULE = DATA["schedule"]
CLASS_NAMES = list(SCHEDULE.keys())

def split_keyboard(items, row_size=3):
    return [items[i : i + row_size] for i in range(0, len(items), row_size)]

def class_keyboard():
    return ReplyKeyboardMarkup(split_keyboard(CLASS_NAMES, 3), resize_keyboard=True)

def main_keyboard():
    return ReplyKeyboardMarkup(
        [["Bugungi", "Ertangi"], ["Haftalik", "Sinifni o'zgartirish"]],
        resize_keyboard=True,
    )

def kun_nomini_aniqla(offset=0):
    bugun = datetime.datetime.now().weekday()
    return WEEK_DAYS[(bugun + offset) % 7]

async def prompt_class_choice(update: Update, text: str | None = None):
    matn = text or "Iltimos, avval sinfni tanlang."
    await update.message.reply_text(matn, reply_markup=class_keyboard())

def get_schedule_for_day(class_name: str, day: str):
    return SCHEDULE.get(class_name, {}).get(day, ["Bu kun uchun jadval topilmadi."])

def format_lessons(lessons):
    if not lessons:
        return ["Bu kun uchun jadval topilmadi."]
    return [f"{idx + 1}. {lesson}" for idx, lesson in enumerate(lessons)]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_class = context.user_data.get("class")
    if not user_class:
        await update.message.reply_text(
            "Salom! Avval qaysi sinf jadvalini ko‘rmoqchi ekaningizni tanlang.",
            reply_markup=class_keyboard(),
        )
    else:
        await update.message.reply_text(
            f"Salom! Siz {user_class} sinfi jadvali bilan ishlayapsiz.",
            reply_markup=main_keyboard(),
        )

async def tugma_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    matn = update.message.text.strip()
    past_matn = matn.lower()
    if matn in CLASS_NAMES:
        context.user_data["class"] = matn
        await update.message.reply_text(
            f"{matn} sinfi jadvali tanlandi. Endi kerakli bo‘limni tanlang.",
            reply_markup=main_keyboard(),
        )
        return

    if past_matn == "sinifni o'zgartirish":
        context.user_data.pop("class", None)
        await prompt_class_choice(update, "Qaysi sinf jadvalini ko‘rmoqchisiz?")
        return

    user_class = context.user_data.get("class")
    if not user_class:
        await prompt_class_choice(update)
        return

    if past_matn == "bugungi":
        kun = kun_nomini_aniqla(0)
        darslar = format_lessons(get_schedule_for_day(user_class, kun))
        javob = f"{user_class} sinfi uchun bugungi darslar ({kun}):\n" + "\n".join(darslar)
    elif past_matn == "ertangi":
        kun = kun_nomini_aniqla(1)
        darslar = format_lessons(get_schedule_for_day(user_class, kun))
        javob = f"{user_class} sinfi uchun ertangi darslar ({kun}):\n" + "\n".join(darslar)
    elif past_matn == "haftalik":
        javob = f"{user_class} sinfi uchun haftalik jadval:"
        for kun_nomi in WEEK_DAYS:
            darslar = format_lessons(get_schedule_for_day(user_class, kun_nomi))
            javob += f"\n\n{kun_nomi}:\n" + "\n".join(darslar)
    else:
        javob = "Iltimos, tugmalardan birini tanlang!"
    await update.message.reply_text(javob)

def main():
    TOKEN = os.getenv("TOKEN") or "8527268214:AAF6tgrGp-7G3v6AJe54zQABhlW0Cd6Iybc"
    application = ApplicationBuilder().token(TOKEN).build()

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tugma_handler))

    print("Bot ishga tushdi!")
    application.run_polling()

if __name__ == "__main__":
    main()
    