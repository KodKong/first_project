from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import app.database.client_requests as rq


async def shop_list_keyboard():
    keyboard = InlineKeyboardBuilder()
    all_shops = await rq.get_shop_list()
    for shop in all_shops: 
        keyboard.add(InlineKeyboardButton(text = shop.address, callback_data = f'shop_list_{str(shop.id)}_{str(shop.sbys_id)}_{str(shop.tg_id)}_{str(shop.price_list_id)}'))
    return keyboard.adjust(2).as_markup()

async def category_list_keyboard():
    keyboard = InlineKeyboardBuilder()
    all_categories = await rq.get_category_list()
    for category in all_categories: 
        keyboard.add(InlineKeyboardButton(text = category.name, callback_data = f'category_list_{str(category.id)}'))
    return keyboard.adjust(2).as_markup()

async def brand_list_keyboard(category_id):
    keyboard = InlineKeyboardBuilder()
    all_brands = await rq.get_brand_list(category_id)
    for brand in all_brands: 
        keyboard.add(InlineKeyboardButton(text = brand.name, callback_data = f'brand_list_{str(brand.name)}_{str(brand.id)}'))
    return keyboard.adjust(2).as_markup()

async def model_list_keyboard(brand_id):
    keyboard = InlineKeyboardBuilder()
    all_models = await rq.get_model_list(brand_id)
    for model in all_models: 
        keyboard.add(InlineKeyboardButton(text = model.name, callback_data = f'model_list_{str(model.name)}_{str(model.id)}'))
    return keyboard.adjust(2).as_markup()