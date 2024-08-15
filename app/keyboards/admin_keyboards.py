from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import app.database.admin_requests as rq


buttons_for_first_admin = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text = 'Добавить новую точку', callback_data = 'add_shop')],
        [InlineKeyboardButton(text = 'Удалить точку', callback_data = 'delete_shop')],
        [InlineKeyboardButton(text = 'Обновить прайс-листы', callback_data = 'update_price_list')],
        [InlineKeyboardButton(text = 'Добавить категорию', callback_data = 'add_category')],
        [InlineKeyboardButton(text = 'Удалить категорию', callback_data = 'delete_category')],
        [InlineKeyboardButton(text = 'Добавить бренд', callback_data = 'add_brand')],
        [InlineKeyboardButton(text = 'Удалить бренд', callback_data = 'delete_brand')],
        [InlineKeyboardButton(text = 'Добавить модель', callback_data = 'add_model')],
        [InlineKeyboardButton(text = 'Удалить модель', callback_data = 'delete_model')],
        [InlineKeyboardButton(text = 'Сделать рассылку', callback_data = 'create_marketing')]])

buttons_for_admins = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text = 'Обновить прайс-листы', callback_data = 'update_price_list')],
        [InlineKeyboardButton(text = 'Добавить категорию', callback_data = 'add_category')],
        [InlineKeyboardButton(text = 'Удалить категорию', callback_data = 'delete_category')],
        [InlineKeyboardButton(text = 'Добавить бренд', callback_data = 'add_brand')],
        [InlineKeyboardButton(text = 'Удалить бренд', callback_data = 'delete_brand')],
        [InlineKeyboardButton(text = 'Добавить модель', callback_data = 'add_model')],
        [InlineKeyboardButton(text = 'Удалить модель', callback_data = 'delete_model')],
        [InlineKeyboardButton(text = 'Сделать рассылку', callback_data = 'create_marketing')]])

buttons_for_marketing = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text = 'Отправить рассылку', callback_data = 'approve_marketing')],
        [InlineKeyboardButton(text = 'Отмена', callback_data = 'reject_marketing')]])

# Клавиатуры для добавления

async def category_list_keyboard():
    try:
        keyboard = InlineKeyboardBuilder()
        all_categories = await rq.get_category_list()
        for category in all_categories: 
            keyboard.add(InlineKeyboardButton(text = category.name, callback_data = f'add_brand_{str(category.id)}'))
        return keyboard.adjust(2).as_markup()
    except: 
        return('error')

async def category_for_model_list_keyboard():
    try:
        keyboard = InlineKeyboardBuilder()
        all_categories = await rq.get_category_list()
        for category in all_categories: 
            keyboard.add(InlineKeyboardButton(text = category.name, callback_data = f'add_model_1_{str(category.id)}'))
        return keyboard.adjust(2).as_markup()
    except: 
        return('error')

async def brand_list_keyboard(category_id):
    try:
        keyboard = InlineKeyboardBuilder()
        all_brands = await rq.get_brand_list(category_id)
        for brand in all_brands: 
            keyboard.add(InlineKeyboardButton(text = brand.name, callback_data = f'add_model_2_{str(brand.id)}'))
        return keyboard.adjust(2).as_markup()
    except: 
        return('error')

# Клавиатуры для удаления 

async def delete_category_keyboard():
    try:   
        keyboard = InlineKeyboardBuilder()
        all_categories = await rq.get_category_list()
        for category in all_categories: 
            keyboard.add(InlineKeyboardButton(text = category.name, callback_data = f'delete_category_1_{str(category.id)}'))
        return keyboard.adjust(2).as_markup()
    except: 
        return('error')

async def delete_category_for_brand_list_keyboard():
    try:
        keyboard = InlineKeyboardBuilder()
        all_categories = await rq.get_category_list()
        for category in all_categories: 
            keyboard.add(InlineKeyboardButton(text = category.name, callback_data = f'delete_brand_1_{str(category.id)}'))
        return keyboard.adjust(2).as_markup()
    except: 
        return('error')

async def delete_brand_list_keyboard(category_id):
    try:
        keyboard = InlineKeyboardBuilder()
        all_brands = await rq.get_brand_list(category_id)
        for brand in all_brands: 
            keyboard.add(InlineKeyboardButton(text = brand.name, callback_data = f'delete_brand_2_{str(brand.id)}'))
        return keyboard.adjust(2).as_markup()
    except: 
        return('error')

async def delete_category_for_model_list_keyboard():
    try:
        keyboard = InlineKeyboardBuilder()
        all_categories = await rq.get_category_list()
        for category in all_categories: 
            keyboard.add(InlineKeyboardButton(text = category.name, callback_data = f'delete_model_1_{str(category.id)}'))
        return keyboard.adjust(2).as_markup()
    except: 
        return('error')

async def delete_brand_for_model_list_keyboard(category_id):
    try:
        keyboard = InlineKeyboardBuilder()
        all_brands = await rq.get_brand_list(category_id)
        for brand in all_brands: 
            keyboard.add(InlineKeyboardButton(text = brand.name, callback_data = f'delete_model_2_{str(brand.id)}'))
        return keyboard.adjust(2).as_markup()
    except: 
        return('error')

async def delete_model_list_keyboard(brand_id):
    try:
        keyboard = InlineKeyboardBuilder()
        all_models = await rq.get_model_list(brand_id)
        for model in all_models: 
            keyboard.add(InlineKeyboardButton(text = model.name, callback_data = f'delete_model_3_{str(model.id)}'))
        return keyboard.adjust(2).as_markup()
    except: 
        return('error')

async def delete_shop_list_keyboard():
    try:
        keyboard = InlineKeyboardBuilder()
        all_shops = await rq.get_shop_list()
        for shop in all_shops: 
            keyboard.add(InlineKeyboardButton(text = shop.address, callback_data = f'delete_shop_1_{str(shop.id)}'))
        return keyboard.adjust(2).as_markup()
    except: 
        return('error')

