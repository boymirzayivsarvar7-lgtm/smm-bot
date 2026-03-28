import asyncio
import os
from aiohttp import web

async def handle(request):
    return web.Response(text="Bot ishlayapti")

async def start_web_app():
    app = web.Application()
    app.router.add_get("/", handle)

    port = int(os.environ.get("PORT", 10000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, ReplyKeyboardMarkup, KeyboardButton,
    FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.filters import CommandStart

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
user_history = {}

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

ADMIN_ID = 5354466357

# ================= STATES =================
class OrderState(StatesGroup):
    tariff = State()
    name = State()
    contact = State()
    comment = State()

# ================= MENU =================
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📌 Bio")],
        [KeyboardButton(text="🤝 Hamkorlarimiz")],
        [KeyboardButton(text="💰 Narxlar")],
        [KeyboardButton(text="📞 Aloqa")]
    ],
    resize_keyboard=True
)

menu_btn = menu

back_btn = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="⬅️ Orqaga")]],
    resize_keyboard=True
)

partners_btn = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚗 HAVAL"), KeyboardButton(text="🚗 CHERY")],
        [KeyboardButton(text="🛢 ROWE"), KeyboardButton(text="💒 TURON")],
        [KeyboardButton(text="🚘 AVTOMAKTAB"), KeyboardButton(text="🛒 F-MART")],
        [KeyboardButton(text="🎓 RARE"), KeyboardButton(text="🎤 OZODBEK")],
        [KeyboardButton(text="⬅️ Orqaga"), KeyboardButton(text="👕 EMIRAN")]
    ],
    resize_keyboard=True
)

# ================= START =================
@dp.message(CommandStart())
async def start(message: Message):

    user_history[message.from_user.id] = "menu"

    await message.answer(
        "👋 <b>Assalomu alaykum!</b>\n\n"
        
        "🎯 <b>Professional SMM xizmatlariga xush kelibsiz!</b>\n\n"
        
        "🚀 Biz sizning Instagram sahifangizni:\n"
        "📈 O‘stiramiz\n"
        "🎨 Dizayn qilamiz\n"
        "🎬 Kontent tayyorlaymiz\n"
        "🎯 Target reklama qilamiz\n\n"
        
        "💼 100+ muvaffaqiyatli loyihalar tajribasi mavjud\n\n"
        
        "👇 <b>Kerakli bo‘limni tanlang:</b>",
        
        parse_mode="HTML",
        reply_markup=menu_btn
    )

# ================= BIO =================
bio_btn = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛒 Buyurtma berish")],
        [KeyboardButton(text="⬅️ Orqaga")]
    ],
    resize_keyboard=True
)
@dp.message(F.text == "📌 Bio")
async def bio(message: Message):

    await message.answer(
        "📌 <b>Biz haqimizda</b>\n\n"
        
        "🚀 <b>Professional SMM xizmatlari</b>\n"
        "Biz sizning biznesingizni ijtimoiy tarmoqlarda\n"
        "<b>rivojlantirishga yordam beramiz</b> 📈\n\n"
        
        "💼 <b>Xizmatlarimiz:</b>\n"
        "✅ Post va Story tayyorlash\n"
        "✅ Videomontaj\n"
        "✅ Dizayn xizmatlari\n"
        "✅ Target reklama\n\n"
        
        "📊 <b>Natija:</b>\n"
        "📈 Kuzatuvchilar oshadi\n"
        "💰 Sotuvlar ko‘payadi\n"
        "🔥 Brendingiz kuchayadi\n\n"
        
        "💎 <b>Nega aynan biz?</b>\n"
        "✔️ 100+ muvaffaqiyatli loyihalar\n"
        "✔️ Tajribali jamoa\n"
        "✔️ Tez va sifatli xizmat\n\n"
        
        "👇 <b>Hoziroq boshlang!</b>\n"
        "🛒 Buyurtma berish tugmasini bosing 🚀",
        
        parse_mode="HTML",
        reply_markup=bio_btn
    )

# ================= BUYURTMA =================
@dp.message(F.text == "🛒 Buyurtma berish")
async def start_order(message: Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🥇 Gold"), KeyboardButton(text="🥈 Silver")],
            [KeyboardButton(text="🥉 Platinum")],
            [KeyboardButton(text="⬅️ Orqaga")]
        ],
        resize_keyboard=True
    )

    await message.answer("💼 Tarifni tanlang:", reply_markup=keyboard)
    await state.set_state(OrderState.tariff)

@dp.message(OrderState.tariff)
async def get_tariff(message: Message, state: FSMContext):
    if message.text == "⬅️ Orqaga":
        await state.clear()
        await message.answer("🏠 Menu", reply_markup=menu_btn)
        return

    await state.update_data(tariff=message.text)
    await message.answer("👤 Ismingizni kiriting:")
    await state.set_state(OrderState.name)

@dp.message(OrderState.name)
async def get_name(message: Message, state: FSMContext):
    if message.text == "⬅️ Orqaga":
        await state.clear()
        await message.answer("🏠 Menu", reply_markup=menu_btn)
        return

    await state.update_data(name=message.text)
    await message.answer("📞 Telefon yoki username:")
    await state.set_state(OrderState.contact)

@dp.message(OrderState.contact)
async def get_contact(message: Message, state: FSMContext):
    if message.text == "⬅️ Orqaga":
        await state.clear()
        await message.answer("🏠 Menu", reply_markup=menu_btn)
        return

    await state.update_data(contact=message.text)
    await message.answer("✍️ Izoh yozing:")
    await state.set_state(OrderState.comment)

@dp.message(OrderState.comment)
async def finish_order(message: Message, state: FSMContext):
    if message.text == "⬅️ Orqaga":
        await state.clear()
        await message.answer("🏠 Menu", reply_markup=menu_btn)
        return

    data = await state.get_data()

    text = (
        "🆕 Yangi buyurtma!\n\n"
        f"👤 Ism: {data['name']}\n"
        f"💼 Tarif: {data['tariff']}\n"
        f"📞 Aloqa: {data['contact']}\n"
        f"📝 Izoh: {message.text}\n\n"
        f"🔗 Username: @{message.from_user.username}"
    )

    await message.answer("✅ Buyurtma qabul qilindi!\n📞 Tez orada bog‘lanamiz")
    await message.bot.send_message(ADMIN_ID, text)

    await state.clear()

# ================= NARXLAR =================
@dp.message(F.text == "💰 Narxlar")
async def narxlar(message: Message):
    user_history[message.from_user.id] = "narx"

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🥇 Gold"), KeyboardButton(text="🥈 Silver")],
            [KeyboardButton(text="🥉 Platinum")],
            [KeyboardButton(text="🔙 Orqaga")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "💎 <b>SMM XIZMAT TARIFLARI</b>\n\n"
        
        "Siz uchun 3 xil tarif tayyorladik 👇\n\n"
        
        "🥇 GOLD — maksimal natija uchun\n"
        "🥈 SILVER — optimal variant\n"
        "🥉 PLATINUM — boshlash uchun\n\n"
        
        "📊 Har bir tarif o‘ziga xos imkoniyatlarga ega.\n"
        "📈 Sahifangizni o‘sishi uchun eng mosini tanlang.\n\n"
        
        "👇 O‘zingizga maqul tarifni tanlang\n"
        "va ichidan <b>Buyurtma berish</b> tugmasini bosing 🚀",
        
        parse_mode="HTML",
        reply_markup=keyboard
    )
@dp.message(F.text == "🥇 Gold")
async def gold(message: Message):

    user_history[message.from_user.id] = "gold"

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛒 Buyurtma berish")],
            [KeyboardButton(text="⬅️ Orqaga")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "🥇 <b>GOLD — 700$</b>\n"
        "━━━━━━━━━━━━━━━\n\n"

        "🔥 <b>Eng mashhur va maksimal natija beruvchi paket</b>\n\n"

        "📌 15 ta professional post\n"
        "📌 15 ta story\n"
        "📌 Target reklama — 100$\n\n"

        "📈 <b>Natija:</b>\n"
        "🚀 Tez o‘sish\n"
        "👥 Real auditoriya\n"
        "💰 Sotuv oshadi\n\n"

        "💎 <b>Tavsiya qilamiz!</b>",
        
        parse_mode="HTML",
        reply_markup=keyboard
    )

@dp.message(F.text == "🥈 Silver")
async def silver(message: Message):
    user_history[message.from_user.id] = "silver"

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛒 Buyurtma berish")],
            [KeyboardButton(text="⬅️ Orqaga")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "🥈 <b>SILVER — 500$</b>\n"
        "━━━━━━━━━━━━━━━\n\n"

        "⚖️ <b>Eng optimal va balansli paket</b>\n\n"

        "📌 15 ta post\n"
        "📌 15 ta story\n\n"

        "📈 <b>Natija:</b>\n"
        "📊 Sahifa rivojlanadi\n"
        "👀 Faollik oshadi\n\n"

        "👍 Ko‘pchilik tanlaydi",
        
        parse_mode="HTML",
        reply_markup=keyboard
    )

@dp.message(F.text == "🥉 Platinum")
async def platinum(message: Message):

    user_history[message.from_user.id] = "platinum"

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛒 Buyurtma berish")],
            [KeyboardButton(text="⬅️ Orqaga")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "🥉 <b>PLATINUM — 300$</b>\n"
        "━━━━━━━━━━━━━━━\n\n"

        "🚀 <b>Yangi boshlayotganlar uchun</b>\n\n"

        "📌 15 ta post\n"
        "📌 15 ta story\n\n"

        "📈 <b>Natija:</b>\n"
        "📊 Sahifa start oladi\n"
        "🔥 Brend shakllanadi\n\n"

        "💡 Boshlash uchun ideal",
        
        parse_mode="HTML",
        reply_markup=keyboard
    )


# ================= ALOQA =================
@dp.message(F.text == "📞 Aloqa")
async def contact(message: Message):
    await message.answer(
        "📞 Aloqa:\n\n"
        "👤 Admin: @SAR_VAR_07\n"
        "📱 Telefon: +998933385607",
        reply_markup=back_btn
    )

# ================= HAMKORLAR =================
@dp.message(F.text == "🤝 Hamkorlarimiz")
async def partners(message: Message):
    await message.answer("🤝 Bizning hamkorlarimiz 👇", reply_markup=partners_btn)

# ================= HAVAL =================
@dp.message(F.text == "🚗 HAVAL")
async def haval(message: Message):
    photo = FSInputFile("images/haval.jpg")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📱 Instagram", url="https://instagram.com/havalqarshi")],
            [InlineKeyboardButton(text="🌐 Rasmiy sayt", url="https://haval.uz/")],
            [InlineKeyboardButton(text="📍 Lokatsiya", url="https://yandex.uz/maps/-/CLqH5M-i")]
        ]
    )

    await message.answer_photo(
        photo=photo,
        caption=(
            "🚗 HAVAL Qashqadaryo\n\n"
            "🔘 Haval brendining Qashqadaryo viloyatidagi rasmiy dilleri\n"
            "🔘 5 yillik kafolat va servis xizmati\n\n"
            "☎️ +998 77 195 07 70\n"
            "☎️ +998 77 193 07 70\n"
            "☎️ +998 77 154 07 70\n"
        ),
        reply_markup=keyboard
    )

# ================= RARE =================

@dp.message(F.text == "🎓 RARE")
async def rare(message: Message):
    photo = FSInputFile("images/rare.jpg")  # rasm nomini shunday qo'ying

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌐 Rasmiy sayt", url="https://qarshistateuniversity.com")],
            [InlineKeyboardButton(text="📸 Instagram", url="https://instagram.com/rareeducation")],
            [InlineKeyboardButton(text="📍 Lokatsiya", url="https://maps.google.com/?q=Qarshi+State+University")]
        ]
    )

    await message.answer_photo(
        photo=photo,
        caption=(
            "🎓 Qarshi State University (RARE Education)\n\n"
            "🌍 MBBS dasturi (Ingliz tilida)\n"
            "🏥 WHO va NMC tomonidan tan olingan\n"
            "👨‍⚕️ Hindistonlik tajribali o‘qituvchilar\n"
            "🍽 Hind taomlari va yotoqxona mavjud\n"
            "💰 Arzon kontrakt va yashash xarajatlari\n\n"
            "📞 Aloqa: +91 9953126603\n"
            "📧 Email: support@rareeducation.in\n\n"
            "⚡ Xavfsiz va zamonaviy ta’lim muhiti!"
        ),
        reply_markup=keyboard
    )


# ================= ROWE =================

@dp.message(F.text == "🛢 ROWE")
async def rowe(message: Message):
    photo = FSInputFile("images/rowe.jpg")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📸 Instagram", url="https://instagram.com/roweoiluzbekistan")],
            [InlineKeyboardButton(text="📲 Telegram", url="https://t.me/roweoiluzbekistan")]
        ]
    )

    await message.answer_photo(
        photo=photo,
        caption=(
            "🛢 ROWE Motor Oil\n\n"
            "🇩🇪 Eng ishonchli nemis brendi\n\n"
            "🔧 Motor moylari\n"
            "⚙️ MKPP / AKPP moylari\n"
            "❄️ Antifrizlar\n\n"
            "📞 Aloqa: +998 71 207 90 90\n"
            "📍 Toshkent, O‘zbekiston\n\n"
            "⚡ Yuqori sifat va ishonch!"
        ),
        reply_markup=keyboard
    )


# ================= AVTOMAKTAB =================

@dp.message(F.text == "🚘 AVTOMAKTAB")
async def avtomaktab(message: Message):
    photo = FSInputFile("images/avtomaktab.jpg")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📸 Instagram", url="https://instagram.com/avtomaktab_qarshii")],
            [InlineKeyboardButton(text="🌐 Sayt", url="https://taplink.cc/avtoinnovation_qarshi")],
            [InlineKeyboardButton(
                text="📍 Lokatsiya",
                url="https://maps.google.com/?q=Amir+Temur+ko'chasi+43A+Qarshi"
            )]
        ]
    )

    await message.answer_photo(
        photo=photo,
        caption=(
            "🚗 Innovatsion Avto Maktab | Qarshi\n\n"
            "📚 Haydovchilik guvohnomasini olish oson!\n\n"
            "💳 Bo‘lib to‘lash imkoniyati mavjud\n"
            "📋 Toifalar: A, B, C, E, D, BC\n\n"
            "📞 Aloqa: +998 90 244 11 11\n"
            "📍 Manzil: Amir Temur ko‘chasi, 43A (Qarshi)\n\n"
            "⚡ Tez, sifatli va ishonchli ta’lim!"
        ),
        reply_markup=keyboard
    )

# ================= CHERY =================

@dp.message(F.text == "🚗 CHERY")
async def chery(message: Message):
    photo = FSInputFile("images/chery.jpg")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📸 Instagram", url="https://instagram.com/chery.qarshi")],
            [InlineKeyboardButton(text="🌐 Rasmiy sayt", url="https://chery-aster.uz/")],
            [InlineKeyboardButton(
                text="📍 Lokatsiya",
                url="https://maps.app.goo.gl/Lj6jHgLe6UaxbGeb6"
            )]
        ]
    )

    await message.answer_photo(
        photo=photo,
        caption=(
            "🚘 CHERY Qarshi | ADM-ASTER\n\n"
            "🇺🇿 O‘zbekistondagi rasmiy diler\n\n"
            "🚗 Avtomobillar savdosi va servis xizmati\n\n"
            "✅ 5 yil / 150 000 km kafolat\n"
            "💳 Foizsiz muddatli to‘lov\n"
            "🏦 Kredit asosida xarid qilish imkoniyati\n\n"
            "📞 Aloqa: +998 55 516 22 11\n"
            "📍 Manzil: To‘qmang‘it MFY, Qarshi\n\n"
            "🔥 Zamonaviy va ishonchli avtomobillar!"
        ),
        reply_markup=keyboard
    )


# ================= AVTOMAKTAB =================

@dp.message(F.text == "💒 TURON")
async def turon(message: Message):
    photo = FSInputFile("images/turon.jpg")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📸 Instagram", url="https://instagram.com/turon_tuyxona")],
            [InlineKeyboardButton(
                text="📍 Lokatsiya",
                url="https://maps.app.goo.gl/bREDqQGHxjmr64cv8"
            )]
        ]
    )

    await message.answer_photo(
        photo=photo,
        caption=(
            "🏛 Wedding Hall \"TURON\"\n\n"
            "💎 Premium to‘yxona\n\n"
            "👑 2 ta VIP kabina mavjud\n"
            "👥 600 tagacha mehmon sig‘imi\n"
            "🍽 Catering xizmati mavjud\n\n"
            "📞 Aloqa: +998 94 790 88 88\n"
            "📍 Manzil: Qarshi shahri\n\n"
            "✨ To‘y va tadbirlaringiz uchun ideal maskan!"
        ),
        reply_markup=keyboard
    )


# ================= F-MART =================

@dp.message(F.text == "🛒 F-MART")
async def fmart(message: Message):
    photo = FSInputFile("images/fmart.jpg")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📸 Instagram", url="https://instagram.com/f_mart_supermarket")],
            [InlineKeyboardButton(
                text="📍 Lokatsiya",
                url="https://maps.google.com/?q=Qarshi+4-mkr+11-maktab"
            )]
        ]
    )

    await message.answer_photo(
        photo=photo,
        caption=(
            "🛒 F-MART SUPERMARKET | QARSHI\n\n"
            "📍 4-mkr, 11-maktab qarshisida\n\n"
            "🛍 Hamyonbop narxlar\n"
            "📦 Keng assortiment\n"
            "✨ Yangi va sifatli mahsulotlar\n\n"
            "🤝 Ishonch va halollik – bizning tamoyil\n\n"
            "📞 Tel: 55 406 42 55"
        ),
        reply_markup=keyboard
    )


# ================= OZODBEK =================

@dp.message(F.text == "🎤 OZODBEK")
async def ozodbek(message: Message):
    photo = FSInputFile("images/ozodbek.jpg")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📸 Instagram", url="https://instagram.com/ozodbekabduxoliqov_oficial")],
            [InlineKeyboardButton(text="▶️ YouTube", url="https://youtube.com")],
        ]
    )

    await message.answer_photo(
        photo=photo,
        caption=(
            "🎤 Ozodbek Abduxoliqov | Singer\n\n"
            "🎉 To‘y va tadbirlar uchun professional xizmat\n"
            "🎶 Jonli ijro va yuqori darajadagi dastur\n\n"
            "📞 Aloqa:\n"
            "+998 20 026 88 58\n"
            "+998 88 206 88 58\n\n"
            "✨ Sizning bayramingiz — bizning mas’uliyat!"
        ),
        reply_markup=keyboard
    )

# ================= EMIRAN =================
@dp.message(F.text == "👕 EMIRAN")
async def emiran(message: Message):
    photo = FSInputFile("images/emiran.jpg")  # rasm nomini shunaqa qilib qo‘ying

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="📸 Instagram",
                url="https://instagram.com/emiran_qarshi_atlas"
            )],
            [InlineKeyboardButton(
                text="📍 Lokatsiya",
                url="https://maps.google.com/?q=Qarshi+Atlas+Savdo+Markazi"
            )]
        ]
    )

    await message.answer_photo(
        photo=photo,
        caption=(
            "👕 EMIRAN | ERKAKLAR KIYIM DO‘KONI\n\n"
            "📍 Qarshi Atlas Savdo Markazi\n\n"
            "👔 Erkaklar uchun zamonaviy kiyimlar\n"
            "✨ Sifat va stil bir joyda\n\n"
            "🕘 Ish vaqti: 09:00 - 23:00\n\n"
            "🚚 Dastafka xizmati mavjud\n"
            "📞 Tel: +998888300698"
        ),
        reply_markup=keyboard
    )

# ================= ORQAGA =================
@dp.message(F.text == "⬅️ Orqaga")
async def back(message: Message):

    prev = user_history.get(message.from_user.id)

    # Tarifdan → Narxlarga
    if prev in ["gold", "silver", "platinum"]:
        user_history[message.from_user.id] = "narx"

        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🥇 Gold"), KeyboardButton(text="🥈 Silver")],
                [KeyboardButton(text="🥉 Platinum")],
                [KeyboardButton(text="⬅️ Orqaga")]
            ],
            resize_keyboard=True
        )

        await message.answer("💰 Tarifni tanlang 👇", reply_markup=keyboard)
        return

    # Narxlardan → Menu
    if prev == "narx":
        user_history[message.from_user.id] = "menu"
        await message.answer("🏠 Menu", reply_markup=menu_btn)
        return

    # Default (boshqa joylardan)
    user_history[message.from_user.id] = "menu"
    await message.answer("🏠 Menu", reply_markup=menu_btn)

# ================= RUN =================
async def main():
    asyncio.create_task(start_web_app())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())