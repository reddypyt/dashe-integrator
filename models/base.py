import re
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base():
    id: int
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        name = cls.__name__
        name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
        return name
