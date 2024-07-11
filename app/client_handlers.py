from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from app.store import get_token, get_point_list, get_points_price_list
from config import WELCOME_PROPOSAL

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message): 
    await message.answer(str(WELCOME_PROPOSAL))
    r = get_token()
    r2 = get_point_list(r)
    r3 = get_points_price_list(r, r2['salesPoints'][0]['id'])
    await message.answer(r)

@router.callback_query(F.startwith())
async def cmd_start(callback: CallbackQuery):
    r = get_token()