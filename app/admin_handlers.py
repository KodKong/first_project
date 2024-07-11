from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from app.store import get_token, get_point_list, get_points_price_list

router_admin = Router()

