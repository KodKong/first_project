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
    new_order_id = rq.create_order(order_data["tg_id_client"], order_data["product"], order_data["shop_id"])
    await bot.send_message(chat_id = order_data["shop_tg_id"], text = f'{ORDER_FOR_SHOP} {order_data["product"]}', reply_markup = await kb.response_shop_keyboard(str(order_data["tg_id_client"])))


@router.callback_query(F.data.startswith('approve_order_'))
async def approve_order(callback: CallbackQuery, state: FSMContext): 
    final_response = callback.data.split('_')[2]
    order_data = await state.get_data()
    await callback.message.answer(str(order_data["tg_id_client"]))
    #if final_response == 'positive': 
        #await bot.send_message(chat_id = str(order_data["tg_id_client"]), text = POSITIVE_ORDER)
    #elif final_response == 'negative':
        #await bot.send_message(chat_id = str(order_data["tg_id_client"]), text = NEGARIVE_ORDER)