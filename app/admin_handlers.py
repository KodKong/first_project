from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State 
from aiogram.fsm.context import FSMContext
from app.store import get_points_price_list
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

# Клавиатуры 

@router_admin.message(Command('first_admin_panel'))
async def show_first_admin_button(message: Message, state: FSMContext): 
   try: 
      if str(message.from_user.id) == FIRST_ADMIN_CHAT_ID: 
         await state.clear()
         await message.answer('Здарова отец', reply_markup = kb.buttons_for_first_admin)
   except: 
      await message.answer('Произошла ошибка')

@router_admin.message(Command('admin_panel'))
async def show_admin_button(message: Message, state: FSMContext): 
    if str(message.from_user.id) in ADMINS_CHAT_ID: 
        await state.clear()
        await message.answer('Привет, прочти инструкцию по эксплуатации перед использованием', reply_markup = kb.buttons_for_first_admin)
    else: 
        await message.answer('Я вас не понимаю')

# Добавить точку 

@router_admin.callback_query(F.data == 'add_shop')
async def start_adding_shop(callback: CallbackQuery, state: FSMContext): 
   await state.set_state(Adding_Obj.name_category)
   await callback.message.answer('Напишите адрес новой точки')

@router_admin.message(Adding_Obj.name_category)
async def start_adding_model(message: Message, state: FSMContext):
   await state.update_data(name_category = message.text) # Адрес точки 
   await state.set_state(Adding_Obj.name_brand)
   await message.answer('Напиши идентификатор телеграмма магазина')

@router_admin.message(Adding_Obj.name_brand)
async def adding_model_step(message: Message, state: FSMContext):
   await state.update_data(name_brand = message.text) # Идентификатор ТГ точки
   await state.set_state(Adding_Obj.name_model)
   await message.answer('Напиши Сбис ИД точки')

@router_admin.message(Adding_Obj.name_model)
async def add_model(message: Message, state: FSMContext):
   await state.update_data(name_model = message.text) # Идентификатор Сбис точки
   data_state = await state.get_data()
   await rq.create_new_shop(data_state['name_category'], data_state['name_brand'], data_state['name_model'])
   await state.clear()
   await message.answer('Точка успешно добавлена')
   
# Удалить точку 

@router_admin.callback_query(F.data == 'delete_shop')
async def start_deleting_shop(callback: CallbackQuery):
   await callback.message.answer('Выберите магазин', reply_markup = await kb.delete_shop_list_keyboard())

@router_admin.callback_query(F.data.startswith('delete_shop_1'))
async def start_deleting_shop_1(callback: CallbackQuery):
   await rq.delete_shop(callback.data.split('_')[3])
   await callback.message.answer('Точка успешно удалена')


# Обновление прайс листов

@router_admin.callback_query(F.data == 'update_price_list')
async def update_price_lists(callback: CallbackQuery):
    current_list_shops = await rq.get_shop_list()
    message = ''
    for shop_id in current_list_shops:
      price_lists = await get_points_price_list(shop_id.sbys_id)
      try:
         if price_lists['priceLists'][0]['id'] is not None: 
            await rq.update_price_list(str(shop_id.sbys_id), str(price_lists['priceLists'][0]['id']))
            message = message + f'\n Обновили прайс лист для {str(shop_id.address)}'
      except: 
         message = message + f'\n не удалось обновить прайс для {str(shop_id.address)}' 
    await callback.message.answer(str(message))
   
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

# Удаление категории 

@router_admin.callback_query(F.data == 'delete_category')
async def start_delete_model(callback: CallbackQuery):
   await callback.message.answer('Выберите категорию', reply_markup = await kb.delete_category_keyboard())

@router_admin.callback_query(F.data.startswith('delete_category_1'))
async def start_delete_model(callback: CallbackQuery):
   await rq.delete_category(callback.data.split('_')[3])
   await callback.message.answer('Категория успешно удалена')

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

# Удаление бренда 

@router_admin.callback_query(F.data == 'delete_brand')
async def start_delete_brand(callback: CallbackQuery):
   await callback.message.answer('Выберите категорию', reply_markup = await kb.delete_category_for_brand_list_keyboard())

@router_admin.callback_query(F.data.startswith('delete_brand_1'))
async def start_delete_brand(callback: CallbackQuery):
   await callback.message.answer('Выберите бренд, который необходимо удалить', reply_markup = await kb.delete_brand_list_keyboard(callback.data.split('_')[3]))

@router_admin.callback_query(F.data.startswith('delete_brand_2'))
async def adding_delete_step(callback: CallbackQuery):
   await rq.delete_brand(callback.data.split('_')[3])
   await callback.message.answer('Бренд успешно удален со всеми моделями')

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
   await message.answer('Модель успешно добавлена')
   await state.clear()

# Удаление модели 

@router_admin.callback_query(F.data == 'delete_model')
async def start_delete_model(callback: CallbackQuery):
   await callback.message.answer('Выберите категорию', reply_markup = await kb.delete_category_for_model_list_keyboard())

@router_admin.callback_query(F.data.startswith('delete_model_1'))
async def start_delete_model(callback: CallbackQuery):
   await callback.message.answer('Выберите бренд', reply_markup = await kb.delete_brand_for_model_list_keyboard(callback.data.split('_')[3]))

@router_admin.callback_query(F.data.startswith('delete_model_2'))
async def adding_delete_step(callback: CallbackQuery, state: FSMContext):
   await callback.message.answer('Выберите модель, которую необходимо удалить', reply_markup = await kb.delete_model_list_keyboard(callback.data.split('_')[3]))

@router_admin.callback_query(F.data.startswith('delete_model_3'))
async def adding_delete_step(callback: CallbackQuery):
   await rq.delete_model(callback.data.split('_')[3])
   await callback.message.answer('Модель успешно удалена')

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

# Оповещение магазина о истечении срока брони 

async def notification_timer(id_shop: str, position: str):
   try: 
      tg_id_shops = await rq.get_shop_by_id(str(id_shop))
      for i in tg_id_shops:
         await bot.send_message(chat_id = str(i.tg_id), text = f'Срок бронирования на {position} истек')
   except: 
      await print('error')

