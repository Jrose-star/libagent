from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import create_engine, DateTime
from app.config import settings
from datetime import datetime

# engine = create_engine(settings.DATABASE_URL)
engine = create_engine(
    settings.DATABASE_URL,
    pool_recycle=3600,  # 连接池回收时间，设置为3600秒（1小时）
    pool_pre_ping=True,  # 每次使用前先检查连接是否有效，无效则自动重建
)

# 数据库session会话的连接工厂
SessionLocal = sessionmaker(bind=engine, autoflush=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment="主键ID", sort_order=-1
    )
    create_time: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, comment="创建时间", sort_order=1
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间",
        sort_order=2,
    )
