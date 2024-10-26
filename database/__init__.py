"""
注意：这里的导入是有用的，确保各个和表对应的class都加入到了Base当中。
这样在create_tables.py中会统一进行表的创建，不需要手动创建表。
"""
from .user import User
from .cost import Cost
