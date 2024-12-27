from flask_admin import Admin, BaseView, expose
import App.models
from App import app, db,dao
from App.models import MonHoc, Diem, VaiTro, NguoiDung, QuyDinh, LoaiQuyDinh, LoaiDiem, HocSinhLop, \
    HocKy,Lop,LopMonHoc # Sửa đổi để sử dụng các mô hình phù hợp
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask import redirect,flash,abort,url_for, request, jsonify
from wtforms import SelectField
from werkzeug.security import hashlib
from sqlalchemy.exc import IntegrityError
import json
from datetime import datetime

admin = Admin(app=app, name='Quản Trị Hệ Thống Học Sinh', template_mode='bootstrap4')


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.vaiTro == VaiTro.QUANTRI


class MonHocView(AdminView):
    column_list = ['maMonHoc', 'tenMonHoc']  # Các thuộc tính của môn học
    column_labels = {
        'maMonHoc': 'Mã Môn Học',
        'tenMonHoc': 'Tên Môn Học',
    }

    form_columns=('tenMonHoc',)
    can_export = True
    column_searchable_list = ['tenMonHoc']  # Các cột có thể tìm kiếm
    column_filters = ['maMonHoc', 'tenMonHoc']  # Các bộ lọc
    page_size = 10

    def on_model_change(self, form, model, is_created):
        # Kiểm tra xem mã môn học đã tồn tại hay chưa
        if is_created:
            with db.session.no_autoflush:
                # Gán các giá trị từ form vào mô hình
                model.maMonHoc=dao.generate_ma_mon_hoc(form.tenMonHoc.data)
                model.tenMonHoc = form.tenMonHoc.data

                db.session.add(model)  # Thêm mô hình vào phiên làm việc
                db.session.commit()  # Lưu thay đổi vào cơ sở dữ liệu
                flash(f"Đã tạo môn học: {model.tenMonHoc}", "success")  # Thông báo thành công


class DiemView(AdminView):
    column_list = [
        'maMonHoc',
        'tenMonHoc',
        'maHocSinh',
        'tenHocSinh',
        'giaTriDiem',
        'loaiDiem',
    ]

    column_labels = {
        'maMonHoc': 'Mã Môn Học',
        'tenMonHoc': 'Tên Môn Học',
        'maHocSinh': 'Mã Học Sinh',
        'tenHocSinh': 'Tên Học Sinh',
        'giaTriDiem': 'Giá Trị Điểm',
        'loaiDiem': 'Loại Điểm',
    }

    can_export = True
    column_searchable_list = ['maMonHoc', 'maHocSinh']
    # Cho phép lọc theo loại điểm
    column_filters = ['loaiDiem']  # Thêm loại điểm vào danh sách bộ lọc

    page_size = 10

    # Định nghĩa trường ảo
    def _get_ten_mon_hoc(view, context, model, name):
        return model.monHoc.tenMonHoc if model.monHoc.tenMonHoc else ''

    def _get_ten_hoc_sinh(view, context, model, name):
        return model.hocSinh.ten if model.hocSinh.ten else ''

    # def create_model(self, form):
    #     abort(403)  # Từ chối quyền tạo mới

    column_formatters = {
        'tenMonHoc': _get_ten_mon_hoc,
        'tenHocSinh': _get_ten_hoc_sinh,
        'loaiDiem': lambda v, c, m, p: m.loaiDiem.value if m.loaiDiem else 'Không xác định'

    }

    # Định nghĩa form_columns
    form_columns = [
        'giaTriDiem',
        'loaiDiem',
    ]

    # Trường bổ sung cho loại điểm
    form_extra_fields = {
        'loaiDiem': SelectField('Loại Điểm', choices=[
            (LoaiDiem.PHUT_15.value, 'Kiểm Tra Mười Lăm Phút'),
            (LoaiDiem.TIET_1.value, 'Kiểm Tra Một Tiết'),
            (LoaiDiem.CUOI_KI.value, 'Kiểm Tra Cuối Kì')
        ])
    }

    def on_model_change(self, form, model, is_created):
        # Gọi hàm để thiết lập thuộc tính mô hình
        self._set_model_attributes(form, model)

        # Nếu là bản ghi mới
        if is_created:
            db.session.add(model)  # Thêm mô hình vào phiên làm việc
            db.session.commit()  # Lưu thay đổi vào cơ sở dữ liệu
            flash(f"Đã tạo điểm cho học sinh: {model.tenHocSinh}", "success")  # Thông báo thành công

        # Hàm để thiết lập thuộc tính cho mô hình

    def _set_model_attributes(self, form, model):
        # model.giaTriDiem = form.giaTriDiem.data  # Gán giá trị điểm
        model.loaiDiem = LoaiDiem(form.loaiDiem.data)  # Gán loại điểm, đảm bảo nó là Enum





class NguoiDungView(AdminView):
    form_extra_fields = {
        'vaiTro': SelectField('Vai Trò', choices=[
            (VaiTro.GIAOVIEN.value, 'Giáo viên'),
            (VaiTro.GIAOVU.value, 'Giáo vụ'),
            (VaiTro.QUANTRI.value, 'Quản trị')
        ])
    }

    # Các trường hiển thị trong biểu mẫu tạo/sửa
    form_columns = (
        'tenDangNhap',
        'matKhau',
        'vaiTro',
        'tenNguoiDung',
        'email',
    )

    # Các trường hiển thị trong danh sách
    column_list = (
        'tenDangNhap',
        'vaiTro',
        'tenNguoiDung',
        'email',
    )

    # Tùy chỉnh tiêu đề cho các cột
    column_labels = {
        'tenDangNhap': 'Tên Đăng Nhập',
        'vaiTro': 'Vai Trò',
        'tenNguoiDung': 'Tên Người Dùng',
        'email': 'Email',
    }

    # Các trường có thể tìm kiếm
    column_searchable_list = ['tenNguoiDung',
                              'tenDangNhap']  # Thêm tên người dùng và tên đăng nhập vào danh sách tìm kiếm

    # Các bộ lọc có thể sử dụng
    column_filters = ['vaiTro']  # Thêm vai trò vào danh sách lọc

    def on_model_change(self, form, user, is_created):
        if is_created:
            print(f"Vai trò được chọn: {form.vaiTro.data}")  # In ra để kiểm tra
            user.vaiTro = VaiTro(form.vaiTro.data)  # Lấy vai trò từ biểu mẫu
        else:
            # Xử lý khi chỉnh sửa người dùng
            print(f"Cập nhật vai trò: {form.vaiTro.data}")  # In ra để kiểm tra
            user.vaiTro = VaiTro(form.vaiTro.data)  # Cập nhật vai trò mới

        # Mã hóa mật khẩu trước khi lưu
        raw_password = form.matKhau.data  # Giả sử bạn có trường mật khẩu trong biểu mẫu
        hashed_password = hashlib.md5(raw_password.encode('utf-8')).hexdigest()
        print(f"Mật khẩu đã băm: {hashed_password}")  # In ra để kiểm tra

        # Sử dụng session.no_autoflush
        with db.session.no_autoflush:
            user.maNguoiDung = dao.generate_nguoi_dung_id(user.vaiTro)  # Gọi hàm để tạo mã người dùng
            user.matKhau = hashed_password  # Lưu mật khẩu đã mã hóa
            db.session.add(user)  # Thêm user vào session
            db.session.commit()  # Lưu thay đổi



class QuyDinhView(AdminView):
    # Trường bổ sung cho loại quy định
    form_extra_fields = {
        'loaiQuyDinh': SelectField('Loại Quy Định', choices=[
            (LoaiQuyDinh.TUOI_TOI_THIEU.value, 'Tuổi Tối Thiểu'),
            (LoaiQuyDinh.TUOI_TOI_DA.value, 'Tuổi Tối Đa'),
            (LoaiQuyDinh.SI_SO_TOI_DA.value, 'Sĩ Số Tối Đa')
        ])
    }

    # Các thuộc tính hiển thị trong danh sách
    column_list = ('tenQuyDinh', 'ngayRaQuyDinh', 'noiDung', 'loaiQuyDinh', 'giaTri')
    form_columns = ('tenQuyDinh', 'ngayRaQuyDinh', 'noiDung', 'giaTri', 'loaiQuyDinh')

    # Các cột có thể tìm kiếm và lọc
    column_searchable_list = ('tenQuyDinh', 'ngayRaQuyDinh')
    column_filters = ('loaiQuyDinh',)

    # Tùy chỉnh tiêu đề cho các cột
    column_labels = {
        'maQuyDinh': 'Mã Quy Định',
        'giaTri': 'Giá Trị',
        'tenQuyDinh': 'Tên Quy Định',
        'ngayRaQuyDinh': 'Ngày Ban Hành Quy Định',
        'noiDung': 'Nội Dung Quy Định',
        'loaiQuyDinh': 'Loại Quy Định'
    }

    # Định dạng hiển thị cho cột ngày
    column_formatters = {
        'ngayRaQuyDinh': lambda v, c, m, p: m.ngayRaQuyDinh.strftime('%d-%m-%Y') , # Chuyển đổi định dạng ngày sang dạng d-m-Y
        'loaiQuyDinh': lambda v, c, m, p: m.loaiQuyDinh.value if m.loaiQuyDinh else 'Không xác định'
    }

    # Xử lý khi mô hình thay đổi
    def on_model_change(self, form, model, is_created):
        self._set_model_attributes(form, model)  # Gọi hàm để thiết lập thuộc tính mô hình
        if is_created:
            model.maQuyDinh = dao.generate_ma_quy_dinh()  # Tạo mã quy định mới
            db.session.add(model)  # Thêm mô hình vào phiên làm việc
            db.session.commit()  # Lưu thay đổi vào cơ sở dữ liệu
            flash(f"Đã tạo quy định: {model.tenQuyDinh}", "success")  # Thông báo thành công

    # Hàm để thiết lập thuộc tính cho mô hình
    def _set_model_attributes(self, form, model):
        model.tenQuyDinh = form.tenQuyDinh.data  # Gán tên quy định
        model.ngayRaQuyDinh = form.ngayRaQuyDinh.data  # Gán ngày ra quy định
        model.noiDung = form.noiDung.data  # Gán nội dung quy định
        model.loaiQuyDinh = LoaiQuyDinh(form.loaiQuyDinh.data)

    #     Xử lý cập nhật mô hình
    def update_model(self, form, model):
        if model.maQuyDinh is not None:  # Kiểm tra xem quy định đã tồn tại chưa
            flash("Quy định không được phép chỉnh sửa.", "error")  # Thông báo lỗi
            return False  # Ngăn không cho lưu thay đổi
        return super().update_model(form, model)  # Gọi phương thức cha để cập nhật mô hình



class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


class StatsView(AdminView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):

        return self.render('admin/stats.html')

class LopMonHocView(AdminView):
    column_list = [
        'maMonHoc',
        'tenMonHoc',
        'maLop',
        'tenLop',
        'maGVBM',
        'tenGV'
    ]

    column_labels = {
        'maMonHoc': 'Mã Môn Học',
        'tenMonHoc': 'Tên Môn Học',
        'maLop': 'Mã Lớp',
        'tenLop': 'Tên Lớp',
        'maGVBM': 'Mã Giáo Viên',
        'tenGV': 'Tên Giáo Viên'
    }

    can_export = True
    column_searchable_list = ['maMonHoc', 'maLop']
    page_size = 10

    def _get_ten_mon_hoc(view, context, model, name):
        return model.monHoc.tenMonHoc if model.monHoc else 'Không xác định'

    def _get_ten_lop(view, context, model, name):
        return model.lop.tenLop if model.lop else 'Không xác định'

    def _get_ten_giao_vien(view, context, model, name):
        return model.giaoVien.tenNguoiDung if model.giaoVien else 'Không xác định'

    column_formatters = {
        'tenMonHoc': _get_ten_mon_hoc,
        'tenLop': _get_ten_lop,
        'tenGV': _get_ten_giao_vien
    }

    # Tạo danh sách năm học chỉ hiển thị năm hiện tại và năm kế tiếp
    current_year = datetime.now().year
    nam_hoc_list = [
        f"{current_year}-{current_year + 1}"  # Năm hiện tại và năm kế tiếp
    ]

    form_columns = [
        'namHoc',
        'maMonHoc',
        'maLop',
        'maGVBM'
    ]

    form_extra_fields = {
        'namHoc': SelectField('Năm Học', choices=[(nam, nam) for nam in nam_hoc_list]),
        'maMonHoc': SelectField('Môn Học', choices=[
            (m.maMonHoc, m.tenMonHoc) for m in MonHoc.query.all()
        ]),
        'maLop': SelectField('Lớp', choices=[
            (l.maLop, l.tenLop) for l in db.session.query(Lop).join(HocSinhLop).filter(
                HocSinhLop.namHoc == f"2024-2025"
            ).all()
        ]),  # Để trống ban đầu
        'maGVBM': SelectField('Giáo Viên', choices=[
            (g.maNguoiDung, g.tenNguoiDung) for g in NguoiDung.query.filter(NguoiDung.vaiTro == VaiTro.GIAOVIEN).all()
        ])
    }



    def on_model_change(self, form, model, is_created):
        if is_created:

            db.session.add(model)
            db.session.commit()
            flash(f"Đã thêm môn học cho lớp: {model.lop.tenLop}", "success")


# Thêm các view vào admin
admin.add_view(MonHocView(MonHoc, db.session,name='Môn Học'))  # Sử dụng mô hình MonHoc
admin.add_view(DiemView(Diem, db.session,name='Điểm Số'))      # Sử dụng mô hình Diem
admin.add_view(NguoiDungView(NguoiDung, db.session,name='Người Dùng'))  # Sử dụng mô hình NguoiDung
admin.add_view(QuyDinhView(QuyDinh, db.session,name='Quy Định'))
admin.add_view(StatsView(Lop,db.session,'Thống kê',))  # Nếu có view thống kê
admin.add_view(LopMonHocView(LopMonHoc,db.session,'Lớp-Môn Học',))
admin.add_view(LogoutView(name='Đăng xuất'))  # Đăng xuất
