from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State 
from aiogram.fsm.context import FSMContext
from app.store import get_point_list
import app.keyboards.admin_keyboards as kb
from config import FIRST_ADMIN_CHAT_ID, ADMINS_CHAT_ID, TOKEN
import app.database.admin_requests as rq
from aiogram import Bot

bot = Bot(token = TOKEN)
router_admin = Router()

class Adding_Obj(StatesGroup):
    name_category = State()
    name_brand = State()
    name_model = State()
    parent = State()
    text_for_marketing = State()
    photo_for_marketing = State()


@router_admin.message(Command('first_admin_panel'))
async def show_first_admin_button(message: Message): 
   try: 
      if str(message.from_user.id) == FIRST_ADMIN_CHAT_ID: 
         await message.answer('Здарова отец', reply_markup = kb.buttons_for_first_admin)
   except: 
      await message.answer('Произошла ошибка')

@router_admin.message(Command('admin_panel'))
async def show_admin_button(message: Message, state: FSMContext): 
    if str(message.from_user.id) in ADMINS_CHAT_ID: 
        await message.answer('Привет, прочти инструкцию по эксплуатации перед использованием', reply_markup = kb.buttons_for_first_admin)
    else: 
        await message.answer('Я вас не понимаю')

@router_admin.callback_query(F.data == 'update_shop_list')
async def show_categories(callback: CallbackQuery):
    new_list_shops = get_point_list()
    current_list_shops = await rq.get_shop_list()
    new_shops = []
    for sbys_id in new_list_shops['salesPoints']:
        if sbys_id not in current_list_shops:
            new_shops.append(sbys_id)

# Добавление категории

@router_admin.callback_query(F.data == 'add_category')
async def start_adding_category(callback: CallbackQuery, state: FSMContext):
   await state.set_state(Adding_Obj.name_category)
   await callback.message.answer('Впишите наименование категории')

@router_admin.message(Adding_Obj.name_category)
async def add_category(message: Message, state: FSMContext):
   await state.update_data(name_category = message.text)
   data_state = await state.get_data()
   await rq.create_new_category(data_state['name_category'])
   await message.answer('Категория успешно добавлена')
   await state.clear()

# Добавление бренда

@router_admin.callback_query(F.data == 'add_brand')
async def start_adding_brand(callback: CallbackQuery):
   await callback.message.answer('Выберите категорию', reply_markup = await kb.category_list_keyboard())

@router_admin.callback_query(F.data.startswith('add_brand'))
async def adding_brand_step(callback: CallbackQuery, state: FSMContext):
   await state.update_data(parent = callback.data.split('_')[2])
   await state.set_state(Adding_Obj.name_brand)
   await callback.message.answer('Напишите наименование нового бренда')

@router_admin.message(Adding_Obj.name_brand)
async def add_brand(message: Message, state: FSMContext):
   await state.update_data(name_brand = message.text)
   data_state = await state.get_data()
   await rq.create_new_brand(data_state['name_brand'], data_state['parent'])
   await message.answer('Бренд успешно добавлен')
   await state.clear()

# Добавление модели

@router_admin.callback_query(F.data == 'add_model')
async def start_adding_model(callback: CallbackQuery):
   await callback.message.answer('Выберите категорию', reply_markup = await kb.category_for_model_list_keyboard())

@router_admin.callback_query(F.data.startswith('add_model_1'))
async def start_adding_model(callback: CallbackQuery):
   await callback.message.answer('Выберите бренд', reply_markup = await kb.brand_list_keyboard(callback.data.split('_')[3]))

@router_admin.callback_query(F.data.startswith('add_model_2'))
async def adding_model_step(callback: CallbackQuery, state: FSMContext):
   await state.update_data(parent = callback.data.split('_')[3])
   await state.set_state(Adding_Obj.name_model)
   await callback.message.answer('Напишите наименование нового модель')

@router_admin.message(Adding_Obj.name_model)
async def add_model(message: Message, state: FSMContext):
   await state.update_data(name_model = message.text)
   data_state = await state.get_data()
   await rq.create_new_model(data_state['name_model'], data_state['parent'])
   await state.clear()
   await message.answer('Модель успешно добавлен')
   await state.clear()

# Рассылка рекламы 

@router_admin.callback_query(F.data.startswith('create_marketing'))
async def add_marketing(callback: CallbackQuery, state: FSMContext):
   await state.set_state(Adding_Obj.text_for_marketing)
   await callback.message.answer('Напиши текст рекламы')

@router_admin.message(Adding_Obj.text_for_marketing)
async def add_marketing_text(message: Message, state: FSMContext):
   await state.update_data(text_for_marketing = message.text)
   await state.set_state(Adding_Obj.photo_for_marketing)
   await message.answer('Отправь фото')

@router_admin.message(Adding_Obj.photo_for_marketing)
async def add_marketing_photo(message: Message, state: FSMContext):
   await state.update_data(photo_for_marketing = message.photo[-1].file_id)
   data_state = await state.get_data()
   await bot.send_photo(chat_id = message.chat.id, caption=data_state['text_for_marketing'], photo = data_state['photo_for_marketing'], reply_markup = kb.buttons_for_marketing)

@router_admin.callback_query(F.data.startswith('approve_marketing'))
async def send_marketing(callback: CallbackQuery, state: FSMContext): 
   data_state = await state.get_data()
   clients = await rq.get_client_list()
   for client in clients: 
      await bot.send_photo(chat_id = client.tg_id, caption=data_state['text_for_marketing'], photo = data_state['photo_for_marketing'])
   await state.clear()

@router_admin.callback_query(F.data.startswith('reject_marketing'))
async def reject_marketing(callback: CallbackQuery, state: FSMContext): 
   await state.clear()
   await callback.message.answer('Рассылка отменена, введи команду /admin_panel, чтоб перейти к панели администратора')
   await state.clear()
   
# Узнать id аккаунта

@router_admin.message(Command('get_my_identificator'))
async def show_id_account(message: Message): 
    try:
        await message.answer(f'{message.from_user.id}')
    except Exception as err:
        await message.answer(str(err)) 

