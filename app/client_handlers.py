from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State 
from aiogram.fsm.context import FSMContext
from app.store import show_products
import app.keyboards.client_keyboards as kb
from config import WELCOME_PROPOSAL, CATEGORIES_CHOOSE, BRAND_CHOOSE, PRODUCT_CHOOSE, MODEL_CHOOSE, ORDER_FOR_SHOP, POSITIVE_ORDER, NEGARIVE_ORDER
import app.database.client_requests as rq
from config import TOKEN
from aiogram import Bot

router = Router()
bot = Bot(token = TOKEN)

class Order(StatesGroup):
    shop_id = State(),
    tg_id_client = State(),
    shop_tg_id = State(),
    shop_sbys_id = State(),
    price_list_id = State(),
    brand = State(),
    product = State()

@router.message(CommandStart())
async def show_shops(message: Message, state: FSMContext): 
    try:
        await rq.set_client(message.from_user.id)
        await state.update_data(tg_id_client = message.from_user.id)
        await message.answer(str(WELCOME_PROPOSAL), reply_markup = await kb.shop_list_keyboard())
    except: 
        await message.answer('Произошла ошибка')

@router.callback_query(F.data.startswith('shop_back'))
async def show_shops_again(callback: CallbackQuery, state: FSMContext): 
    try:
        await state.update_data(tg_id_client = callback.message.from_user.id)
        await callback.message.answer(str(WELCOME_PROPOSAL), reply_markup = await kb.shop_list_keyboard())
    except: 
        await callback.message.answer('Произошла ошибка')
    
@router.callback_query(F.data.startswith('shop_list_'))
async def show_categories(callback: CallbackQuery, state: FSMContext):
    try:
        await state.update_data(shop_id = callback.data.split('_')[2])
        await state.update_data(shop_sbys_id = callback.data.split('_')[3])
        await state.update_data(shop_tg_id = callback.data.split('_')[4])
        await state.update_data(price_list_id = callback.data.split('_')[5])
        await callback.message.edit_text(str(WELCOME_PROPOSAL))
        await callback.message.answer(str(CATEGORIES_CHOOSE), reply_markup = await kb.category_list_keyboard())
    except: 
        await callback.message.answer('Произошла ошибка')

@router.callback_query(F.data.startswith('back_categories'))
async def show_categories(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text(str(BRAND_CHOOSE))
        await callback.message.answer(str(CATEGORIES_CHOOSE), reply_markup = await kb.category_list_keyboard())
    except: 
        await callback.message.answer('Произошла ошибка')

@router.callback_query(F.data.startswith('category_list_'))
async def show_brands(callback: CallbackQuery):
    try: 
        await callback.message.edit_text(str(CATEGORIES_CHOOSE))
        await callback.message.answer(str(BRAND_CHOOSE), reply_markup = await kb.brand_list_keyboard(callback.data.split('_')[2]))
    except: 
        await callback.message.answer('Произошла ошибка')

@router.callback_query(F.data.startswith('back_brands_'))
async def show_brands(callback: CallbackQuery):
    try: 
        await callback.message.edit_text(str(CATEGORIES_CHOOSE))
        await callback.message.answer(str(BRAND_CHOOSE), reply_markup = await kb.brand_list_keyboard(callback.data.split('_')[2]))
    except: 
        await callback.message.answer('Произошла ошибка')

@router.callback_query(F.data.startswith('brand_list_'))
async def show_models(callback: CallbackQuery, state: FSMContext): 
    try: 
        await callback.message.edit_text(str(BRAND_CHOOSE))
        await state.update_data(brand = callback.data.split('_')[2])
        await callback.message.answer(str(MODEL_CHOOSE), reply_markup = await kb.model_list_keyboard(callback.data.split('_')[3]))
    except: 
        await callback.message.answer('Произошла ошибка')

@router.callback_query(F.data.startswith('model_list_'))
async def show_product(callback: CallbackQuery, state: FSMContext): 
    try: 
        await callback.message.edit_text(str(MODEL_CHOOSE))
        data_state = await state.get_data()
        await state.set_state(Order.product)
        request_string = str(data_state["brand"]) + ' ' + str(callback.data.split('_')[2])
        product_list = await show_products(data_state["shop_sbys_id"], data_state["price_list_id"], request_string)
        for product in product_list:
            await callback.message.answer(product)
        await callback.message.answer(PRODUCT_CHOOSE)
    except: 
        await callback.message.answer('Произошла ошибка')

@router.message(Order.product)
async def create_order(message: Message, state: FSMContext): 
    # Доделать проверку на активынй заказ
    try: 
        await state.update_data(product = message.text)
        order_data = await state.get_data()
        await rq.create_order(order_data["tg_id_client"], order_data["product"], order_data["shop_id"])
        await bot.send_message(chat_id = order_data["shop_tg_id"], text = f'{ORDER_FOR_SHOP} {order_data["product"]}', reply_markup = await kb.response_shop_keyboard(str(order_data["tg_id_client"])))
        await message.answer('Заказ отправлен на точку. Ожидайте подтверждения брони')
    except Exception as e: 
        await message.answer(str(e))

@router.callback_query(F.data.startswith('approve_order_'))
async def approve_order(callback: CallbackQuery): 
    try:
        final_response = callback.data.split('_')[2]
        if final_response == 'positive': 
            await bot.send_message(chat_id = str(callback.data.split('_')[3]), text = POSITIVE_ORDER, reply_markup=kb.return_to_start)
            await callback.message.answer('Вы подтвердили заказ')
        elif final_response == 'negative':
            await bot.send_message(chat_id = str(callback.data.split('_')[3]), text = NEGARIVE_ORDER, reply_markup=kb.return_to_start)
            await callback.message.answer('Вы отклонили заказ')
    except: 
        await callback.message.answer('Произошла ошибка')