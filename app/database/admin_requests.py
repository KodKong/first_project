from app.database.models import async_session
from app.database.models import Client, Order, Shop, Model, Brand, Category
from sqlalchemy import select, update, delete
import datetime

async def get_shop_list(): 
    async with async_session() as session: 
        return await session.scalars(select(Shop))
    
async def get_client_list(): 
    async with async_session() as session: 
        return await session.scalars(select(Client))
    
async def create_new_category(name_category):  
    async with async_session() as session: 
        new_category = Category(name = name_category)
        session.add(new_category)
        await session.commit()
    
async def create_new_brand(name_brand, parent_id):  
    async with async_session() as session: 
        new_brand = Brand(name = name_brand, category = parent_id)
        session.add(new_brand)
        await session.commit()

async def create_new_model(name_model, parent_id):  
    async with async_session() as session: 
        new_model = Model(name = name_model, brand = parent_id)
        session.add(new_model)
        await session.commit()

async def get_category_list(): 
    async with async_session() as session: 
        return await session.scalars(select(Category))
    
async def get_brand_list(category_id): 
    async with async_session() as session: 
        return await session.scalars(select(Brand).where(Brand.category == category_id))