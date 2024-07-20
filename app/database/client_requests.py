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
    async with async_session() as session: 
        return await session.scalars(select(Brand).where(Brand.category == category_id))
    
async def get_model_list(brand_id): 
    async with async_session() as session: 
        return await session.scalars(select(Model).where(Model.brand == brand_id))
    
async def create_order(tg_client, product_order, id_shop): 
    async with async_session() as session:  
        session.add(Order(product = product_order, tg_id_client = tg_client, shop_id = id_shop))
        await session.commit()
