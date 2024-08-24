from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import app.database.client_requests as rq


async def shop_list_keyboard():
    try:
        keyboard = InlineKeyboardBuilder()
        all_shops = await rq.get_shop_list()
        for shop in all_shops: 
            keyboard.add(InlineKeyboardButton(text = shop.address, callback_data = f'shop_list_{str(shop.id)}_{str(shop.sbys_id)}_{str(shop.tg_id)}_{str(shop.price_list_id)}'))
        return keyboard.adjust(2).as_markup()
    except: 
        await 'error'

async def category_list_keyboard():
    try:
        keyboard = InlineKeyboardBuilder()
        all_categories = await rq.get_category_list()
        for category in all_categories: 
            keyboard.add(InlineKeyboardButton(text = category.name, callback_data = f'category_list_{str(category.id)}'))
        keyboard.add(InlineKeyboardButton(text = "К выбору точки", callback_data = f'shop_back'))
        return keyboard.adjust(2).as_markup()
    except: 
        await 'error'

async def brand_list_keyboard(category_id):
    try:
        keyboard = InlineKeyboardBuilder()
        all_brands = await rq.get_brand_list(category_id)
        for brand in all_brands: 
            keyboard.add(InlineKeyboardButton(text = brand.name, callback_data = f'brand_list_{str(brand.name)}_{str(brand.id)}'))
        keyboard.add(InlineKeyboardButton(text = 'Назад к категориям', callback_data = 'back_categories'))
        return keyboard.adjust(2).as_markup()
    except: 
        await 'error'

async def model_list_keyboard(brand_id):
    try:
        keyboard = InlineKeyboardBuilder()
        all_models = await rq.get_model_list(brand_id)
        for model in all_models: 
            keyboard.add(InlineKeyboardButton(text = model.name, callback_data = f'model_list_{str(model.name)}_{str(model.id)}'))
        return keyboard.adjust(2).as_markup()
    except: 
        await 'error'

async def response_shop_keyboard(tg_id_client): 
    try:
        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text = 'Подтвердить', callback_data = f'approve_order_positive_{str(tg_id_client)}'))
        keyboard.add(InlineKeyboardButton(text = 'Отклонить', callback_data = f'approve_order_negative_{str(tg_id_client)}'))
        return keyboard.adjust(2).as_markup()
    except: 
        await 'error'

return_to_start = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text = 'Вернуться в начало', callback_data = 'shop_back')]])