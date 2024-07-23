from app.database.models import async_session
from app.database.models import Client, Order, Shop, Model, Brand, Category
from sqlalchemy import select, update, delete
import datetime

async def get_shop_list(): 
    async with async_session() as session: 
        return await session.scalars(select(Shop))