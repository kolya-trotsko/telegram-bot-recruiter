import aiogram
from aiogram import Bot, Dispatcher, types
import json
from aiogram.utils import executor
from os import path
TOKEN = '1946562538:AAFfw_CFeOcDRfoLpQdLeWc_4-Y5zvsjh3A'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

status_name,status_home,status_delete,status_delete_goods,status_kategory,status_tovar,status_del_category,admin_status,status_delete_goods,status_add_goods_name,status_add_goods_price,status_add_goods_description,status_add_goods_category,status_buy,status_search = False,False,False,False,False,False,False,False,False,False,False,False,False,False,False
@dp.message_handler()
async def echo_message(message: types.Message):
    global status_name,status_home,status_kategory,cart,t,p,price,name,category_buy,delete_category,status_tovar,status_delete,status_delete_goods,new_good_name,status_del_category,new_good_category,admin_status,status_delete_goods,status_add_goods_name,status_add_goods_price,status_search,status_add_goods_description,status_add_goods_category,status_buy
    file = open(path.join(path.dirname(__file__),"data.json"),"r")
    dictionary = json.load(file)
    if "client" not in dictionary and "price" not in dictionary:
        file = open(path.join(path.dirname(__file__),"data.json"),"w")
        dictionary["client"] = {}
        dictionary["price"] = {}
        dictionary["price"]["category"] = {}
        


    if admin_status == True or message.text == '/admin':
        if message.text == '/admin':
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            result = ["категорія", "товар", "вийти"]
            keyboard.add(*result)
            await message.answer(f"Привіт, адміне✨\nВибери що хочеш зробити:", reply_markup=keyboard)
        admin_status = True
        if message.text == "На головну":
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            result = ["категорія", "товар", "вийти"]
            keyboard.add(*result)
            await message.answer(f"Привіт, адміне✨\nВибери що хочеш зробити:", reply_markup=keyboard)
        elif message.text == "вийти":
            admin_status = False
        elif message.text == "категорія":
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            result = ["показати категорії","додати категорію", "видалити категорію","На головну"]
            keyboard.add(*result)
            await message.answer("Обери що ти хочеш зробити з категорією:", reply_markup=keyboard)
        elif message.text == "показати категорії":
            result = []
            for category in dictionary["price"]["category"]:
                result.append(category)
            if result == []:
                await bot.send_message(message.from_user.id, "немає жодної створеної категорії")
            else:
                await bot.send_message(message.from_user.id, result)
        elif message.text == "додати категорію":
            await bot.send_message(message.from_user.id, "напишіть назву нової категорії")
            status_kategory = True
        elif message.text == "видалити категорію":
            if dictionary["price"]["category"] == {}:
                await bot.send_message(message.from_user.id, "немає жодної створеної категорії")
            else:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(*dictionary["price"]["category"])
                await message.answer(f"вибери категорію яку хочеш видалити", reply_markup=keyboard)
                status_del_category = True
        elif status_kategory == True:
            dictionary["price"]["category"][str(message.text)] = {}
            await bot.send_message(message.from_user.id, f"категорія {message.text} додана")
            status_kategory = False
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*["показати категорії","додати категорію", "видалити категорію","На головну"])
            await message.answer(f"Обери що ти хочеш зробити з категорією:", reply_markup=keyboard)
        elif status_del_category == True:
            if str(message.text) in dictionary["price"]["category"]:
                del dictionary["price"]["category"][str(message.text)]
                await bot.send_message(message.from_user.id, f"категорія {message.text} видалена")
            else:
                await bot.send_message(message.from_user.id, f"категорії {message.text} не знайдено")
            status_del_category = False
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*["показати категорії","додати категорію", "видалити категорію","На головну"])
            await message.answer(f"Обери що ти хочеш зробити з категорією:", reply_markup=keyboard)

###############################################################################################################

        elif message.text == "товар":
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*["додати товар","видалити товар","На головну"])
            await message.answer("Обери що ти хочеш зробити з товаром:", reply_markup=keyboard)
            #dictionary["price"]["goods"] = {}
            #dictionary["price"]
        elif message.text == "додати товар":
            if dictionary["price"]["category"] != {}:
                status_add_goods_category = True
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(*dictionary["price"]["category"])
                await message.answer("Обери категорію нового товару:", reply_markup=keyboard)
            else:
                await bot.send_message(message.from_user.id, "спочатку створи категорію:")
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(*["додати товар","видалити товар","На головну"])
                await message.answer("Обери що ти хочеш зробити з товаром:", reply_markup=keyboard)
            #await bot.send_message(message.from_user.id, "Обери категорію нового товару:")
        elif status_add_goods_category == True:
            status_add_goods_category = False
            new_good_category = str(message.text)
            await bot.send_message(message.from_user.id, "як буде називатися ваш товар?:")
            status_add_goods_name = True
        elif status_add_goods_name == True:
            dictionary["price"]["category"][new_good_category][str(message.text)]={}
            status_add_goods_name = False
            new_good_name = str(message.text)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*dictionary["price"]["category"])
            await message.answer("Опис нового товару:", reply_markup=keyboard)
            status_add_goods_description = True
        elif status_add_goods_description == True:
            status_add_goods_description = False
            dictionary["price"]["category"][new_good_category][new_good_name]["description"]=str(message.text)
            await bot.send_message(message.from_user.id, "а тепер ціна товару:")
            status_add_goods_price = True
        elif status_add_goods_price == True:
            status_add_goods_price = False
            dictionary["price"]["category"][new_good_category][new_good_name]["price"]=str(message.text)
            dictionary["price"]["category"][new_good_category][new_good_name]["category"]=str(new_good_category)
            await bot.send_message(message.from_user.id, "товар додано")
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*["додати товар","видалити товар","На головну"])
            await message.answer("Обери що ти хочеш зробити з товаром:", reply_markup=keyboard)

        elif message.text == "видалити товар":
            if dictionary["price"]["category"] != {}:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(*dictionary["price"]["category"])
                await message.answer("Обери категорію товару що бажаєш видалити", reply_markup=keyboard)
                status_delete = True
            else:
                await bot.send_message(message.from_user.id, "спочатку створіть категорію")
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(*["додати товар","видалити товар","На головну"])
                await message.answer("Обери що ти хочеш зробити з товаром:", reply_markup=keyboard)
        elif status_delete == True:
            status_delete = False
            if dictionary["price"]["category"][delete_category] != {}:
                delete_category = str(message.text)
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(*dictionary["price"]["category"][delete_category])
                await message.answer("Обери товар що бажаєш видалити", reply_markup=keyboard)
                status_delete_goods = True
            else:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(*["На головну"])
                await message.answer("хм.. в цій категорії ще нема жодного товару", reply_markup=keyboard)
        elif status_delete_goods == True:
            status_delete_goods = False
            if len(dictionary["price"]["category"][delete_category][str(message.text)]) <= 1:
                dictionary["price"]["category"][delete_category][str(message.text)] = {}
            else:
                del dictionary["price"]["category"][delete_category][str(message.text)]
            await bot.send_message(message.from_user.id, f"товар {str(message.text)} видалено")

    else:
        if message.text == '/home' or message.text == "Подивлюся ще":
            if str(message.from_user.id) in dictionary["client"]:
                for id in dictionary["client"]:
                    if id == str(message.from_user.id):
                        cart = dictionary["client"][id]["cart"]
                        price = int(dictionary["client"][id]["price"])
                        name = dictionary["client"][id]["name"]
                
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                result = []
                for i in dictionary["price"]["category"]:
                    result.append(i)
                result.append("Оплатити корзину")
                result.append("Очистити корзину")
                keyboard.add(*result)
                result = []
                status_home = True
                if cart != "":
                    await message.answer(f"Привіт, {name}✨\nТвоя корзина:\n{cart}\nЦіна: {price}\nобери категорію товару що хочеш придбати:", reply_markup=keyboard)
                else: 
                    await message.answer(f"Привіт, {name}✨\nТвоя корзина:\nпусто\nЦіна: {price}\nобери категорію товару що хочеш придбати:", reply_markup=keyboard)
            else:
                await bot.send_message(message.from_user.id, "давай для початку познайомимося\nнапиши /reg")
        elif message.text == "Очистити корзину":
            status_home = False
            dictionary["client"][str(message.from_user.id)]["cart"] = ""
            dictionary["client"][str(message.from_user.id)]["price"] = 0
            await bot.send_message(message.from_user.id, "корзина очищена, перейди в щоб обрати щось /home")
        elif message.text == "Оплатити корзину":
            status_home = False
            if cart == "":
                await bot.send_message(message.from_user.id, "корзина пуста, спочатку потрібно щось обрати в /home")
            else:
                await bot.send_message(message.from_user.id, "дякую за замовлення!\nскоро вам напише наш менеджер")
                await bot.send_message(367471403, f"Привіт!!!\nтам клієнт написав.. @{message.from_user.username} \n його замовлення: {cart},\nціною: {price}")
                await bot.send_message(337646093, f"Привіт!!!\nтам клієнт написав.. @{message.from_user.username} \n його замовлення: {cart},\nціною: {price}")
        elif status_home == True:
            if dictionary["price"]["category"][message.text] != {}:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                category_buy = str(message.text)
                keyboard.add(*dictionary["price"]["category"][message.text])
                await message.answer(f"Привіт, {name}✨\nОсь все що я знайшов з категорії: {message.text}", reply_markup=keyboard)
                status_home = False
                status_search = True
            else:
                await bot.send_message(message.from_user.id, "в цій категорії поки нічого немає, введи /home щоб перейти на головну")
        elif status_search == True:
            status_search = False
            d = dictionary["price"]["category"][category_buy][str(message.text)]["description"]
            p = int(dictionary["price"]["category"][category_buy][str(message.text)]["price"])
            t = str(message.text)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            category_buy = str(message.text)
            keyboard.add(*["Купляю","Подивлюся ще"])
            await message.answer(f"""
Назва: {t}
Категорія: {category_buy}
Опис: {d}
Ціна: {str(p)}""", reply_markup=keyboard)
            status_buy = True
        elif status_buy == True and str(message.text) == "Купляю":
            status_buy = False
            dictionary["client"][str(message.from_user.id)]["cart"] += t
            dictionary["client"][str(message.from_user.id)]["price"] += p
            await bot.send_message(message.from_user.id, "Додано до корзини! зайди в свій /home щоб переглянути")

        elif message.text == '/reg':
            await message.reply("Привіт...?\nЯк мені звертатись до тебе?")
            status_name = True

        elif message.text == '/save':
                await message.reply("Зміни збережено. Надішліть /home щоб перейти на головну")
                status_name = False

        elif status_name == True:
            await message.reply(f"ну тепер привіт, {message.text},\nякщо хочеш поміняти ім'я - напиши його ще раз.\nЯкщо все окей то натисни /save")  # <-- Here we get the name
            name = message.text
            price = 0
            cart = ''
            dictionary["client"][str(message.from_user.id)] = {"cart": cart, "price": price, "name": name}

        else:
            await bot.send_message(message.from_user.id, "Не розумію(\nнапиши /home щоб потрапити на головну сторінку\nабо /reg щоб зареєструватися")
    file = open(path.join(path.dirname(__file__),"data.json"),"w")
    json.dump(dictionary, file)
if __name__ == '__main__':
    executor.start_polling(dp)