from app.database.models import async_session
from app.database.models import Client, Order, Shop, Model, Brand, Category
from sqlalchemy import select, update, delete

async def set_client(tg_id): 
    async with async_session() as session: 
        client = await session.scalar(select(Client).where(Client.tg_id == tg_id))

        if not client: 
            session.add(Client(tg_id = tg_id))
            await session.commit()

async def get_shop_list(): 
    async with async_session() as session: 
        return await session.scalars(select(Shop))
    
async def get_category_list(): 
    async with async_session() as session: 
        return await session.scalars(select(Category))
    
async def get_brand_list(category_id): 
    print(str(category_id))
    async with async_session() as session: 
        return await session.scalars(select(Brand).where(Brand.category == category_id))