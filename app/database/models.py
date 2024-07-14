from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Client(Base): 
    __tablename__ = 'clients'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[str] = mapped_column(String(25))

class Shop(Base): 
    __tablename__ = 'shops'

    id: Mapped[int] = mapped_column(primary_key=True) 
    sbys_id: Mapped[str] = mapped_column(String(32))
    tg_id: Mapped[str] = mapped_column(String(25))
    address: Mapped[str] = mapped_column(String(64))

class Order(Base): 
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    product: Mapped[str] = mapped_column(String(200))
    tg_id_client: Mapped[str] = mapped_column(String(25))
    experation_time: Mapped[str] = mapped_column(String(25))
    execute: Mapped[str] = mapped_column(String(6))
    shop_id: Mapped[int] = mapped_column(ForeignKey('shops.id'))

class Category(Base): 
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

class Brand(Base): 
    __tablename__ = 'brands'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    category: Mapped[int] = mapped_column(ForeignKey('categories.id'))

class Model(Base): 
    __tablename__ = 'models'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    brand: Mapped[int] = mapped_column(ForeignKey('brands.id'))

async def async_main():
    async with engine.begin() as conn: 
        await conn.run_sync(Base.metadata.create_all)