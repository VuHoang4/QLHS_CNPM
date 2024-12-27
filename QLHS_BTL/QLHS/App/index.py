from App import app, login_manager, dao,db
from flask import render_template, redirect, request, jsonify, request, url_for, flash, session
from flask_login import login_user,current_user,logout_user
from App.models import NguoiDung, VaiTro,Khoi, LoaiDiem,MonHoc,HocKy,Lop,HocSinhLop,HocSinh,LopMonHoc,Diem
from datetime import date, datetime,timedelta
from werkzeug.security import hashlib
from flask_mail import Mail, Message
import os
import random
import string
import logging
from sqlalchemy.exc import SQLAlchemyError
from functools import wraps

def db_error_handler(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)  # Gọi hàm gốc
        except SQLAlchemyError as e:
            logging.error(f"Lỗi CSDL: {e}")  # Ghi log lỗi
            return redirect(url_for('error_page'))  # Chuyển hướng đến trang lỗi
    return wrapper

@app.route('/test_error')
@db_error_handler
def test_error():
    raise SQLAlchemyError("Lỗi giả lập")  # Ném ra lỗi giả lập
@app.route('/error_page')
def error_page():
    return render_template('error.html')


@app.route("/")
def index():

    # dao.add_nguoi_dung('admin', "123456", VaiTro.QUANTRI, 'Admin', 'vuhoang@gmailadmin')
    # dao.add_nguoi_dung('giaovu1', "1234", VaiTro.GIAOVU, 'Giáo vụ 1', 'vuhoang@gmailgiaovu1')
    # dao.add_nguoi_dung('giaovu2', "1234", VaiTro.GIAOVU, 'Giáo vụ 2', 'vuhoang@gmailgiaovu2')
    # dao.add_nguoi_dung('giaovien1', "1234", VaiTro.GIAOVIEN, 'Giáo viên 1', 'vuhoang@gmailgiaovien1')
    # dao.add_nguoi_dung('giaovien2', "1234", VaiTro.GIAOVIEN, 'Giáo viên 2', 'vuhoang@gmailgiaovien2')
    # dao.add_nguoi_dung('giaovien3', "1234", VaiTro.GIAOVIEN, 'Giáo viên 3', 'vuhoang@gmailgiaovien3')
    #
    # def generate_random_username():
    #     return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    #
    # def generate_random_name():
    #     first_names = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng"]
    #     last_names = ["An", "Bình", "Cường", "Đức", "Hải"]
    #     return f"{random.choice(first_names)} {random.choice(last_names)}"
    #
    # def generate_random_email(username):
    #     domains = ["gmail.com", "yahoo.com", "hotmail.com"]
    #     return f"{username}@{random.choice(domains)}"
    #
    # # Tạo 7 người dùng với vai trò giáo viên
    # for _ in range(7):
    #     ten_dang_nhap = generate_random_username()
    #     mat_khau = "1234"  # Mật khẩu mặc định
    #     vai_tro =VaiTro.GIAOVIEN  # Vai trò giáo viên
    #     ten_nguoi_dung = generate_random_name()
    #     email = generate_random_email(ten_dang_nhap)
    #     avatar = None  # Có thể thay đổi avatar nếu cần
    #
    #     dao.add_nguoi_dung(ten_dang_nhap, mat_khau, vai_tro, ten_nguoi_dung, email, avatar)
    #
    #
    # def generate_random_name():
    #     first_names = [
    #         "An", "Bình", "Cường", "Đức", "Hải", "Khoa", "Linh", "Mai", "Nam", "Oanh",
    #         "Phúc", "Quang", "Thảo", "Tú", "Vân", "Xuân"
    #     ]
    #     return random.choice(first_names)
    #
    # def generate_random_surname():
    #     surnames = [
    #         "Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Vũ", "Đỗ", "Ngô", "Bùi", "Dương",
    #         "Lý", "Đinh", "Nguyễn Văn", "Trương"
    #     ]
    #     return random.choice(surnames)
    #
    # def generate_random_email(username):
    #     domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
    #     return f"{username}@{random.choice(domains)}"
    #
    # def generate_random_phone_number():
    #     return "0" + ''.join(random.choices(string.digits, k=9))
    #
    # def generate_random_address():
    #     streets = [
    #         "Đường 1", "Đường 2", "Đường 3", "Đường 4", "Đường 5",
    #         "Đường 6", "Đường 7", "Đường 8", "Đường 9", "Đường 10"
    #     ]
    #     return f"{random.choice(streets)}, Thành phố {random.choice(['Hà Nội', 'Hồ Chí Minh', 'Đà Nẵng', 'Nha Trang', 'Cần Thơ'])}"
    #
    # def generate_random_birth_date():
    #     start_date = datetime(2005, 1, 1)
    #     end_date = datetime(2008, 12, 31)
    #     return start_date + (end_date - start_date) * random.random()
    #
    # # Tạo 500 học sinh
    # for _ in range(500):
    #     ho = generate_random_surname()
    #     ten = generate_random_name()
    #     ngay_sinh = generate_random_birth_date().date()
    #     email = generate_random_email(ho.lower() + ten.lower())
    #     gioi_tinh = random.choice(["Nam", "Nữ"])
    #     so_dien_thoai = generate_random_phone_number()
    #     dia_chi = generate_random_address()
    #     khoi = random.choice(list(Khoi))  # Chọn ngẫu nhiên khối lớp
    #
    #     dao.add_hoc_sinh(ho, ten, ngay_sinh, email, gioi_tinh, so_dien_thoai, dia_chi, khoi)



    # # Dữ liệu cần thêm
#     maMonHoc = "TH1001"
#     maHocSinh =[
#     "HS240294", "HS240297", "HS240298", "HS240299", "HS240303",
#     "HS240307", "HS240335", "HS240339", "HS240342", "HS240344",
#     "HS240345", "HS240358", "HS240359", "HS240361", "HS240365",
#     "HS240367"
# ]
#     maHocKy = "2501"
#
#     # Thêm điểm cho từng học sinh
#     for ma_hoc_sinh in maHocSinh:
#         print(f"Thêm điểm cho học sinh: {ma_hoc_sinh}")
#
#
#         # 3 điểm PHUT_15
#         for _ in range(3):
#             dao.add_diem(dao.generate_random_score(), LoaiDiem.PHUT_15, maMonHoc, ma_hoc_sinh, maHocKy)
#
#         # 2 điểm TIET_1
#         for _ in range(2):
#             dao.add_diem(dao.generate_random_score(), LoaiDiem.TIET_1, maMonHoc, ma_hoc_sinh, maHocKy)
#
#
#         # 1 điểm CUOI_KI
#         dao.add_diem(dao.generate_random_score(), LoaiDiem.CUOI_KI, maMonHoc, ma_hoc_sinh, maHocKy)
#
#     print("Đã thêm điểm thành công.")
    # # Danh sách các mã lớp
    # maLops = ['LH12001', 'LH12002']
    #
    # # Mã môn học
    # maMonHoc = 'TH1001'
    #
    # # Danh sách mã giáo viên
    # maGVBMs = ['GV0FBDBC9B', 'GV1331674F']
    #
    # # Gọi hàm để thêm cho từng mã lớp và từng giáo viên
    # for maLop in maLops:
    #     for maGVBM in maGVBMs:
    #         dao.add_mon_hoc_vao_lop(maLop, maMonHoc, maGVBM)
    # def add_diem_nhanh(ma_hoc_sinh_list, ma_mon_hoc, ma_hoc_ky, loai_diem):
    #     for ma_hoc_sinh in ma_hoc_sinh_list:
    #         # Tạo giá trị điểm ngẫu nhiên từ 1 đến 10
    #         gia_tri_diem = random.randint(1, 10)
    #         # Gọi hàm add_diem để thêm điểm
    #         dao.add_diem(gia_tri_diem, loai_diem, ma_mon_hoc, ma_hoc_sinh, ma_hoc_ky)
    #
    # # Danh sách mã học sinh
    # ma_hoc_sinh_list = [
    #     "HS240001", "HS240002", "HS240003", "HS240004",
    #     "HS240010", "HS240021", "HS240024", "HS240026",
    #     "HS240029", "HS240030", "HS240033", "HS240034",
    #     "HS240035", "HS240036", "HS240037"
    # ]
    #
    # # Thông tin về môn học, học kỳ và loại điểm
    # ma_mon_hoc = "HH1004"
    # ma_hoc_ky = "2501"
    # loai_diem = LoaiDiem.PHUT_15  # Giả sử LoaiDiem đã được định nghĩa trước đó
    #
    # # Gọi hàm để thêm điểm nhanh
    # add_diem_nhanh(ma_hoc_sinh_list, ma_mon_hoc, ma_hoc_ky, loai_diem)
    # dao.add_mon_hoc_vao_lop("LH10001",)

    if not current_user.is_authenticated:
        return redirect("/login")  # Chuyển tới trang login nếu chưa đăng nhập
    return redirect("/dashboard")  # Hiển thị trang index nếu đã đăng nhập


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        tenDangNhap = request.form['username']
        matKhau = request.form['password']


        user = dao.auth_user(username=tenDangNhap, password=matKhau)

        if user :  # Kiểm tra mật khẩu
            login_user(user)
            return redirect(url_for('dashboard'))  # Chuyển hướng đến trang dashboard

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    user_role = current_user.vaiTro

    if user_role == VaiTro.GIAOVIEN:
        current_year = datetime.now().year
        return render_template('giaovien_dashboard.html',current_year=current_year)
    elif user_role == VaiTro.GIAOVU:
        return render_template('giaovu_dashboard.html')

    return render_template('default_dashboard.html')

@app.route("/logout", methods=['get', 'post'])
def logout_process():
    logout_user()
    return redirect("/login")


@app.route("/login-admin", methods=['post'])
def login_admin_process():
    username = request.form.get('username')
    password = request.form.get('password')
    u = dao.auth_user(username=username, password=password, role=VaiTro.QUANTRI)
    if u:
        login_user(u)

    return redirect('/admin')

@login_manager.user_loader
def load_user(maNguoiDung):
    return NguoiDung.query.get(maNguoiDung)  # Lấy người dùng từ cơ sở dữ liệu theo maNguoiDung


@app.route('/user/<string:tenDangNhap>')
def user_profile(tenDangNhap):
    # Tìm người dùng theo tên đăng nhập
    user = NguoiDung.query.filter_by(tenDangNhap=tenDangNhap).first()
    if user:
        return render_template('user_profile.html', user=user)
    else:
        return "Người dùng không tồn tại", 404


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    user = current_user

    if request.method == 'POST':
        tenDangNhap = request.form['tenDangNhap']
        matKhau = request.form['matKhau']
        matKhauConfirm = request.form['matKhauConfirm']
        tenNguoiDung = request.form['tenNguoiDung']
        email = request.form['email']
        avatar = request.form['avatar']

        # Kiểm tra tính duy nhất của email
        existing_user = NguoiDung.query.filter_by(email=email).first()
        if existing_user and existing_user.maNguoiDung != user.maNguoiDung:
            flash('Email đã được sử dụng bởi người dùng khác!', 'danger')
            return redirect(url_for('edit_profile'))

            # Kiểm tra xem mật khẩu có được thay đổi không
        if matKhau and matKhau != "**********":
            # Kiểm tra khớp mật khẩu
            if matKhau != matKhauConfirm:
                flash('Hai mật khẩu không khớp, vui lòng thử lại!', 'danger')
                return redirect(url_for('edit_profile'))
            user.matKhau = hashlib.md5(matKhau.encode('utf-8')).hexdigest()  # Mã hóa mật khẩu

        # Cập nhật thông tin người dùng
        user.tenDangNhap = tenDangNhap
        user.tenNguoiDung = tenNguoiDung
        user.email = email
        user.avatar = avatar

        db.session.commit()
        flash('Thông tin của bạn đã được cập nhật!', 'success')
        return redirect(url_for('user_profile', tenDangNhap=user.tenDangNhap))

    return render_template('edit_profile.html', user=user)



# API lấy danh sách khối
@app.route('/api/khois', methods=['GET'])
def get_khois():
    khois = [k.value for k in Khoi]
    return jsonify(khois)

# API lấy danh sách lớp theo khối
# API lấy danh sách lớp theo khối
@app.route('/api/classes', methods=['GET'])
def get_classes():
    grade = request.args.get('grade', type=int)
    year = request.args.get('year', type=str)  # Lấy năm học từ tham số
    classes = db.session.query(Lop).join(HocSinhLop).filter(
        HocSinhLop.namHoc == year,
        Lop.khoi == Khoi(grade)
    ).all()
    return jsonify([{'maLop': lop.maLop, 'tenLop': lop.tenLop} for lop in classes])

# API lấy danh sách môn học
@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    maLop = request.args.get('classId', type=str)  # Lấy mã lớp từ tham số
    subjects = db.session.query(MonHoc).join(LopMonHoc).filter(LopMonHoc.maLop == maLop).all()
    return jsonify([{'maMonHoc': mon.maMonHoc, 'tenMonHoc': mon.tenMonHoc} for mon in subjects])

# API lấy danh sách học kỳ
@app.route('/api/hocky', methods=['GET'])
def get_hocky():
    year = request.args.get('year', type=str)  # Lấy năm học từ tham số
    hocky = HocKy.query.filter_by(namHoc=year).all()
    return jsonify([{'maHocKy': hk.maHocKy, 'tenHocKy': hk.tenHocKy, 'namHoc': hk.namHoc} for hk in hocky])

@app.route('/add_hoc_sinh', methods=['POST'])
def add_hoc_sinh():
    data = request.json
    ho = data.get('ho')
    ten = data.get('ten')
    ngay_sinh = data.get('ngay_sinh')
    email = data.get('email')
    gioi_tinh = data.get('gioi_tinh')
    so_dien_thoai = data.get('so_dien_thoai')
    dia_chi = data.get('dia_chi')
    khoi=Khoi(int(data.get('khoi')))
    print(khoi)

    errors = []

    # Kiểm tra email đã tồn tại chưa
    if dao.check_email_exists(email):
        errors.append("Email đã tồn tại trong cơ sở dữ liệu.")

    # Kiểm tra số điện thoại đã tồn tại chưa
    if dao.check_phone_exists(so_dien_thoai):
        errors.append("Số điện thoại đã tồn tại trong cơ sở dữ liệu.")

    # Tính tuổi từ ngày sinh
    today = datetime.today()
    ngay_sinh_date = datetime.strptime(ngay_sinh, "%Y-%m-%d")  # Định dạng ngày tháng

    age = today.year - ngay_sinh_date.year - ((today.month, today.day) < (ngay_sinh_date.month, ngay_sinh_date.day))

    # Lấy quy định tuổi tối thiểu và tối đa mới nhất
    quy_dinh_toi_thieu = dao.get_most_recent_quy_dinh("TUOI_TOI_THIEU")
    quy_dinh_toi_da = dao.get_most_recent_quy_dinh("TUOI_TOI_DA")

    # Kiểm tra quy định tuổi tối thiểu
    if quy_dinh_toi_thieu and age < quy_dinh_toi_thieu.giaTri:
        errors.append(f"Tuổi tối thiểu là {quy_dinh_toi_thieu.giaTri}.")

    # Kiểm tra quy định tuổi tối đa
    if quy_dinh_toi_da and age > quy_dinh_toi_da.giaTri:
        errors.append(f"Tuổi tối đa là {quy_dinh_toi_da.giaTri}.")

    # Nếu có lỗi, trả về thông báo lỗi
    if errors:
        return jsonify({"errors": errors}), 400

    # Nếu không có lỗi, thêm học sinh vào DB
    dao.add_hoc_sinh(ho, ten, ngay_sinh, email, gioi_tinh, so_dien_thoai, dia_chi,khoi)

    return jsonify({"message": "Học sinh đã được thêm thành công!"}), 201


# api get HocSinh
@app.route('/api/students', methods=['GET'])
def get_students():
    grade = request.args.get('grade', type=int)
    year = request.args.get('year', type=str)  # Lấy năm học từ tham số
    # print(year)

    if grade in [10, 11, 12]:
        # Lấy danh sách học sinh theo khối
        students = dao.get_students_by_grade(grade)

        # Lấy danh sách mã học sinh trong lớp học sinh
        lophocsinh = dao.get_students_in_classes()  # Giả sử đây là hàm lấy dữ liệu lớp học sinh
        maHocSinh_lophoc = {student['maHocSinh'] for student in lophocsinh}  # Tạo tập hợp mã học sinh trong lớp

        # Lọc học sinh
        filtered_students = []
        for student in students:
            if student['maHocSinh'] not in maHocSinh_lophoc:
                filtered_students.append(student)
            else:
                # Kiểm tra năm học
                student_class_year = next(
                    (cls['namHoc'] for cls in lophocsinh if cls['maHocSinh'] == student['maHocSinh']), None)
                if student_class_year != year:
                    filtered_students.append(student)

        return jsonify(filtered_students)

    return jsonify([])

# API Để Lấy Kỳ Học
@app.route('/api/semesters', methods=['GET'])
def get_semesters():
    semesters = dao.get_all_semesters()  # Lấy tất cả kỳ học từ cơ sở dữ liệu
    return jsonify(semesters)

# API Để Lấy Giáo Viên
@app.route('/api/teachers', methods=['GET'])
def get_teachers():
    selected_year = request.args.get('year',  type=str)  # Lấy năm học từ yêu cầu
    print('nam: ')
    print(selected_year)

    # Lấy danh sách giáo viên không thuộc lớp có học sinh trong năm học đã chọn
    teachers_in_classes = dao.get_teachers_in_classes(selected_year)

    # Lấy tất cả giáo viên
    teachers = dao.get_all_teachers()

    # Lọc giáo viên
    filtered_teachers = [teacher for teacher in teachers if teacher['maNguoiDung'] not in teachers_in_classes]

    return jsonify(filtered_teachers)




# 3 API để Luu trong LapDSLop
@app.route('/api/lop', methods=['POST'])
def add_lop_api():
    data = request.json
    try:
        maLop = dao.generate_ma_lop(Khoi(int(data['khoi'])))

        # Lấy quy định sĩ số tối đa mới nhất
        quy_dinh_si_so_toi_da = dao.get_most_recent_quy_dinh("SI_SO_TOI_DA")
        print(quy_dinh_si_so_toi_da.giaTri)

        # Kiểm tra quy định sĩ số
        siSo = int(data['siSo'])
        print(siSo)
        errors = []

        if quy_dinh_si_so_toi_da and siSo > quy_dinh_si_so_toi_da.giaTri:
            errors.append(f"Sĩ số tối đa là {quy_dinh_si_so_toi_da.giaTri}.")

        if errors:
            return jsonify({'errors': errors}), 400  # Trả về mã lỗi 400 nếu có lỗi

        # Gọi hàm add_lop đã có
        dao.add_lop(
            maLop=maLop,
            tenLop=data['tenLop'],
            siSo=siSo,
            khoi=Khoi(int(data['khoi'])),
            maGVCN=data.get('maGVCN')
        )

        return jsonify({'maLop': maLop, 'message': 'Lớp đã được thêm thành công.'}), 201
    except Exception as e:
        logging.error(f"Lỗi khi thêm lớp: {str(e)}")
        return jsonify({'message': 'Đã xảy ra lỗi, vui lòng thử lại.'}), 500


@app.route('/api/hoc-ky', methods=['POST'])
def add_hoc_ky_api():
    data = request.json
    try:
        # Kiểm tra xem học kỳ đã tồn tại
        existing_semester = HocKy.query.filter_by(namHoc=data['nam_hoc'], tenHocKy=data['ten_hoc_ky']).first()
        if existing_semester:
            return jsonify({'message': 'Kỳ học đã tồn tại.'}), 409  # 409 Conflict

        # Gọi hàm để thêm kỳ học
        dao.add_hoc_ky(
            ten_hoc_ky=data['ten_hoc_ky'],
            nam_hoc=data['nam_hoc']
        )
        return jsonify({'message': 'Kỳ học đã được thêm thành công.'}), 201
    except Exception as e:
        logging.error(f"Lỗi khi thêm kỳ học: {str(e)}")
        return jsonify({'message': 'Đã xảy ra lỗi, vui lòng thử lại.'}), 500


@app.route('/api/hoc-sinh-lop', methods=['POST'])
def add_hoc_sinh_vao_lop_api():
    data = request.json
    maHocSinh = data['maHocSinh']
    maLop = data['maLop']
    namHoc=data['namHoc']
    print(maLop)

    # Gọi hàm đã có để thêm học sinh vào lớp
    try:
        existing_record = HocSinhLop.query.filter_by(maHocSinh=maHocSinh, maLop=maLop, namHoc=namHoc).first()
        if existing_record:
            logging.warning(f"Học sinh {maHocSinh} đã được ghi danh vào lớp {maLop} trong kỳ học {namHoc}.")
            return jsonify({
                               'message': f'Học sinh {maHocSinh} đã được ghi danh vào lớp {maLop} trong kỳ học {namHoc}.'}), 409  # 409 Conflict

        dao.add_hoc_sinh_vao_lop(maHocSinh, maLop,namHoc)  # Gọi hàm đã có
        return jsonify({'message': 'Học sinh đã được thêm vào lớp'}), 201

    except Exception as e:
        logging.error(f"Lỗi khi thêm học sinh vào lớp: {str(e)}")
        return jsonify({'message': 'Đã xảy ra lỗi, vui lòng thử lại.'}), 500

#QLHS
@app.route('/api/manage_students', methods=['GET'])
def get_manage_students():
    student_id = request.args.get('studentId')
    print(student_id)

    # Tìm kiếm học sinh theo mã học sinh
    student = HocSinh.query.filter_by(maHocSinh=student_id).first()
    print(student.email)

    if student:
        return jsonify({
            'maHocSinh': student.maHocSinh,
            'ho': student.ho,
            'ten': student.ten,
            'ngaySinh': student.ngaySinh.strftime('%Y-%m-%d'),  # Chuyển đổi định dạng ngày
            'email': student.email,
            'gioiTinh': student.gioiTinh,
            'soDienThoai': student.soDienThoai,
            'diaChi': student.diaChi,
            'khoi': student.khoi.value
        })
    else:
        return jsonify({'message': 'Không tìm thấy học sinh1.'}), 404

@app.route('/api/update_students', methods=['POST'])
def update_students():
    updated_students = request.json
    for student_data in updated_students:
        student = HocSinh.query.filter_by(maHocSinh=student_data['maHocSinh']).first()
        if student:
            student.ho = student_data['ho']
            student.ten = student_data['ten']
            student.ngaySinh = student_data['ngaySinh']
            student.email = student_data['email']
            student.gioiTinh = student_data['gioiTinh']
            student.soDienThoai = student_data['soDienThoai']
            student.diaChi = student_data['diaChi']
            db.session.commit()
    return jsonify({'status': 'success'})
# HET QLHS

#
@app.route('/api/list_classes', methods=['GET'])
def list_classes():
    academic_year = request.args.get('academicYear')
    grade = request.args.get('grade')

    try:
        # Lấy danh sách lớp theo năm học và khối
        classes = db.session.query(Lop).join(HocSinhLop).filter(
            HocSinhLop.namHoc == academic_year,
            Lop.khoi == Khoi(int(grade))
        ).all()

        result = [{'maLop': c.maLop, 'tenLop': c.tenLop, 'siSo': c.siSo} for c in classes]
        return jsonify(result)
    finally:
        db.session.close()

@app.route('/api/class/<class_id>', methods=['GET'])
def get_class_details(class_id):
    try:
        class_data = db.session.query(Lop).filter(Lop.maLop == class_id).first()
        if not class_data:
            return jsonify({'error': 'Class not found'}), 404

        students = db.session.query(HocSinhLop).filter(HocSinhLop.maLop == class_id).all()
        student_details = [
            {
                'maHocSinh': s.maHocSinh,
                'ho': db.session.query(HocSinh).filter(HocSinh.maHocSinh == s.maHocSinh).first().ho,
                'ten': db.session.query(HocSinh).filter(HocSinh.maHocSinh == s.maHocSinh).first().ten
            }
            for s in students
        ]

        return jsonify({
            'tenLop': class_data.tenLop,
            'siSo': class_data.siSo,
            'hocSinh': student_details
        })
    finally:
        db.session.close()

@app.route('/api/delete_student', methods=['POST'])
def remove_student():
    data = request.json
    student_id = data.get('studentId')
    class_id = data.get('classId')
    try:
        if dao.delete_hoc_sinh(student_id, class_id):
            # Cập nhật sĩ số của lớp
            class_data = db.session.query(Lop).filter(Lop.maLop == class_id).first()
            if class_data:
                class_data.siSo -= 1  # Giảm sĩ số đi 1
                db.session.commit()
            return jsonify({'message': 'Học sinh đã được xóa thành công.'}), 200
        return jsonify({'error': 'Học sinh không tồn tại trong lớp.'}), 404
    except Exception as e:
        db.session.rollback()  # Hoàn tác nếu có lỗi
        return jsonify({'error': str(e)}), 500
    finally:
        db.session.close()


@app.route('/api/add_student', methods=['POST'])
def add_student():
    data = request.json
    required_fields = ['maHocSinh', 'tenLop']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Thiếu thông tin cần thiết.'}), 400


    session = db.session
    maHocSinh = data['maHocSinh']
    tenLop = data['tenLop']
    maLop=session.query(Lop).filter(Lop.tenLop == tenLop).first().maLop
    print(maHocSinh)
    print(tenLop)
    print(maLop)
    try:
        # Lấy thông tin lớp
        class_data = session.query(Lop).filter(Lop.maLop == maLop).first()
        if not class_data:
            return jsonify({'error': 'Lớp không tồn tại.'}), 404

        # Lấy năm học từ bảng HocSinhLop
        hoc_sinh_lop_data = session.query(HocSinhLop).filter(HocSinhLop.maLop == maLop).first()
        if not hoc_sinh_lop_data:
            return jsonify({'error': 'Không tìm thấy thông tin năm học cho lớp này.'}), 404

        namHoc = hoc_sinh_lop_data.namHoc  # Lấy năm học từ bản ghi đầu tiên
        # Kiểm tra xem học sinh đã có trong lớp chưa
        existing_record = session.query(HocSinhLop).filter(
            HocSinhLop.maHocSinh == maHocSinh,
            HocSinhLop.maLop == maLop,
            HocSinhLop.namHoc == namHoc
        ).first()

        if existing_record:
            return jsonify({'message': 'Học sinh đã có trong lớp.'}), 400  # Trả về thông báo nếu đã có

        # Thêm học sinh vào lớp
        dao.add_hoc_sinh_vao_lop(maHocSinh, maLop, namHoc)

        # Cập nhật sĩ số của lớp
        class_data.siSo += 1
        session.commit()

        return jsonify({'classId':maLop,'message': 'Học sinh đã được thêm vào lớp thành công.'}), 201
    except Exception as e:
        session.rollback()  # Hoàn tác nếu có lỗi
        return jsonify({'error': 'Có lỗi xảy ra khi thêm học sinh: ' + str(e)}), 500
    finally:
        session.close()


@app.route('/api/update_class_name', methods=['POST'])
def update_class_name():
    data = request.get_json()
    old_class_name = data.get('oldClassName')
    new_class_name = data.get('newClassName')

    # Tìm lớp theo tên cũ
    class_to_update = db.session.query(Lop).filter_by(tenLop=old_class_name).first()

    if class_to_update:
        # Cập nhật tên lớp
        class_to_update.tenLop = new_class_name
        db.session.commit()  # Lưu thay đổi vào cơ sở dữ liệu
        return jsonify({'class_id':class_to_update.maLop,'message': 'Tên lớp đã được cập nhật.'}), 200
    else:
        return jsonify({'message': 'Không tìm thấy lớp với tên đã cho.'}), 404

@app.route('/api/report', methods=['GET'])
def get_report():
    nam_hoc = request.args.get('namHoc')
    khoi = request.args.get('khoi')
    hoc_ky = request.args.get('hocky')
    mon_hoc = request.args.get('monhoc')

    query = db.session.query(LopMonHoc).join(Lop).join(HocSinhLop).filter(
        LopMonHoc.maMonHoc==mon_hoc,
        HocSinhLop.namHoc==nam_hoc
    ).all()

    report_data = []

    for lop_mon in query:
        # Lấy thông tin lớp từ mã lớp
        lop_info = db.session.query(Lop).filter_by(maLop=lop_mon.maLop).first()
        ten_lop = lop_info.tenLop if lop_info else "Không xác định"  # Lấy tên lớp

        hoc_sinh_list = db.session.query(HocSinhLop).filter_by(maLop=lop_mon.maLop, namHoc=nam_hoc).all()
        si_so = len(hoc_sinh_list)
        count_passed = 0  # Số học sinh đạt

        for hoc_sinh in hoc_sinh_list:
            diem_hs = db.session.query(Diem).filter_by(maHocSinh=hoc_sinh.maHocSinh, maHocKy=hoc_ky,
                                                       maMonHoc=mon_hoc).all()
            # Kiểm tra xem có điểm nào rỗng không
            if not diem_hs:
                return jsonify({'error': 'Tồn tại học sinh trong ít nhất 1 lớp chưa có điểm của môn học này, không thể lập báo cáo'}), 400

            average_score = calculate_average_score(diem_hs)  # Tính điểm trung bình cho học sinh

            if average_score >= 5:
                count_passed += 1  # Tăng số học sinh đạt

        ti_le = (count_passed / si_so * 100) if si_so > 0 else 0  # Tính tỷ lệ đạt

        report_data.append({
            'stt': len(report_data) + 1,
            'lop': ten_lop,  # Gán tên lớp vào đây
            'siSo': si_so,
            'soLuongDat': count_passed,
            'tiLe': ti_le
        })

    db.session.close()
    return jsonify(report_data)

# Hàm tính điểm trung bình
def calculate_average_score(diem_list):
    total_score = 0
    total_coefficient = 0

    for diem in diem_list:
        coefficient = 0

        # Kiểm tra xem diem là đối tượng Diem hay từ điển
        if isinstance(diem, Diem):  # Nếu diem là đối tượng Diem
            loai_diem = diem.loaiDiem
            gia_tri_diem = diem.giaTriDiem
        elif isinstance(diem, dict):  # Nếu diem là từ điển
            loai_diem = diem.get('loaiDiem')
            loai_diem=LoaiDiem(loai_diem)
            print(loai_diem)
            gia_tri_diem = diem.get('giaTriDiem')
            print(gia_tri_diem)
        else:
            continue  # Bỏ qua nếu không phải là đối tượng Diem hoặc từ điển

        # Tính hệ số
        if loai_diem == LoaiDiem.PHUT_15:
            coefficient = 1
        elif loai_diem == LoaiDiem.TIET_1:
            coefficient = 2
        elif loai_diem == LoaiDiem.CUOI_KI:
            coefficient = 3

        total_score += gia_tri_diem * coefficient
        total_coefficient += coefficient

    return total_score / total_coefficient if total_coefficient > 0 else 0  # Tránh chia cho 0

# admin-LopMonHoc
# GiaoVien-Them Diem
@app.route('/get_classes/<maNguoiDung>', methods=['GET'])
def fetch_classes(maNguoiDung):  # Đổi tên hàm ở đây
    current_year = datetime.now().year
    nam_hoc_list = [
        f"{current_year}-{current_year + 1}"  # Năm hiện tại và năm kế tiếp
    ]
    # Lấy danh sách lớp mà giáo viên đã dạy
    classes = db.session.query(Lop).join(LopMonHoc).join(HocSinhLop).filter(
        LopMonHoc.maGVBM == maNguoiDung,
        HocSinhLop.namHoc==nam_hoc_list
    ).all()

    # Chuyển đổi danh sách lớp thành định dạng JSON
    class_list = {lop.maLop: lop.tenLop for lop in classes}

    return jsonify(class_list)


@app.route('/fetch_subjects', methods=['GET'])
def fetch_subjects():
    ma_nguoi_dung = current_user.maNguoiDung
    maLop = request.args.get('maLop')

    subjects = db.session.query(MonHoc).join(LopMonHoc).filter(
        LopMonHoc.maGVBM==ma_nguoi_dung,
        LopMonHoc.maLop==maLop
    ).all()
    return jsonify([{'maMonHoc': subject.maMonHoc, 'tenMonHoc': subject.tenMonHoc} for subject in subjects])


@app.route('/fetch_semesters/<string:nam_hoc>', methods=['GET'])
def fetch_semesters(nam_hoc):
    semesters = HocKy.query.filter_by(namHoc=nam_hoc).all()
    return jsonify([
        {'maHocKy': semester.maHocKy, 'tenHocKy': semester.tenHocKy}
        for semester in semesters
    ])


@app.route('/fetch_students/<string:maLop>', methods=['GET'])
def fetch_students(maLop):
    # Lấy danh sách học sinh theo mã lớp
    students = db.session.query(HocSinhLop, HocSinh).join(HocSinh).filter(HocSinhLop.maLop == maLop).all()

    # Lấy tên lớp từ bảng Lop
    tenLop = db.session.query(Lop.tenLop).filter(Lop.maLop == maLop).scalar()

    # Chuyển đổi dữ liệu thành định dạng JSON
    student_list = [
        {
            'maHocSinh': student[0].maHocSinh,
            'tenHocSinh': f"{student[1].ho} {student[1].ten}",  # Kết hợp họ và tên
            'email': student[1].email  # Email
        } for student in students
    ]

    # Trả về danh sách học sinh cùng với tên lớp
    return jsonify({'tenLop': tenLop, 'students': student_list})



@app.route('/fetch_points', methods=['POST'])
def fetch_points():
    data = request.json
    maMonHoc = data.get('maMonHoc')
    maHocKy = data.get('maHocKy')
    maHocSinhs = data.get('maHocSinhs')  # Danh sách mã học sinh

    diem_records = Diem.query.filter(
        Diem.maMonHoc == maMonHoc,
        Diem.maHocKy == maHocKy,
        Diem.maHocSinh.in_(maHocSinhs)
    ).all()

    points = [
        {
            'maHocSinh': d.maHocSinh,
            'loaiDiem': d.loaiDiem.value,
            'soThuTuDiem': d.soThuTuDiem,
            'diem': d.giaTriDiem
        }
        for d in diem_records
    ]
    return jsonify(points)

@app.route('/add_diem', methods=['POST'])
def add_diem_route():
    data = request.json
    gia_tri_diem = data.get('gia_tri_diem')
    loai_diem = data.get('loai_diem')
    ma_mon_hoc = data.get('ma_mon_hoc')
    ma_hoc_sinh = data.get('ma_hoc_sinh')
    ma_hoc_ky = data.get('ma_hoc_ky')

    # Gọi hàm lưu điểm
    try:
        dao.add_diem(gia_tri_diem, LoaiDiem(loai_diem), ma_mon_hoc, ma_hoc_sinh, ma_hoc_ky)
        return jsonify({'message': 'Điểm đã được lưu thành công!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/fetch_hoc_ky/<namHoc>')
def fetch_hoc_ky(namHoc):
    hocKys = HocKy.query.filter_by(namHoc=namHoc).all()  # Lấy tất cả kỳ học
    return jsonify([{'maHocKy': hk.maHocKy} for hk in hocKys]) if hocKys else jsonify({'error': 'Not found'}), 404


@app.route('/fetch_scores/<maHocSinh>/<maHocKy>/<maMonHoc>')
def fetch_scores(maHocSinh, maHocKy, maMonHoc):
    diem_list = Diem.query.filter_by(maHocSinh=maHocSinh, maHocKy=maHocKy, maMonHoc=maMonHoc).all()
    return jsonify([diem.to_dict() for diem in diem_list])  # Sử dụng phương thức to_dict()

@app.route('/calculate_average', methods=['POST'])
def calculate_average():
    data = request.json
    diem_list = data.get('diemList', [])
    # In giá trị diem_list để kiểm tra
    print("Diem List:", diem_list)
    result = [{
        'maMonHoc': diem['maMonHoc'],
        'maHocSinh': diem['maHocSinh'],
        'maHocKy': diem['maHocKy'],
        'soThuTuDiem': diem['soThuTuDiem'],
        'giaTriDiem': diem['giaTriDiem'],
        'loaiDiem': diem['loaiDiem']  # Chuyển đổi về enum
    } for diem in diem_list]
    average_score = calculate_average_score(result)
    print('DiemTB :')
    print(average_score)
    return jsonify({'average_score': average_score})

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '2251050081vu@ou.edu.vn'  # Thay bằng email của bạn
app.config['MAIL_PASSWORD'] = 'VukhungconghoanG040528'  # Thay bằng mật khẩu của bạn
app.config['MAIL_DEFAULT_SENDER'] = '2251050081vu@ou.edu.vn'

mail = Mail(app)

@app.route('/send_email', methods=['POST'])
def send_email():
    pdf_file = request.files['pdf']
    recipient_email = request.form['email']
    message_body = request.form['message']  # Nhận thông điệp từ request

    msg = Message("Danh sách học sinh", recipients=[recipient_email])
    msg.body = message_body  # Sử dụng thông điệp tùy chỉnh
    msg.attach(pdf_file.filename, pdf_file.content_type, pdf_file.read())

    try:
        mail.send(msg)
        return jsonify({"message": "Email đã được gửi thành công!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        from App import admin
        app.run(debug=True,port=9999)
