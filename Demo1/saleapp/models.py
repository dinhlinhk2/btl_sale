import calendar
import hashlib

from sqlalchemy import Column, Integer, String, Text, Boolean, Float, ForeignKey, Enum, DateTime, DECIMAL
from sqlalchemy.orm import relationship, backref
from saleapp import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime


class UserRole(UserEnum):
    USER = 1
    ADMIN = 2
    DOCTOR = 3
    NURSE = 4


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)




#
# prod_tag = db.Table('medicine_tag',
#                     Column('medicine_id', Integer, ForeignKey('medicine_id'), primary_key=True),
#                     Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True))



class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100), nullable=False)
    email = Column(String(100))
    date_register = Column(DateTime, default=datetime.now())
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.name


class BenhNhan(BaseModel):
    name = Column(String(50), nullable=False)
    phone = Column(String(10), nullable=False)
    birth_day = Column(DateTime, default= datetime.now())
    address = Column(String(100), nullable=False)
    sex = Column(Boolean, default=False)
    joined_date = Column(DateTime, default=datetime.now())

    def __str__(self):
        return self.name

class Category(BaseModel):
    __tablename__ = 'category'
    name = Column(String(50), nullable=False)
    medicine = relationship('Medicine', backref='Loại Thuốc', lazy=True)

    def __str__(self):
        return self.name
class Medicine(BaseModel):
    name = Column(String(100), nullable=False, unique=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    description = Column(Text)
    amount = Column(Integer, default=0)
    unit_price = Column(Float, default=0)
    image = Column(String(500))
    import_date = Column(DateTime, default=datetime.now())
    expiration_date = Column(DateTime, default=datetime.now())
    receipt_details = relationship('ReceiptDetails', backref='medicine', lazy=True)
    # tags = relationship('Tag', secondary='medicine_tag', lazy='subquery',
    #                     backref=backref('medicine', lazy=True))
    comments = relationship('Comment', backref='medicine', lazy=True)
    def __str__(self):
        return self.name

class PhieuKham(BaseModel):
    name = Column(String(50), nullable=False)
    ngaykham = Column(DateTime, default=datetime.now())
    trieuchung = Column(String(100))
    dudoanbenh = Column(String(100), nullable=False)
    thuoc = Column(String(100))
    def __str__(self):
        return self.name




class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    medicine_id = Column(Integer, ForeignKey(Medicine.id), nullable=False)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)


class Comment(BaseModel):
    content = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    medicine_id = Column(Integer, ForeignKey(Medicine.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()
        db.create_all()

        # c1 = Category(name='Viên')
        # c2 = Category(name='Vỹ')
        # c3 = Category(name='Chai')
        #
        # db.session.add_all([c1, c2, c3])
        # db.session.commit()
        # p1 = Medicine(name='Panadol', amount=1, unit_price=175.000,
        #              image='https://cdn.tgdd.vn/Products/Images/6985/193179/vien-uong-ho-tro-giac-ngu-nature-s-bounty-melatoni-thumb-1-1-600x600.jpg',
        #              category_id=1)
        # p2 = Medicine(name='Dau bung', amount= 1, unit_price=125.000,
        #              image='https://cdn.tgdd.vn/Products/Images/6985/214935/ginkgo-biloba-omega-3-coenzym-q10-hop-100vien-thumb-1-1-600x600.jpg',
        #              category_id=1)
        # p3 = Medicine(name='nhuc dau', amount = 1, unit_price=330.000,
        #              image='https://cdn.tgdd.vn/Products/Images/6985/129741/vien-uong-otiv-30-vien-thumb-1-1-600x600.jpg',
        #              category_id=3)
        # p4 = Medicine(name='Ho', amount = 1, unit_price=800.000,
        #              image='https://cdn.tgdd.vn/Products/Images/6985/210465/healthy-golden-super-brain-heart-360mg-hop-100vien-thumb-1-1-600x600.jpg',
        #              category_id=1)
        # p5 = Medicine(name='Xui', amount= 1, unit_price=182.000,
        #              image='https://cdn.tgdd.vn/Products/Images/6985/243293/hoat-huyet-minh-nao-khang-extra-20-vien-thumb-1-1-600x600.jpg',
        #              category_id=2)
        # #
        # db.session.add_all([p1, p2, p3, p4, p5])
        # db.session.commit()

        # import hashlib
        # password = str(hashlib.md5('123'.encode('utf-8')).hexdigest())
        # u = User(name='linh', username='admin', password=password,
        #          user_role=UserRole.ADMIN,
        #          avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg')
        # db.session.add(u)
        # db.session.commit()
        #
        # c1 = Comment(content='Good', user_id=1, medicine_id=1)
        # c2 = Comment(content='Nice', user_id=1, medicine_id=1)
        # db.session.add_all([c1, c2])
        # db.session.commit()
