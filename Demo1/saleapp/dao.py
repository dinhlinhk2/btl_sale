from saleapp.models import Category, User, Receipt, ReceiptDetails, Comment, Medicine
from saleapp import db
import hashlib
from flask_login import current_user
from sqlalchemy import func


def load_categories():
    return Category.query.all()



def load_medicine(cate_id=None, kw=None):
    query = Medicine.query

    if cate_id:
        query = query.filter(Medicine.category_id.__eq__(cate_id))

    if kw:
        query = query.filter(Medicine.name.contains(kw))

    return query.all()


def get_medicine_by_id(medicine_id):
    return Medicine.query.get(medicine_id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def register(name, username, password, avatar, email):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, username=username.strip(), password=password, avatar=avatar, email=email)
    db.session.add(u)
    db.session.commit()


def get_user_by_id(user_id):
    return User.query.get(user_id)

def save_receipt(cart):
    if cart:
        r = Receipt(user=current_user)
        db.session.add(r)

        for c in cart.values():
            d = ReceiptDetails(quantity=c['quantity'], price=c['price'],
                               receipt=r, medicine_id=c['id'])
            db.session.add(d)

        db.session.commit()

def count_medicine_by_cate():
    return db.session.query(Category.id, Category.name, func.count(Medicine.id))\
             .join(Medicine, Medicine.category_id.__eq__(Category.id), isouter=True)\
             .group_by(Category.id).all()


def stats_revenue(kw=None, from_date=None, to_date=None):
    query = db.session.query(Medicine.id, Medicine.name, func.sum(ReceiptDetails.quantity*ReceiptDetails.price))\
                      .join(ReceiptDetails, ReceiptDetails.medicine_id.__eq__(Medicine.id))\
                      .join(Receipt, ReceiptDetails.receipt_id.__eq__(Receipt.id))

    if kw:
        query = query.filter(Medicine.name.contains(kw))

    if from_date:
        query = query.filter(Receipt.created_date.__ge__(from_date))

    if to_date:
        query = query.filter(Receipt.created_date.__le__(to_date))

    return query.group_by(Medicine.id).order_by(-Medicine.id).all()


def load_comments(medicine_id):
    return Comment.query.filter(Comment.medicine_id.__eq__(medicine_id)).order_by(-Comment.id).all()


def save_comment(content, medicine_id):
    c = Comment(content=content, medicine_id=medicine_id, user=current_user)
    db.session.add(c)
    db.session.commit()

    return c


if __name__ == '__main__':
    from saleapp import app
    with app.app_context():
        print(count_medicine_by_cate())