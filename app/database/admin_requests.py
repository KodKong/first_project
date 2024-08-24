from app.database.models import async_session
from app.database.models import Client, Shop, Model, Brand, Category, Order
from sqlalchemy import select

async def get_shop_list(): 
    try:
        async with async_session() as session: 
            return await session.scalars(select(Shop))
    except: 
        return('error')
    
async def get_shop_by_id(id_shop): 
    try:
        async with async_session() as session: 
            return await session.scalars(select(Shop).where(id == id_shop))
    except: 
        return('error')
    
async def get_client_list(): 
    try:
        async with async_session() as session: 
            return await session.scalars(select(Client))
    except: 
        return('error')
    
async def create_new_category(name_category: str):  
    try:
        async with async_session() as session: 
            new_category = Category(name = name_category)
            session.add(new_category)
            await session.commit()
    except: 
        return('error')
    
async def create_new_brand(name_brand: str, parent_id: str):  
    try:    
        async with async_session() as session: 
            new_brand = Brand(name = name_brand, category = parent_id)
            session.add(new_brand)
            await session.commit()
    except: 
        return('error')

async def create_new_model(name_model: str, parent_id: str):  
    try:
        async with async_session() as session: 
            new_model = Model(name = name_model, brand = parent_id)
            session.add(new_model)
            await session.commit()
    except: 
        return('error')

async def get_category_list(): 
    try:
        async with async_session() as session: 
            return await session.scalars(select(Category))
    except: 
        return('error')  
    
async def get_brand_list(category_id: str): 
    try:
        async with async_session() as session: 
            return await session.scalars(select(Brand).where(Brand.category == category_id))
    except: 
        return('error')
    
async def get_model_list(brand_id: str): 
    try:    
        async with async_session() as session: 
            return await session.scalars(select(Model).where(Model.brand == brand_id))
    except: 
        return('error')
    
async def delete_model(model_id: str):
    try: 
        async with async_session() as session: 
            stmt = select(Model).filter(Model.id == model_id)
            result = await session.execute(stmt)
            model_to_delete = result.scalars().first()
            await session.delete(model_to_delete)
            await session.commit()
    except: 
        return('error')

async def delete_brand(brand_id: str): 
    try:
        async with async_session() as session: 
            stmt = select(Brand).filter(Brand.id == brand_id)
            result = await session.execute(stmt)
            brand_to_delete = result.scalars().first()
            await session.delete(brand_to_delete)
            await session.commit()
    except: 
        return('error')

async def delete_category(category_id: str): 
    try:    
        async with async_session() as session: 
            stmt = select(Category).filter(Category.id == category_id)
            result = await session.execute(stmt)
            category_to_delete = result.scalars().first()
            await session.delete(category_to_delete)
            await session.commit()
    except: 
        return('error')

async def update_price_list(sbys_id: str, new_price_id: str): 
    try:
        async with async_session() as session: 
            async with session.begin():
                # Находим запись
                stmt = select(Shop).where(Shop.sbys_id == sbys_id)
                result = await session.execute(stmt)
                shop = result.scalars().first()
                if shop:
                    shop.price_list_id = new_price_id
                    await session.commit()
    except: 
        return('error')

async def create_new_shop(new_address: str, new_tg_id: str, new_sbys_id: str):  
    try:
        async with async_session() as session: 
            new_shop = Shop(address = new_address, tg_id = new_tg_id, sbys_id = new_sbys_id, price_list_id = '1')
            session.add(new_shop)
            await session.commit()
    except: 
        return('error')

async def delete_shop(shop_id: str): 
    try:
        async with async_session() as session: 
            stmt = select(Shop).filter(Shop.id == shop_id)
            result = await session.execute(stmt)
            shop_to_delete = result.scalars().first()
            await session.delete(shop_to_delete)
            await session.commit()
    except: 
        return('error')
    
async def create_structure_to_database(): 
    categories = ['Табак', 'Одноразовые электронные сигареты', 'Жидкости', 'Бестабачные смеси', 'Принадлежности для кальяна', 'Картриджи/испарители', 'Кальяны', 'Жевательный табак', 'Уголь', 'POD - системы'] 
    brand_tabac = ['']
    try:
        async with async_session() as session: 
            for category in categories:
                new_category = Category(name = category)
                session.add(new_category)
                await session.commit()
    except: 
        return('error')
    


        
        