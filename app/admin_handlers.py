from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State 
from aiogram.fsm.context import FSMContext
from app.store import get_point_list
import app.keyboards.admin_keyboards as kb
from config import FIRST_ADMIN_CHAT_ID
import app.database.admin_requests as rq


router_admin = Router()

@router_admin.message(Command('admin_panel'))
async def show_shops(message: Message): 
    if message.from_user.id != FIRST_ADMIN_CHAT_ID: 
        await message.answer('Здарова отец', reply_markup = kb.buttons_for_admin)
    else: 
        await message.answer('Я вас не понимаю')

@router_admin.callback_query(F.data == 'update_shop_list')
async def show_categories(callback: CallbackQuery):
    new_list_shops = get_point_list()
    current_list_shops = await rq.get_shop_list()