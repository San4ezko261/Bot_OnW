from aiogram import Bot, Dispatcher, types, executor
from aiogram.utils.exceptions import MessageToDeleteNotFound
from config import TOKEN_API

from keyboards import ikb, ikb2, ikb3, ikb4, ikb5
import os
import random
import asyncio
from datetime import datetime, timedelta

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)
# Список фотографий
signal_photos = [
    'images/signal1.jpeg',
    'images/signal2.jpeg',
    'images/signal3.jpeg',
    'images/signal4.jpeg',
    'images/signal5.jpg',
    'images/signal6.jpg',
    'images/signal7.jpg',
    'images/signal8.jpg',
    'images/signal9.jpg',
    'images/signal10.jpg',
    'images/signal11.jpg',
    'images/signal12.jpg',
    'images/signal13.jpg',
    'images/signal14.jpg'
]
# Словарь для хранения данных о пользователях
user_signals = {}

async def on_startup(_):
    print('I have been started up!')

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    photo_path = os.path.join('images', 'start.jpg')
    caption_text = (
        'Привет, ты попал в бота с бесплатными сигналами Mines💣\n\n'
        'Для получения доступа тебе необходимо пройти регистрацию по ссылке ниже, используя промокод "fluxy"🔘\n\n'
        'Очень важно зарегистрироваться с нового аккаунта по нашей ссылке и промокоду. Так вы свяжете игровой аккаунт 1win и этого бота, чтобы получать сигналы КОНКРЕТНО ПОД ВАС в реальном времени.\n\n'
        'Бот основан на нейросети от OpenAI. Точность бота - 92%'
    )
    await bot.send_photo(chat_id=message.chat.id, photo=open(photo_path, 'rb'), caption=caption_text, reply_markup=ikb)
    try:
        await message.delete()
    except MessageToDeleteNotFound:
        print("Сообщение уже удалено или не найдено.")

@dp.callback_query_handler(lambda call: True)
async def callback_query_handler(call: types.CallbackQuery):
    try:
        await call.message.delete()
    except MessageToDeleteNotFound:
        print("Сообщение уже удалено или не найдено.")
    if call.data == "registr":
        register_photo_path = os.path.join('images', 'register.jpg')
        register_text = (
            "Регистрация\n\n"
            "1. Заходим на официальный сайт 1win по ссылке: https://1wzvro.top/casino/list?open=register&p=e9yp (единственная ссылка на официальный сайт 1win).\n\n"
            "❗ОБЯЗАТЕЛЬНО НУЖЕН НОВЫЙ АККАУНТ❗\n\n"
            "При регистрации вводим промокод \"fluxy\"\n\n"
            "2. После успешной регистрации скопируйте ваш ID на сайте (Вкладка \"пополнение\" и в правом верхнем углу будет ваш ID).\n\n"
            "3. Отправьте ID боту в ответ на данное сообщение. ТОЛЬКО ЦИФРЫ!"
        )
        await bot.send_photo(chat_id=call.from_user.id, photo=open(register_photo_path, 'rb'), caption=register_text, reply_markup=ikb2)
        await call.message.answer("Пожалуйста, введите ваш ID:")
    elif call.data == "instr":
        instruction_text = (
            "Бот основан и обучен на кластере нейросети 🖥\n\n"
            "Для тренировки бота было сыграно 🎰 10.000+ игр.\n\n"
            "На текущий момент пользователи бота успешно делают в день 15-25% от своего 💸 капитала!\n\n"
            "Точность бота составляет 92%!\n\n"
            "Для получения максимального профита следуйте следующей инструкции:\n\n"
            "🟢 1. Пройти регистрацию в букмекерской конторе 1WIN\n\n"
            "❗ОБЯЗАТЕЛЬНО НУЖНО СОЗДАТЬ НОВЫЙ АККАУНТ❗\n\n"
            "Официальный сайт 1win: https://1wzvro.top/casino/list?open=register&p=e9yp\n\n"
            "При регистрации вводим промокод \"fluxy\"\n\n"
            "Если не открывается - заходим с включенным VPN (Швеция). В Play Market/App Store полно бесплатных сервисов, например: Vpnify, Planet VPN, Hotspot VPN и так далее!\n\n"
            "Без регистрации доступ к сигналам не будет открыт!\n\n"
            "❗При регистрации вводим промокод \"fluxy\"❗\n\n"
            "🟢 2. Пополнить баланс своего аккаунта.\n\n"
            "🟢 3. Перейти в раздел 1win games и выбрать игру 💣 'MINES'.\n\n"
            "🟢 4. Выставить кол-во ловушек в зависимости от сигнала. Это важно!\n\n"
            "🟢 5. Запросить сигнал в боте и ставить.\n\n"
            "🟢 6. При неудачном сигнале советуем удвоить(Х²) ставку чтобы полностью перекрыть потерю при следующем сигнале."
        )
        await bot.send_message(chat_id=call.from_user.id, text=instruction_text, reply_markup=ikb2)
    elif call.data == "menu":
        await start_command(call.message)
    elif call.data == "signal":
        user_id = call.from_user.id
        current_time = datetime.now()
        # Проверка на наличие пользователя в словаре
        if user_id not in user_signals:
            user_signals[user_id] = {
                'last_request_time': current_time,
                'signal_count': 0
            }
        user_data = user_signals[user_id]
        # Проверка времени последнего запроса
        if current_time - user_data['last_request_time'] >= timedelta(hours=12):
            user_data['last_request_time'] = current_time
            user_data['signal_count'] = 0
        if user_data['signal_count'] < 5:
            user_data['signal_count'] += 1
            await handle_signal_request(call, user_id)
        else:
            # Вычисление времени ожидания
            time_remaining = timedelta(hours=12) - (current_time - user_data['last_request_time'])
            hours_remaining, minutes_remaining = divmod(time_remaining.total_seconds() // 60, 60)
            await call.message.answer(
                f"Вы достигли лимита в 5 сигналов за 12 часов. Пожалуйста, подождите еще {int(hours_remaining)} часов и {int(minutes_remaining)} минут.", reply_markup=ikb5)

    await call.answer()

async def handle_signal_request(call: types.CallbackQuery, user_id: int):
    session_number = random.randint(10000, 99999)  # Генерация случайного пятизначного числа
    current_date = datetime.now().strftime("%d.%m.%Y")  # Получение текущей даты в формате ДД.ММ.ГГГГ
    # Форматируем сообщение
    signal_message = (
        f"Бот получает сигнал для игрока {user_id}\n\n"
        f"Сессия #{session_number}\n"
        f"{current_date}"
    )
    await call.message.answer(signal_message)
    # Задержка 2 секунды
    await asyncio.sleep(2)
    # Генерация случайных значений для описания
    game_number = random.randint(1000, 9999)  # Случайное 4-значное число
    chance = round(random.uniform(92.0, 98.0), 2)  # Случайное вещественное число от 92% до 98%
    traps_count = random.choice([1, 3, 5])  # Случайное число от 2 до 4
    # Формируем описание
    description = (
        f"Игра Mines #{game_number}\n"
        f"Шанс - {chance}%\n"
        f"Кол-во ловушек - {traps_count}"
    )
    # Выбор случайного фото из списка
    photo_path = random.choice(signal_photos)
    # Отправка случайного фото с описанием
    if os.path.isfile(photo_path):
        await bot.send_photo(chat_id=user_id, photo=open(photo_path, 'rb'), caption=description, reply_markup=ikb5)
    else:
        await call.message.answer("Ошибка: изображение не найдено.")

@dp.message_handler(lambda message: message.chat.id == message.from_user.id)
async def get_user_id(message: types.Message):
    user_id = message.text.strip()
    if len(user_id) == 8 and user_id[0] == '9' and user_id.isdigit():
        await message.answer("Поздравляем! Доступ активирован ✅", reply_markup=ikb4)
    else:
        await message.answer("Некорректное значение ID. Попробуйте ещё раз!", reply_markup=ikb3)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
