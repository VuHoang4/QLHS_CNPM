from App import app,db
from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey ,Date, Text,Enum as SQLAEnum
from enum import Enum
from sqlalchemy.orm import relationship
from flask_login import UserMixin

# Enum cho loại điểm
class LoaiDiem(Enum):
    PHUT_15 = "Kiểm Tra Mười Lăm Phút"
    TIET_1 = "Kiểm Tra Một Tiết"
    CUOI_KI = "Kiểm Tra Cuối Kì"

# Enum cho vai trò
class VaiTro(Enum):
    GIAOVIEN = "Giáo Viên"
    GIAOVU = "Giáo Vụ"
    QUANTRI = "Quản Trị Viên"


# Enum cho khối
class Khoi(Enum):
    KHOI_10 = 10
    KHOI_11 = 11
    KHOI_12 = 12
# Enum cho quy định
class LoaiQuyDinh(Enum):
    TUOI_TOI_THIEU = "Tuổi Tối Thiểu"
    TUOI_TOI_DA = "Tuổi Tối Đa"
    SI_SO_TOI_DA = "Sĩ Số Tối Đa"

# Môn học
class MonHoc(db.Model):
    __tablename__='MonHoc'
    maMonHoc = Column(String(10), primary_key=True, nullable=False)  # Mã môn học
    tenMonHoc = Column(String(50), nullable=False)  # Tên môn học
    diem = relationship('Diem', backref='monHoc')
    lopMonHoc = relationship('LopMonHoc', backref='monHoc')

# Lớp
class Lop(db.Model):
    __tablename__='Lop'
    maLop = Column(String(10), primary_key=True, nullable=False)  # Mã lớp
    tenLop = Column(String(50), nullable=False)  # Tên lớp
    siSo = Column(Integer)  # Sĩ số lớp
    khoi = Column(SQLAEnum(Khoi), nullable=False)  # Khối lớp
    maGVCN = Column(String(10), ForeignKey('NguoiDung.maNguoiDung'), nullable=True)  # Mã giáo viên chủ nhiệm
    dsHocSinh = relationship('HocSinhLop', backref='lop')
    lopMonHoc = relationship('LopMonHoc', backref='lop')
    giaoVienChuNhiem = relationship('NguoiDung', backref='lopChuNhiem', uselist=False)

# Lớp có môn học
class LopMonHoc(db.Model):
    __tablename__='LopMonHoc'
    maLop = Column(String(10), ForeignKey('Lop.maLop'), primary_key=True, nullable=False)
    maMonHoc = Column(String(10), ForeignKey('MonHoc.maMonHoc'), primary_key=True, nullable=False)
    maGVBM = Column(String(10), ForeignKey('NguoiDung.maNguoiDung'), nullable=False)  # Mã giáo viên bộ môn

    # Định nghĩa quan hệ tới NguoiDung
    giaoVien = relationship('NguoiDung', backref='lopMonHocs')

# Học sinh
class HocSinh(db.Model):
    __tablename__='HocSinh'
    maHocSinh = Column(String(10), primary_key=True, nullable=False)  # Mã học sinh
    ho = Column(String(50), nullable=False)  # Họ học sinh
    ten = Column(String(50), nullable=False)  # Tên học sinh
    ngaySinh = Column(Date, nullable=False)  # Ngày sinh
    email = Column(String(30), unique=True, nullable=False)  # Email
    gioiTinh = Column(String(10))  # Giới tính
    soDienThoai = Column(String(15), unique=True)  # Số điện thoại
    diaChi = Column(String(100))  # Địa chỉ học sinh
    khoi = Column(SQLAEnum(Khoi))  # Khối lớp
    diem = relationship('Diem', backref='hocSinh')

# Học sinh học lớp
class HocSinhLop(db.Model):
    __tablename__='HocSinhLop'
    maHocSinh = Column(String(10), ForeignKey('HocSinh.maHocSinh'), primary_key=True, nullable=False)
    maLop = Column(String(10), ForeignKey('Lop.maLop'), primary_key=True, nullable=False)
    namHoc = Column(String(10) , primary_key=True, nullable=False)

# Điểm
class Diem(db.Model):
    __tablename__ = 'Diem'

    maMonHoc = Column(String(10), ForeignKey('MonHoc.maMonHoc'), primary_key=True, nullable=False)
    maHocSinh = Column(String(10), ForeignKey('HocSinh.maHocSinh'), primary_key=True, nullable=False)
    maHocKy = Column(String(10), ForeignKey('HocKy.maHocKy'), primary_key=True, nullable=False)
    soThuTuDiem=Column(Integer, primary_key=True, nullable=False)

    giaTriDiem = Column(Float, nullable=False)  # Giá trị điểm
    loaiDiem = Column(SQLAEnum(LoaiDiem), primary_key=True, nullable=False)  # Loại điểm

    def to_dict(self):
        """Chuyển đổi đối tượng Diem thành từ điển."""
        return {
            'maMonHoc': self.maMonHoc,
            'maHocSinh': self.maHocSinh,
            'maHocKy': self.maHocKy,
            'soThuTuDiem': self.soThuTuDiem,
            'giaTriDiem': self.giaTriDiem,
            'loaiDiem': self.loaiDiem.value if self.loaiDiem else None
        }# Nếu `loaiDiem` là enum


# Kỳ học
class HocKy(db.Model):
    __tablename__='HocKy'
    maHocKy = Column(String(10), primary_key=True, nullable=False)  # Mã kỳ học
    tenHocKy = Column(String(20), nullable=False)  # Tên kỳ học
    namHoc = Column(String(10), nullable=False)  # Năm học

    # Mối quan hệ với các lớp khác
    diem = relationship('Diem', backref='hocKy', lazy=True)

# Người dùng
class NguoiDung(db.Model, UserMixin):
    __tablename__='NguoiDung'
    maNguoiDung = Column(String(10), primary_key=True, nullable=False)  # Mã người dùng
    tenDangNhap = Column(String(50), unique=True, nullable=False)  # Tên đăng nhập
    matKhau = Column(String(50), nullable=False)  # Mật khẩu
    vaiTro = Column(SQLAEnum(VaiTro), nullable=False)  # Vai trò
    tenNguoiDung = Column(String(50), nullable=False)  # Tên người dùng
    email = Column(String(30), unique=True, nullable=False)  # Email
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1691062682/tkeflqgroeil781yplxt.jpg')

    def get_id(self):
        return self.maNguoiDung  # Trả về giá trị ID

# Quy định
class QuyDinh(db.Model):
    __tablename__ = 'QuyDinh'
    maQuyDinh = Column(String(10), primary_key=True, nullable=False)  # Mã quy định
    tenQuyDinh = Column(String(20), nullable=False)  # Tên quy định
    ngayRaQuyDinh = Column(Date, nullable=False)  # Ngày ra quy định
    noiDung = Column(Text, nullable=False)  # Nội dung quy định
    giaTri = Column(Integer,nullable=False)  # Giá trị quy định (tuổi tối thiểu, tuổi tối đa, sĩ số tối đa)
    loaiQuyDinh = Column(SQLAEnum(LoaiQuyDinh), nullable=False)  # Loại quy định






if __name__ == '__main__':
    with app.app_context():

        # db.drop_all()
        db.create_all()

