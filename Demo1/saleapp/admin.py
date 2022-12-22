from saleapp.models import Category, User, UserRole, BenhNhan, PhieuKham, Medicine
from saleapp import db, app, dao
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea
from flask import request, redirect


class AuthenticatedBase(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and not current_user.user_role == UserRole.USER
class AuthenticatedModel(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class AuthenticatedModelNurse(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.NURSE
class AuthenticatedModelDoctor(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.DOCTOR

class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class UserView(AuthenticatedModel):
    column_searchable_list = ['name', 'username']
    column_filters = ['name', 'username']
    can_view_details = True
    can_export = True
    column_labels = {
        'name': 'Tên tài khoản',
        'username': 'Tên đăng nhập',
        'password': 'Mật khẩu',
        'active': 'Hoạt động',
        'joined_date': 'Ngày tham gia',
        'user_role': 'Chức vụ'
    }
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    # form_overrides = {
    #     'address': CKTextAreaField
    # }

class MedicineView(AuthenticatedModel):
    column_searchable_list = ['name']
    column_filters = ['name']
    can_view_details = True
    can_export = True
    column_labels = {
        'name': 'Tên thuốc',
        'amount': 'Số lượng',
        'unit_price': 'Giá',
        'import_date': 'Ngày sản xuất',
        'expiration_date': 'Ngày hết dùng',
        'description': 'Công dụng'
    }
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaField
    }
class BenhNhanView(AuthenticatedModelNurse):
    column_searchable_list = ['name', 'phone']
    column_filters = ['name', 'phone']
    can_view_details = True
    can_export = True
    column_labels = {
        'name': 'Tên bệnh nhân',
        'phone': 'Số điện thoại',
        'birth_day': 'Ngày sinh',
        'address': 'Địa chỉ',
        'sex': 'Giới tính',
        'joined_date' : 'Ngày đăng ký'
    }
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'address': CKTextAreaField
    }

class PhieuKhamView(AuthenticatedModelDoctor):
    column_searchable_list = ['name', 'thuoc']
    column_filters = ['name', 'thuoc']
    can_view_details = True
    can_export = True
    column_labels = {
        'name': 'Tên bệnh nhân',
        'ngaykham': 'Ngày khám',
        'trieuchung': 'Triệu chứng',
        'dudoanbenh': 'Dự đoán bệnh',
        'thuoc': 'Thuốc'
    }
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'trieuchung': CKTextAreaField,
        'dudoanbenh': CKTextAreaField
    }


class StatsView(AuthenticatedUser):
    @expose('/')
    def index(self):
        stats = dao.stats_revenue(kw=request.args.get('kw'),
                                  from_date=request.args.get('from_date'),
                                  to_date=request.args.get('to_date'))
        return self.render('admin/stats.html', stats=stats)



class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        stats = dao.count_medicine_by_cate()
        return self.render('admin/index.html', stats=stats)

class LogoutView(AuthenticatedBase):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')





admin = Admin(app=app, name='Quản trị', template_mode='bootstrap4', index_view=MyAdminView())
admin.add_view(UserView(User, db.session, name='Tài khoản'))
admin.add_view(AuthenticatedModel(Category, db.session, name='Loại thuốc'))
admin.add_view(MedicineView(Medicine, db.session, name='Thuốc'))
# admin.add_view(AuthenticatedModel(Tag, db.session, name='Tag'))
admin.add_view(BenhNhanView(BenhNhan, db.session, name='Đăng ký khám'))
admin.add_view(PhieuKhamView(PhieuKham, db.session, name='Phiếu khám bệnh'))
admin.add_view(StatsView(name='Thống kê'))
admin.add_view(LogoutView(name='Đăng xuất'))