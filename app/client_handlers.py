from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from app.store import get_token, get_point_list, get_points_price_list

router = Router()

@router.message(CommandStart())
async def cmd_start(message:Message): 
    r = get_token()
    r2 = get_point_list(r)
    r3 = get_points_price_list(r, r2['salesPoints'][0]['id'])
    await message.answer(r)