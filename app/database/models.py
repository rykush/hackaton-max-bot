import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
filters = {
        'author': [],
        'type': []
    }


class User_setting(Base):
    __tablename__ = "user_setting"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    max_id: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False)
    filters: so.Mapped[dict] = so.mapped_column(sa.JSON, default=filters)
    on_off: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)


class Parser_data(Base):
    __tablename__ = "parser_data"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    document_id: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    document_filters: so.Mapped[dict] = so.mapped_column(sa.JSON, nullable=False)
    document_send: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)