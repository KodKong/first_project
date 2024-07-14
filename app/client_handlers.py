from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State 
from aiogram.fsm.context import FSMContext
from app.store import get_token, get_point_list, get_points_price_list
import app.keyboards.client_keyboards as kb
from config import WELCOME_PROPOSAL, CATEGORIES_CHOOSE, BRAND_CHOOSE
import app.database.client_requests as rq

router = Router()

class Order(StatesGroup):
    shop_id = State(),
    tg_id_client = State(), 
    brand = State(),
    product = State()

@router.message(CommandStart())
async def show_shops(message: Message, state: FSMContext): 
    await rq.set_client(message.from_user.id)
    await state.update_data(tg_id_client = message.from_user.id)
    await message.answer(str(WELCOME_PROPOSAL), reply_markup = await kb.shop_list_keyboard())
    

@router.callback_query(F.data.startswith('shop_list_'))
async def show_categories(callback: CallbackQuery, state: FSMContext):
    await state.update_data(shop_id = callback.data.split('_')[1])
    await callback.message.answer(str(CATEGORIES_CHOOSE), reply_markup = await kb.category_list_keyboard())

@router.callback_query(F.data.startswith('category_list_'))
async def show_brands(callback: CallbackQuery):
    await callback.message.answer(str(BRAND_CHOOSE), reply_markup = await kb.brand_list_keyboard(callback.data.split('_')[2]))

@router.callback_query(F.data.startswith('brand_list_'))
async def show_product(callback: CallbackQuery, state: FSMContext): 
    await state.update_data(brand = callback.data.split('_')[2])
    await state.set_state(Order.product)