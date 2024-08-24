from app.database.models import async_session
from app.database.models import Client, Order, Shop, Model, Brand, Category
from sqlalchemy import select, update
from datetime import datetime, timedelta
from app.admin_handlers import notification_timer

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
    
async def create_order(tg_client: str, product_order: str, id_shop: str): 
    current_datetime = datetime.now() + timedelta(minutes = 60)
    async with async_session() as session:  
        new_order = Order(product = str(product_order), tg_id_client = str(tg_client), shop_id = str(id_shop), experation_time = str(current_datetime), execute = 'CREATE')
        session.add(new_order)
        await session.commit()

async def check_timer_orders(): 
    try:
        date_format = "%Y-%m-%d %H:%M:%S.%f"
        current_time = datetime.now()
        async with async_session() as session: 
            async with session.begin():
                # Находим запись
                stmt = select(Order).where(Order.execute == 'CREATE')
                result = await session.execute(stmt)
                orders = result.scalars()
                for order_iteration in orders:
                    if current_time >= datetime.strptime(order_iteration.experation_time, date_format): 
                        order_iteration.execute = 'EXPIRED'
                        await notification_timer(str(order_iteration.shop_id), str(order_iteration.product))
                        await session.commit()
    except: 
        return('error')
