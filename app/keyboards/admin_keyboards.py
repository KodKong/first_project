from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import app.database.client_requests as rq


buttons_for_admin = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text = 'Обновить список точек', callback_data = 'update_shop_list')],
        [InlineKeyboardButton(text = 'Удалить точку', callback_data = 'delete_shop')],
        [InlineKeyboardButton(text = 'Обновить прайс-листы', callback_data = 'update_price_list')],
        [InlineKeyboardButton(text = 'Добавить категорию', callback_data = 'add_category')],
        [InlineKeyboardButton(text = 'Удалить категорию', callback_data = 'delete_category')],
        [InlineKeyboardButton(text = 'Добавить бренд', callback_data = 'add_brand')],
        [InlineKeyboardButton(text = 'Удалить бренд', callback_data = 'delete_brand')],
        [InlineKeyboardButton(text = 'Добавить модель', callback_data = 'add_model')],
        [InlineKeyboardButton(text = 'Удалить модель', callback_data = 'delete_model')],
        [InlineKeyboardButton(text = 'Сделать рассылку', callback_data = 'create_marketing')]])
