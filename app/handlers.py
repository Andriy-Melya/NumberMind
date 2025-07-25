import asyncio

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

import app.game
import app.keyboards as kb
import os
import text

router = Router()

is_challenge = True
name_challenge = '1-1-1-0-0-0-0-0'


class GameStates(StatesGroup):
    choosing_length = State()
    playing = State()
    create_ch = State()


async def delete_message_sleep(message: Message):
    await asyncio.sleep(3)
    try:
        await message.delete()
    except:
        pass


async def save_winner(username, name, tl_name=''):
    file_name = f'winners_{name}.txt'
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            lines = file.readlines()
            count = len(lines)
    except FileNotFoundError:
        count = 0
    with open(file_name, "a", encoding="utf-8") as file:
        file.write(f"{count + 1}. {username}; нік в телеграм - @{tl_name}\n")


@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(text.st, reply_markup=kb.play_keyboard)


@router.message(Command('admin'))
async def cmd_start(message: Message):
    if message.from_user.id == 1154874808:
        await message.answer(text.st, reply_markup=kb.admin_menu_keyboard)
    else:
        return


@router.callback_query(F.data == 'play_game')
async def start_game(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    length = data.get("length", 3)
    num = app.game.set_number(length)
    await state.update_data(secret_number=num, attempts=0, length=length)

    await callback.message.answer(f"🎲 Я загадав секретний код довжиною\n{length} {'символів' if length > 4 else 'символи'}, спробуй відгадати",
                                  reply_markup=ReplyKeyboardRemove())
    await state.set_state(GameStates.playing)


@router.callback_query(F.data == 'settings')
async def settings(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    length = data.get("length", 3)
    await callback.message.answer(
        f"🔢 Встановленна складність {length}-{'символів' if length > 4 else 'символи'}. \nМожете змінити складність гри (кількість цифр):",
        reply_markup=kb.setting_keyboard)
    await state.set_state(GameStates.choosing_length)


@router.callback_query(F.data == 'help')
async def start_game(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text.hp, reply_markup=kb.play_keyboard)


@router.callback_query(F.data == 'challenge')
async def start_game(callback: CallbackQuery, state: FSMContext):
    if is_challenge:
        data = await state.get_data()
        ch = data.get("task", '')
        if ch == '':
            await callback.message.answer(text.challenge_YES(name_challenge), reply_markup=kb.challenge_keyboard)
        else:
            await callback.message.answer(text.challenge_YES(name_challenge), reply_markup=kb.main_challenge_keyboard)
    else:
        await callback.message.answer(text.challenge_NO, reply_markup=kb.play_keyboard)


@router.callback_query(F.data == 'result_challenge')
async def start_game(callback: CallbackQuery, state: FSMContext):
    global name_challenge
    data = await state.get_data()
    ch_res = data.get("challenge_res", [])
    ch = name_challenge.split('-')
    s = '🧠 Ти відгадав:'
    if len(ch_res) == 0:
        return
    for i in range(2, 10):
        s += f"\n🔢 {i}-цифрових кодів:  {ch_res[i]} з {ch[i - 2]}"
    await callback.message.answer(
        s + "\n\n🏆 Якщо впораєшся — потрапиш у таблицю переможців! Запиши своє ім’я в історію NumberMind 💥",
        reply_markup=kb.play_keyboard)


@router.callback_query(F.data == 'start_challenge')
async def start_game(callback: CallbackQuery, state: FSMContext):
    ch_res = [0] * 10
    await state.update_data(challenge_res=ch_res, task=name_challenge)
    await callback.message.answer('Челендж розпочато! Бажаю успіху', reply_markup=kb.play_keyboard)


@router.callback_query(F.data == 'exit_challenge')
async def challenge_exit(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text('Ви покинули челендж', reply_markup=kb.play_keyboard)


@router.callback_query(F.data == 'table_result')
async def print_table(callback: CallbackQuery, state: FSMContext):
    global name_challenge
    file_name = f'winners_{name_challenge}.txt'
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            lines = ''.join(file.readlines())
    except FileNotFoundError:
        lines = 'Чекаємо на переможців.'
    await callback.message.answer(lines, reply_markup=kb.play_keyboard)


@router.callback_query(F.data == 'create_challenge')
async def create_challenge(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введи складність челенджу')
    await state.set_state(GameStates.create_ch)


@router.callback_query(F.data == 'EXIT_challenge')
async def start_game(callback: CallbackQuery, state: FSMContext):
    global is_challenge, name_challenge
    await callback.message.answer('Челендж завершено')
    is_challenge = False
    name_challenge = ''


@router.callback_query(F.data == 'table_result_zero')
async def table_result_zero(callback: CallbackQuery, state: FSMContext):
    global name_challenge
    file_name = f'winners_{name_challenge}.txt'
    try:
        os.remove(file_name)
        await callback.message.answer(f"Таблицю результатів {file_name} успішно видалено.")
    except FileNotFoundError:
        await callback.message.answer(f"Таблицю результатів {file_name} не знайдено.")
    except Exception as e:
        await callback.message.answer(f"Сталася помилка при видаленні: {e}")


@router.message(GameStates.choosing_length)
async def process_setting(message: Message, state: FSMContext):
    try:
        guess = int(message.text.strip())
    except ValueError:
        await message.answer('Виберіть складність гри (кількість цифр у коді) від 2 до 9',
                             reply_markup=kb.setting_keyboard)
        return
    if 2 <= guess <= 9:
        await state.update_data(length=int(guess))
        await message.answer(f"Складність гри встановленна - {guess} {'символів' if guess > 4 else 'символи'}",
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state(None)
        await message.answer("Готовий зіграти з тобою у гру «Бики та корови» 🧠🔢", reply_markup=kb.play_keyboard)
    else:
        await message.answer('Виберіть складність гри (кількість цифр у коді) від 2 до 9',
                             reply_markup=kb.setting_keyboard)


@router.message(GameStates.playing)
async def process_guess_one(message: Message, state: FSMContext):
    guess = message.text.strip()
    if guess == '0':
        await message.delete()
        await message.answer(text.exit, reply_markup=kb.play_keyboard)
        await state.set_state(None)
        return

    data = await state.get_data()
    N = data["length"]
    if not app.game.is_norm(guess, N):
        await message.delete()
        msg = await message.answer("Помилка вводу, спробуй ще раз", reply_markup=ReplyKeyboardRemove())
        asyncio.create_task(delete_message_sleep(msg))
        return
    secret = data["secret_number"]
    attempts = data["attempts"] + 1
    B, K = app.game.bulls_and_cows(secret, guess)
    if K == N:
        await message.answer(f"🎉 Вітаю! Ти вгадав число {secret} з {attempts}-го разу!", reply_markup=kb.play_keyboard)
        ch_res = data.get("challenge_res", [])
        if len(ch_res) != 0:
            ch_res[N] += 1
            await state.update_data(challenge_res=ch_res)
            ch = data["task"]
            ch_result = '-'.join(map(str, ch_res))[4:]
            if ch == ch_result:
                await save_winner(message.from_user.full_name, ch, message.from_user.username)
                await message.answer(f"Вітаю! Ти виконав умови челенджу і тебе внесено до таблиці результатів",
                                     reply_markup=kb.res_keyboard)
        await state.set_state(None)
        return
    await state.update_data(attempts=attempts)
    await message.delete()
    bot_message_id = await message.answer(f"{attempts}. {guess}  | {B}:{K}")


@router.message(GameStates.create_ch)
async def process_guess(message: Message, state: FSMContext):
    global is_challenge, name_challenge
    ch = message.text.strip().split('-')
    if len(ch) == 8:
        await message.answer('Все гаразд. Челендж встановленно')
        is_challenge = True
        name_challenge = message.text.strip()
        await state.clear()
    else:
        await message.answer('Щось пішло не так!')
        await state.clear()
