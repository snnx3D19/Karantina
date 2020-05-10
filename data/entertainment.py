import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Entertainment(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Entertainment'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    ent = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    ent_type = sqlalchemy.Column(sqlalchemy.String, nullable=True, default=None)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    
    users = orm.relation('User')

    def __repr__(self):
        return f'<ent> {self.ent}'