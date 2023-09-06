from setting.conf import TG_TOKEN, admin_chat_id, options
from db import get_db_users, update_db_user, remove_db_user
from aiogram import executor
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
import traceback
import logging


bot = Bot(TG_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class DialogStates(StatesGroup):
    WaitingForReg = State()
    WaitingForResume = State()
    
    
class DialogBayerState(StatesGroup):
    WaitingForAnswer = State()


@dp.message_handler(lambda message: message.text == "Відгук на спец позицію з доп питаннями")
async def response_bayer(message):
    await message.answer("Доброго дня! Оберіть потрібний варіант:", 
                        reply_markup=types.ReplyKeyboardMarkup(
                        resize_keyboard=True
                        ).add(*[types.KeyboardButton(label) 
                        for label in options.keys()]).add(
                        types.KeyboardButton("Головна")))


    await DialogBayerState.WaitingForAnswer.set()


@dp.message_handler(lambda message: message.text == "Головна", state=DialogBayerState.WaitingForAnswer)
async def handle_option_selection(message: types.Message, state: FSMContext):
    await state.finish()
    await start(message)


@dp.message_handler(lambda message: message.text in options.keys(), state=DialogBayerState.WaitingForAnswer)
async def handle_option_selection(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['current_option'] = message.text
        data['current_question_index'] = 0
        data['answers'] = []

    await process_answer(message, state)


@dp.message_handler(state=DialogBayerState.WaitingForAnswer)
async def process_answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['answers'].append(message.text)

        if data['current_question_index'] < len(options[data['current_option']]):
            data['current_question_index'] += 1
            await send_question(message, state)
        else:
            await update_db_user(message.chat.id, dict(zip(options[data['answers'][0]], data['answers'][1:])))
            await message.answer(f"Дякуємо за твій відгук! Зовсім скоро ми вийдемо до тебе на зв'язок 😉\nДо зустрічі 👋")
            await state.finish()
            await send_answers_to_admin(message.chat.id)
            await start(message)

async def send_question(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await message.answer(options[data['current_option']][data['current_question_index']])
        await DialogBayerState.WaitingForAnswer.set()


@dp.message_handler(state=DialogStates.WaitingForReg)
async def save_reg(message):
    await update_db_user(message.chat.id, {"reg": message.text})
    await DialogStates.WaitingForResume.set()
    await bot.send_message(message.chat.id, "Надішліть своє резюме в форматі файлу або фото:")
        

@dp.message_handler(state=DialogStates.WaitingForResume, content_types=types.ContentTypes.DOCUMENT | types.ContentTypes.PHOTO)
async def save_resume(message, state: FSMContext):
    if message.document:
        await update_db_user(message.chat.id, {"resume": message.document.file_id})
    elif message.photo:
        await update_db_user(message.chat.id, {"resume": message.photo[-1].file_id})

    await state.finish()
    await start(message, "Дякуємо! А тепер, будь ласка, обери вакансію в меню нижче")


@dp.message_handler(state=DialogStates.WaitingForResume, content_types=types.ContentTypes.TEXT)
async def save_resume_ERRORS(message):
    await DialogStates.WaitingForResume.set()
    await bot.send_message(message.chat.id, "Будь ласка, надішліть резюме у форматі файлу або фото:")


async def send_answers_to_admin(telegram_id):
    users = await get_db_users()
    await bot.send_message(admin_chat_id, users[str(telegram_id)]["reg"] + "\n" + "\n".join([f"{key}: {value}" for key, value in users[str(telegram_id)].items() if key not in ['reg']]))
    try:
        await bot.send_document(admin_chat_id, users[str(telegram_id)]['resume'])
    except:
        try:
            await bot.send_photo(admin_chat_id, users[str(telegram_id)]['resume'])
        except:
            await bot.send_message(admin_chat_id, "Неправильний формат резюме")


@dp.message_handler(lambda message: message.text in ["Головна", "/start"])
async def start(message, message_text = "Доброго дня! Оберіть потрібний варіант:"):
    users = await get_db_users()
    await update_db_user(message.chat.id, {"telegram_username": message.chat.username})

    if str(message.chat.id) in users:
        if "reg" in users[str(message.chat.id)] and "resume" in users[str(message.chat.id)]:        
            await message.answer(message_text, 
                                reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton("Профіль"), 
                                    types.KeyboardButton("Відгук на спец позицію з доп питаннями"), 
                                    types.KeyboardButton("Звичайний відгук"), 
                                    types.KeyboardButton("Переглянути активні вакансії")
                                    ))
        else:
            await message.answer("Привіт, ти звернувся/звернулась в компанію компанія \n" \
                            "Дякуємо тобі за твою зацікавленість до нашої компанії. Ми будемо вдячні за твоє резюме, але, \n" \
                            "спочатку заповни 'Профіль' та надішли або обери вакансію яка тебе зацікавила. \n" \
                            "Дякуємо!\n" \
                            "імя, Рекрутер компанія", reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton("Профіль")))
    else:
        await message.answer("Привіт, ти звернувся/звернулась в компанію компанія \n" \
                            "Дякуємо тобі за твою зацікавленість до нашої компанії. Ми будемо вдячні за твоє резюме, але, \n" \
                            "спочатку заповни 'Профіль' та надішли або обери вакансію яка тебе зацікавила. \n" \
                            "Дякуємо!\n" \
                            "імя, Рекрутер компанія", reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton("Профіль")))
        

@dp.message_handler(lambda message: message.text == "Профіль")
async def get_info(message):
    users = await get_db_users()
    if "reg" in users[str(message.chat.id)] and "resume" in users[str(message.chat.id)]:
        await bot.send_message(message.chat.id, users[str(message.chat.id)]["reg"] + "\n" + "\n".join([f"{key}: {value}" for key, value in users[str(message.chat.id)].items() if key not in ['reg']]),
                                reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton("Редагувати профіль"), 
                                                                                                 types.KeyboardButton("Головна")))
        
        try:
            await bot.send_document(message.chat.id, users[str(message.chat.id)]['resume'])
            return
        except:
            try:
                await bot.send_photo(message.chat.id, users[str(message.chat.id)]['resume'])
                return
            except:
                await bot.send_message(message.chat.id, "Неправильний формат резюме")
                return
    else:
        await register(message)


@dp.message_handler(lambda message: message.text in ["Редагувати профіль"])
async def register(message):
    await remove_db_user(message.chat.id)
    await message.answer("Будь ласка, надай свої дані, для того, щоб ми могли пошвидше зв'язатись з тобою 📲\n" \
                        "1. Ім'я та прізвище\n" \
                        "2. Твоя пошта для зв'язку\n" \
                        "3. Твій телеграм для зв'язку\n" \
                        "4. Твоя локація\n" \
                        "5. Ресурс де знайшов/ла нас.")
    await DialogStates.WaitingForReg.set()


@dp.message_handler(lambda message: message.text == "Звичайний відгук")
async def response_other(message):
    await message.answer("Дякуємо за твій відгук! Сподіваємось що ти знайшов/ла цікаву для себе пропозицію. Вже чекаємо на зустріч з тобою 🖤")
    await message.answer("Переходь за посиланням та дізнавайся які ще пропозиції в нас є для тебе - сайт")
    await send_answers_to_admin(message.chat.id)
    await start(message)


@dp.message_handler(lambda message: message.text == "Переглянути активні вакансії")
async def view_vacancies(message):
    await message.answer("Слідкуй за актуальними вакансіями за посиланням - сайт")
    await start(message)


while True:
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
        error_text = "Error: {}\n{}".format(str(e), traceback.format_exc())
        logging.error(error_text)
        bot = Bot(TG_TOKEN)
        storage = MemoryStorage()
        dp = Dispatcher(bot, storage=storage)
        print(e)
