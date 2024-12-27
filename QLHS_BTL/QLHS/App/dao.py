from App.models import NguoiDung, MonHoc, VaiTro, Lop,Khoi, QuyDinh, HocSinh, Diem,HocKy, HocSinhLop,LopMonHoc
from App import app, db
import hashlib
from datetime import datetime
from sqlalchemy.orm import sessionmaker,Session
import random



def auth_user(username, password, role=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = NguoiDung.query.filter(NguoiDung.tenDangNhap.__eq__(username),
                          NguoiDung.matKhau.__eq__(password))

    if role:
        u = u.filter(NguoiDung.vaiTro == role)

    return u.first()


import logging
# Cấu hình logging
logging.basicConfig(level=logging.INFO)

def add_object_to_db(new_object):
    """Hàm thêm đối tượng vào cơ sở dữ liệu và quản lý lỗi."""
    db.session.add(new_object)
    try:
        db.session.commit()
        logging.info(f"Thêm thành công: {new_object}")
    except Exception as e:
        db.session.rollback()
        logging.error(f"Lỗi khi thêm: {e}")

def add_mon_hoc(ten_mon_hoc):
    ma_mon_hoc = generate_ma_mon_hoc(ten_mon_hoc)

    new_mon_hoc = MonHoc(maMonHoc=ma_mon_hoc, tenMonHoc=ten_mon_hoc)
    add_object_to_db(new_mon_hoc)

def add_nguoi_dung(ten_dang_nhap, mat_khau, vai_tro, ten_nguoi_dung, email,avatar=None):
    ma_nguoi_dung = generate_nguoi_dung_id(vai_tro)
    mat_khau_ma_hoa = hashlib.md5(mat_khau.encode('utf-8')).hexdigest()

    new_user = NguoiDung(
        maNguoiDung=ma_nguoi_dung,
        tenDangNhap=ten_dang_nhap,
        matKhau=mat_khau_ma_hoa,
        vaiTro=vai_tro,
        tenNguoiDung=ten_nguoi_dung,
        email=email,
        avatar=avatar
    )
    add_object_to_db(new_user)

def add_quy_dinh(ten_quy_dinh, ngay_ra_quy_dinh, noi_dung, gia_tri, loai_quy_dinh):
    ma_quy_dinh = generate_ma_quy_dinh()

    new_quy_dinh = QuyDinh(
        maQuyDinh=ma_quy_dinh,
        tenQuyDinh=ten_quy_dinh,
        ngayRaQuyDinh=ngay_ra_quy_dinh,
        noiDung=noi_dung,
        giaTri=gia_tri,
        loaiQuyDinh=loai_quy_dinh
    )
    add_object_to_db(new_quy_dinh)

def add_hoc_sinh(ho, ten, ngay_sinh, email, gioi_tinh, so_dien_thoai,dia_chi,khoi):
    ma_hoc_sinh = generate_ma_hoc_sinh()

    new_hoc_sinh = HocSinh(
        maHocSinh=ma_hoc_sinh,
        ho=ho,
        ten=ten,
        ngaySinh=ngay_sinh,
        email=email,
        gioiTinh=gioi_tinh,
        soDienThoai=so_dien_thoai,
        diaChi=dia_chi,
        khoi=khoi
    )
    add_object_to_db(new_hoc_sinh)

def add_diem(gia_tri_diem, loai_diem, ma_mon_hoc, ma_hoc_sinh, ma_hoc_ky):
    stt_diem = get_stt_diem(ma_mon_hoc, ma_hoc_sinh, ma_hoc_ky, loai_diem)
    new_diem = Diem(
        giaTriDiem=gia_tri_diem,
        loaiDiem=loai_diem,
        maMonHoc=ma_mon_hoc,
        maHocSinh=ma_hoc_sinh,
        maHocKy=ma_hoc_ky,
        soThuTuDiem=stt_diem
    )
    add_object_to_db(new_diem)


def get_stt_diem(ma_mon_hoc, ma_hoc_sinh, ma_hoc_ky, loai_diem):
    # Đếm số lượng điểm hiện có dựa trên các điều kiện
    count = Diem.query.filter_by(
        maMonHoc=ma_mon_hoc,
        maHocSinh=ma_hoc_sinh,
        maHocKy=ma_hoc_ky,
        loaiDiem=loai_diem
    ).count()

    return count + 1  # Gán giá trị stt_diem


def add_hoc_ky(ten_hoc_ky, nam_hoc):
    maHocKy=generate_ma_hoc_ky(nam_hoc)

    new_hoc_ky = HocKy(
        maHocKy=maHocKy,
        tenHocKy=ten_hoc_ky,
        namHoc=nam_hoc
    )
    add_object_to_db(new_hoc_ky)


def add_lop(maLop,tenLop, siSo, khoi, maGVCN=None):
    # maLop = generate_ma_lop(khoi)

    new_lop = Lop(
        maLop=maLop,
        tenLop=tenLop,
        siSo=siSo,
        khoi=khoi,
        maGVCN=maGVCN
    )
    add_object_to_db(new_lop)

def add_hoc_sinh_vao_lop(maHocSinh, maLop, namHoc):
    existing_record = HocSinhLop.query.filter_by(maHocSinh=maHocSinh, maLop=maLop,  namHoc=namHoc).first()
    if existing_record:
        logging.warning(f"Học sinh {maHocSinh} đã được ghi danh vào lớp {maLop} trong kỳ học {namHoc}.")
        return

    new_hoc_sinh_lop = HocSinhLop(
        maHocSinh=maHocSinh,
        maLop=maLop,
        namHoc=namHoc
    )
    add_object_to_db(new_hoc_sinh_lop)

def add_mon_hoc_vao_lop(maLop, maMonHoc, maGVBM):
    existing_record = LopMonHoc.query.filter_by(maLop=maLop, maMonHoc=maMonHoc).first()
    if existing_record:
        logging.warning(f"Môn học {maMonHoc} đã tồn tại trong lớp {maLop}.")
        return

    new_lop_mon_hoc = LopMonHoc(
        maLop=maLop,
        maMonHoc=maMonHoc,
        maGVBM=maGVBM
    )
    add_object_to_db(new_lop_mon_hoc)


def delete_hoc_sinh(student_id, class_id):
    try:
        student_class = db.session.query(HocSinhLop).filter(
            HocSinhLop.maHocSinh == student_id,
            HocSinhLop.maLop == class_id
        ).first()

        if student_class:
            db.session.delete(student_class)
            db.session.commit()
            return True
        return False
    except Exception as e:
        db.session.rollback()
        print(f"Lỗi khi xóa học sinh: {e}")
        return False
    finally:
        db.session.close()

def generate_random_score():
    scores = [round(i * 0.5, 1) for i in range(2, 21)]  # Tạo danh sách [1, 1.5, ..., 10]
    return random.choice(scores)

def check_email_exists(email):
    # Truy vấn cơ sở dữ liệu để kiểm tra email
    result = db.session.query(HocSinh).filter_by(email=email).first()
    return result is not None

def check_phone_exists(so_dien_thoai):
    # Truy vấn cơ sở dữ liệu để kiểm tra số điện thoại
    result = db.session.query(HocSinh).filter_by(soDienThoai=so_dien_thoai).first()
    return result is not None


def get_most_recent_quy_dinh(loai_quy_dinh):
    Session = sessionmaker(bind=db.engine)
    session = Session()

    try:
        # Truy vấn để lấy quy định mới nhất theo loại quy định
        quy_dinh = session.query(QuyDinh).filter_by(loaiQuyDinh=loai_quy_dinh).order_by(
            QuyDinh.ngayRaQuyDinh.desc()).first()
        return quy_dinh
    finally:
        session.close()


def get_students_by_grade(grade: int) -> list:
    """
    Lấy danh sách học sinh theo khối.

    :param grade: Khối học (10, 11, 12).
    :return: Danh sách học sinh thuộc khối đã cho.
    """
    # Chuyển đổi grade thành enum Khoi
    grade_enum = Khoi(grade)

    # Sử dụng db.session để truy vấn
    students = db.session.query(HocSinh).filter(HocSinh.khoi == grade_enum).all()

    return [{
        'maHocSinh': student.maHocSinh,
        'ho': student.ho,
        'ten': student.ten,
        'ngaySinh': student.ngaySinh.strftime('%Y-%m-%d'),
        'gioiTinh': student.gioiTinh,
        'diaChi': student.diaChi,
    } for student in students]

#  hàm để lấy tất cả các kỳ học
def get_all_semesters() -> list:
    """
    Lấy danh sách tất cả các kỳ học.

    :return: Danh sách kỳ học.
    """
    semesters = db.session.query(HocKy).all()
    return [{
        'maHocKy': semester.maHocKy,
        'tenHocKy': semester.tenHocKy,
        'namHoc': semester.namHoc,
    } for semester in semesters]



def get_students_in_classes():

    # Truy vấn để lấy danh sách học sinh trong lớp
    classes = HocSinhLop.query.all()  # Lấy tất cả lớp học sinh

    # Chuyển đổi dữ liệu thành danh sách từ đối tượng
    return [
        {
            'maHocSinh': cls.maHocSinh,
            'namHoc': cls.namHoc
        }
        for cls in classes
    ]


def get_all_teachers() -> list:
    """
    Lấy tất cả giáo viên từ cơ sở dữ liệu.
    """
    teachers = db.session.query(NguoiDung).filter(NguoiDung.vaiTro == VaiTro.GIAOVIEN).all()
    return [{
        'maNguoiDung': teacher.maNguoiDung,
        'tenNguoiDung': teacher.tenNguoiDung,
    } for teacher in teachers]

# Thêm hàm để lấy giáo viên thuộc lớp có học sinh trong năm học đã chọn
def get_teachers_in_classes(selected_year):
    """
    Lấy danh sách giáo viên thuộc lớp có học sinh trong năm học đã chọn.
    """
    # Giả sử bạn có các mô hình: NguoiDung, LopHoc, HocSinh
    teachers = db.session.query(NguoiDung).join(Lop).join(HocSinhLop).filter(
        HocSinhLop.namHoc == selected_year,
        NguoiDung.vaiTro == VaiTro.GIAOVIEN
    ).distinct().all()

    return [teacher.maNguoiDung for teacher in teachers]


def search_teachers(query: str) -> list:
    """
    Tìm kiếm giáo viên dựa trên tên.
    """
    teachers = db.session.query(NguoiDung).filter(
        NguoiDung.vaiTro == VaiTro.GIAOVIEN,
        NguoiDung.tenNguoiDung.ilike(f'%{query}%')
    ).all()
    return [{
        'maNguoiDung': teacher.maNguoiDung,
        'tenNguoiDung': teacher.tenNguoiDung,
    } for teacher in teachers]



import uuid

def generate_nguoi_dung_id(vai_tro):
    prefix = ''
    if vai_tro == VaiTro.GIAOVIEN:
        prefix = 'GV'
    elif vai_tro == VaiTro.QUANTRI:
        prefix = 'QT'
    elif vai_tro == VaiTro.GIAOVU:
        prefix = 'GU'

    while True:
        user_id = f"{prefix}{str(uuid.uuid4())[:8]}".upper() # Lấy 8 ký tự đầu của UUID
        # Kiểm tra xem mã người dùng đã tồn tại hay chưa
        if not NguoiDung.query.filter_by(maNguoiDung=user_id).first():
            return user_id  # Trả về mã độc nhất

        # Nếu có trùng lặp, vòng lặp sẽ tiếp tục


def generate_ma_mon_hoc(ten_mon_hoc):
    # Lấy chữ cái đầu tiên của mỗi từ trong tên môn học
    prefix = ''.join(word[0].upper() for word in ten_mon_hoc.split())

    # Lấy số lượng môn học hiện tại và thêm 1
    count = MonHoc.query.count() + 1

    # Tạo mã môn học với định dạng như TH001
    return f"{prefix}{count:03d}"  # VD: TH001 cho Toán Học

def generate_ma_quy_dinh():
    # Tạo mã quy định theo định dạng QD + 4 ký tự ngẫu nhiên từ UUID
    return f"QD{str(uuid.uuid4().int)[:4]}"


def generate_ma_hoc_sinh():
    # Lấy năm hiện tại
    current_year_suffix = str(datetime.now().year)[-2:]  # 2 số cuối năm

    # Tìm mã học sinh lớn nhất hiện có
    max_ma_hoc_sinh = db.session.query(HocSinh.maHocSinh).filter(
        HocSinh.maHocSinh.like(f'HS{current_year_suffix}%')).order_by(HocSinh.maHocSinh.desc()).first()

    if max_ma_hoc_sinh:
        # Lấy số cuối cùng và tăng dần
        max_number = int(max_ma_hoc_sinh[0][4:])  # Lấy 4 số từ mã
        new_number = max_number + 1
    else:
        new_number = 1  # Nếu không có mã nào, bắt đầu từ 0001

    # Tạo mã học sinh mới
    return f"HS{current_year_suffix}{new_number:04d}"  # Đảm bảo có 4 chữ số


def generate_ma_hoc_ky(nam_hoc):
    # Lấy 2 số cuối của năm học
    year_suffix = nam_hoc[-2:]

    # Tìm mã kỳ học lớn nhất hiện tại cho năm học này
    max_ma_hoc_ky = db.session.query(HocKy.maHocKy).filter(HocKy.namHoc == nam_hoc).order_by(
        HocKy.maHocKy.desc()).first()

    if max_ma_hoc_ky:
        # Lấy số cuối cùng và tăng dần
        last_number = int(max_ma_hoc_ky[0][2:])  # Lấy 2 số từ mã (bỏ qua 2 số đầu)
        new_number = last_number + 1
    else:
        new_number = 1  # Nếu không có mã nào, bắt đầu từ 01

    # Tạo mã kỳ học mới
    return f"{year_suffix}{new_number:02d}"  # Đảm bảo có 2 chữ số




def generate_ma_lop(khoi):
    # Tìm các lớp hiện có cho khối này
    existing_lops = Lop.query.filter(Lop.maLop.like(f'LH{khoi.value}%')).all()

    # Nếu chưa có lớp nào, bắt đầu từ 1
    if not existing_lops:
        next_number = 1
    else:
        # Lấy số lớn nhất đã tồn tại và tăng lên 1
        existing_numbers = [int(lop.maLop[-3:]) for lop in existing_lops]
        next_number = max(existing_numbers) + 1

    # Đảm bảo số luôn có 3 chữ số
    return f"LH{khoi.value}{next_number:03}"
