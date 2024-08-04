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
    
async def get_model_list(brand_id): 
    async with async_session() as session: 
        return await session.scalars(select(Model).where(Model.brand == brand_id))
    
async def delete_model(model_id): 
    async with async_session() as session: 
        stmt = select(Model).filter(Model.id == model_id)
        result = await session.execute(stmt)
        model_to_delete = result.scalars().first()
        await session.delete(model_to_delete)
        await session.commit()

async def delete_brand(brand_id): 
    async with async_session() as session: 
        stmt = select(Brand).filter(Brand.id == brand_id)
        result = await session.execute(stmt)
        brand_to_delete = result.scalars().first()
        await session.delete(brand_to_delete)
        await session.commit()

async def delete_category(category_id): 
    async with async_session() as session: 
        stmt = select(Category).filter(Category.id == category_id)
        result = await session.execute(stmt)
        category_to_delete = result.scalars().first()
        await session.delete(category_to_delete)
        await session.commit()
        