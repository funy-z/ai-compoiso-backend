from database.engine import engine, Base
import database  # 导入 models 包，以确保所有模型都被注册


# 创建所有表
Base.metadata.create_all(bind=engine)
