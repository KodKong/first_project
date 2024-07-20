from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State 
from aiogram.fsm.context import FSMContext
from app.store import show_products
import app.keyboards.client_keyboards as kb
from config import WELCOME_PROPOSAL, CATEGORIES_CHOOSE, BRAND_CHOOSE, PRODUCT_CHOOSE, MODEL_CHOOSE
import app.database.client_requests as rq

router = Router()

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
    await rq.set_client(message.from_user.id)
    await state.update_data(tg_id_client = message.from_user.id)
    await message.answer(str(WELCOME_PROPOSAL), reply_markup = await kb.shop_list_keyboard())
    

@router.callback_query(F.data.startswith('shop_list_'))
async def show_categories(callback: CallbackQuery, state: FSMContext):
    await state.update_data(shop_id = callback.data.split('_')[2])
    await state.update_data(shop_sbys_id = callback.data.split('_')[3])
    await state.update_data(shop_tg_id = callback.data.split('_')[4])
    await state.update_data(price_list_id = callback.data.split('_')[5])
    await callback.message.answer(str(CATEGORIES_CHOOSE), reply_markup = await kb.category_list_keyboard())

@router.callback_query(F.data.startswith('category_list_'))
async def show_brands(callback: CallbackQuery):
    await callback.message.answer(str(BRAND_CHOOSE), reply_markup = await kb.brand_list_keyboard(callback.data.split('_')[2]))

@router.callback_query(F.data.startswith('brand_list_'))
async def show_models(callback: CallbackQuery, state: FSMContext): 
    await state.update_data(brand = callback.data.split('_')[2])
    await callback.message.answer(str(MODEL_CHOOSE), reply_markup = await kb.model_list_keyboard(callback.data.split('_')[3]))

@router.callback_query(F.data.startswith('model_list_'))
async def show_product(callback: CallbackQuery, state: FSMContext): 
    data_state = await state.get_data()
    await state.set_state(Order.product)
    request_string = str(data_state["brand"]) + ' ' + str(callback.data.split('_')[2])
    product_list = show_products(data_state["shop_sbys_id"], data_state["price_list_id"], request_string)
    for product in product_list:
        await callback.message.answer(product)
    await callback.message.answer(PRODUCT_CHOOSE)

@router.message(Order.product)
async def create_order(message: Message, state: FSMContext): 
    await state.update_data(product = message.text)
    order_data = await state.get_data()
    