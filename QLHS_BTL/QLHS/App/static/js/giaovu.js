function showContent(contentId) {
    // Ẩn giao diện mặc định
    document.getElementById('default-view').style.display = 'none';

    // Ẩn tất cả các nội dung
    const contentItems = document.querySelectorAll('.content-item');
    contentItems.forEach(item => {
        item.style.display = 'none';
    });

    // Hiển thị nội dung tương ứng
    document.getElementById(contentId).style.display = 'block';
    // Gọi fetchClasses nếu là nội dung "enter-grades"
    if (contentId === 'enter-grades') {
        fetchClasses();//Ben Giao Vien
        const academicYearEl = document.getElementById('academicYear');
        // Lấy năm học từ span
        const namHoc = academicYearEl.textContent.trim();

        // Gọi hàm loadSemesters
        loadSemesters(namHoc);
    }

}

//TNHS- Luu
document.getElementById('student-fill-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Ngăn chặn gửi form mặc định

    // Lấy dữ liệu từ biểu mẫu
    const fullName = document.getElementById('fullName').value.trim();
    const nameParts = fullName.split(' '); // Tách thành mảng từ

    // Lấy tên (từ cuối cùng)
    const ten = nameParts.pop(); // Lấy từ cuối cùng làm tên
    // Lấy họ (các từ còn lại)
    const ho = nameParts.join(' '); // Nối các phần tử còn lại để tạo thành họ

    const ngay_sinh = document.getElementById('dob').value;
    const email = document.getElementById('email').value;
    const gioi_tinh = document.querySelector('input[name="gender"]:checked').value;
    const so_dien_thoai = document.getElementById('phone').value;
    const dia_chi = document.getElementById('address').value;
    const khoi = document.getElementById('grade-level').value; // Lấy giá trị khối

    // Gửi yêu cầu tới server
    fetch('/add_hoc_sinh', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            ho: ho, // Đã thêm ho vào đây
            ten: ten, // Đã thêm ten vào đây
            ngay_sinh: ngay_sinh,
            email: email,
            gioi_tinh: gioi_tinh,
            so_dien_thoai: so_dien_thoai,
            dia_chi: dia_chi,
            khoi: khoi // Thêm khối vào đây
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errorData => {
                console.error('Errors:', errorData.errors);
                alert(errorData.errors.join(' ; ')); // Hiển thị thông báo lỗi
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.errors) {
            alert(data.errors.join(', ')); // Hiển thị thông báo lỗi
        } else {
            // Hiển thị thông tin học sinh
            document.getElementById('student-fullname').innerText = fullName; // Sửa 'fullname' thành 'fullName'
            document.getElementById('student-gender').innerText = gioi_tinh;
            document.getElementById('student-dob').innerText = ngay_sinh;
            document.getElementById('student-address').innerText = dia_chi; // Nếu cần
            document.getElementById('student-phone').innerText = so_dien_thoai;
            document.getElementById('student-email').innerText = email;
            document.getElementById('student-grade').innerText = khoi; // Hiển thị khối

            // Ẩn form và hiển thị thông tin học sinh
            document.getElementById('receive-student').style.display = 'none';
            document.getElementById('student-info').style.display = 'block';
        }
    })
    .catch(error => {
        console.error('Lỗi:', error);
    });
});

// Hàm reset form TNHS
function resetForm() {
    document.getElementById('student-fill-form').reset();
    document.getElementById('student-info').style.display = 'none';
    document.getElementById('receive-student').style.display = 'block';
}


////////////////////////-----------
// Chỉ cho phép nhập ký tự chữ cho ô tên, TNHS
document.getElementById('fullName').addEventListener('input', function() {
    this.value = this.value.replace(/[^a-zA-ZÀ-ỹ\s]/g, '');
});

// Chỉ cho phép nhập số cho ô số điện thoại, TNHS
document.getElementById('phone').addEventListener('input', function() {
    this.value = this.value.replace(/[^0-9]/g, ''); // Xóa ký tự không phải số
});


// Chặn dán nội dung không hợp lệ
document.getElementById('fullName').addEventListener('paste', function(event) {
    event.preventDefault(); // Ngăn chặn hành động dán
    const pastedData = (event.clipboardData || window.clipboardData).getData('text');
    const validData = pastedData.replace(/[^a-zA-ZÀ-ỹ\s]/g, '');
    this.value += validData; // Chỉ dán dữ liệu hợp lệ
});

document.getElementById('phone').addEventListener('paste', function(event) {
    event.preventDefault(); // Ngăn chặn hành động dán
    const pastedData = (event.clipboardData || window.clipboardData).getData('text');
    const validData = pastedData.replace(/[^0-9]/g, '');
    this.value += validData; // Chỉ dán dữ liệu hợp lệ
});





//dsLop-GiaoVien
function  loadValidTeacher() {
    const searchInput = document.getElementById('teacher-search');
    const teacherDropdown = document.getElementById('teacher-dropdown');
    const teacherList = document.getElementById('teacher-list');

    // Hàm nạp tất cả giáo viên vào dropdown
    function loadTeachers() {
         const selectedYear = document.getElementById('year-input').value; // Lấy năm học được chọn

            fetch(`/api/teachers?year=${selectedYear}`) // Gửi năm học cùng với yêu cầu
                .then(response => response.json())
                .then(data => {
                    const teacherList = document.getElementById('teacher-list'); // Đảm bảo đã định nghĩa teacherList
                    teacherList.innerHTML = ''; // Xóa nội dung cũ trước khi thêm mới
                    data.forEach(teacher => {
                        const option = document.createElement('option');
                        option.value = teacher.maNguoiDung;
                        option.textContent = teacher.tenNguoiDung;
                        teacherList.appendChild(option);
                    });
                })
                .catch(error => console.error('Error fetching teachers:', error));
    }

    // Nạp giáo viên khi trang được tải
    loadTeachers();

    searchInput.addEventListener('input', function() {
        const filter = searchInput.value.toLowerCase();
        teacherDropdown.innerHTML = ''; // Xóa nội dung dropdown
        teacherDropdown.style.display = 'none'; // Ẩn dropdown mặc định

        // Lọc các tùy chọn trong select
        const options = Array.from(teacherList.options).slice(1); // Bỏ qua option đầu tiên

        if (filter) {
            const filteredOptions = options.filter(option => option.text.toLowerCase().includes(filter));
            if (filteredOptions.length > 0) {
                filteredOptions.forEach(option => {
                    const dropdownItem = document.createElement('div');
                    dropdownItem.className = 'dropdown-item';
                    dropdownItem.textContent = option.text;
                    dropdownItem.dataset.value = option.value; // Lưu giá trị

                    dropdownItem.addEventListener('click', function() {
                        searchInput.value = option.text; // Cập nhật ô tìm kiếm
                        teacherDropdown.style.display = 'none'; // Ẩn dropdown
                        teacherList.value = option.value; // Cập nhật select
                    });

                    teacherDropdown.appendChild(dropdownItem);
                });
                teacherDropdown.style.display = 'block'; // Hiển thị dropdown
            }
        }
    });

    // Đặt ô tìm kiếm về chuỗi rỗng khi thay đổi select
    teacherList.addEventListener('change', function() {
        searchInput.value = ''; // Đặt ô tìm kiếm về chuỗi rỗng
        teacherDropdown.innerHTML = ''; // Xóa nội dung dropdown
        teacherDropdown.style.display = 'none'; // Ẩn dropdown
    });

    // Ẩn dropdown khi click ra ngoài
    document.addEventListener('click', function(event) {
        if (!teacherDropdown.contains(event.target) && event.target !== searchInput) {
            teacherDropdown.style.display = 'none';
        }
    });
}
//het nap GV

//dsLop- Khoi -HS
// Biến toàn cục
const studentsPerPage = 10;
let currentPage = 1;
let students = [];
let selectedStudents = []; // Mảng lưu trạng thái của các checkbox

document.getElementById('grade-level1').addEventListener('change', fetchStudents);
document.getElementById('year-input').addEventListener('change', function () {
    fetchStudents(); // Gọi hàm fetchStudents
    loadValidTeacher();  // Gọi thêm hàm loadValidTeacher
});
 // Lắng nghe sự kiện thay đổi năm học

function fetchStudents() {
    const selectedGrade = document.getElementById('grade-level1').value;
    const yearInput = document.getElementById('year-input').value; // Lấy năm học từ ô nhập
    const studentList = document.getElementById('student-list');
    studentList.innerHTML = '';
    students = [];
    selectedStudents = []; // Reset trạng thái checkbox
    currentPage = 1;

    // Kiểm tra xem cả khối và năm học đã được chọn chưa
    if (selectedGrade && yearInput) {
//        const tableStudents = document.getElementById('table-list-student');
//        tableStudents.style.display = 'block'; // Hiển thị dropdown


        fetch(`/api/students?grade=${selectedGrade}&year=${yearInput}`) // Gọi API với khối và năm học
            .then(response => response.json())
            .then(data => {
                students = data;
                renderStudents();
                renderPagination();
                updateSelectedCount(); // Cập nhật số dòng được chọn
            })
            .catch(error => console.error('Error fetching students:', error));
    }
}

function renderStudents() {
    const studentList = document.getElementById('student-list');
    studentList.innerHTML = '';

    const startIndex = (currentPage - 1) * studentsPerPage;
    const endIndex = Math.min(startIndex + studentsPerPage, students.length);

    // Hiển thị danh sách học sinh
    for (let i = startIndex; i < endIndex; i++) {
        const student = students[i];
        const checked = selectedStudents[i] ? 'checked' : ''; // Kiểm tra trạng thái checkbox
        const rowNumber = i + 1; // Tính số thứ tự toàn cục

        const row = `<tr>
                        <td><input type="checkbox" class="student-checkbox" data-index="${i}" ${checked}></td>
                        <td class="row-number">${rowNumber}</td>
                        <td>${student.ho} ${student.ten}</td>
                        <td>${student.ngaySinh}</td>
                        <td>${student.gioiTinh}</td>
                        <td>${student.diaChi}</td>
                     </tr>`;
        studentList.innerHTML += row;
    }

    // Thêm các hàng trống
    const emptyRows = studentsPerPage - (endIndex - startIndex);
    for (let i = 0; i < emptyRows; i++) {
        const emptyRow = `<tr class="empty-row">
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                            <td></td>
                         </tr>`;
        studentList.innerHTML += emptyRow;
    }

    // Thêm checkbox "Chọn tất cả" ở cuối bảng
    const selectAllCheckbox = `<tr>
                                  <td><input type="checkbox" id="select-all"></td>
                                  <td colspan="5"><strong>Chọn tất cả</strong></td>
                                </tr>`;
    studentList.innerHTML += selectAllCheckbox;

    // Lắng nghe sự kiện cho các checkbox
    const checkboxes = document.querySelectorAll('.student-checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const index = this.dataset.index;
            selectedStudents[index] = this.checked; // Cập nhật trạng thái checkbox
            updateSelectedCount(); // Cập nhật số dòng được chọn
        });
    });

    // Lắng nghe sự kiện cho checkbox "Chọn tất cả"
    const selectAll = document.getElementById('select-all');
    if (selectAll) {
        selectAll.addEventListener('change', function() {
            const isChecked = this.checked;
            checkboxes.forEach(checkbox => {
                checkbox.checked = isChecked; // Cập nhật tất cả checkbox
                const index = checkbox.dataset.index;
                selectedStudents[index] = isChecked; // Cập nhật trạng thái trong mảng
            });
            updateSelectedCount(); // Cập nhật số dòng được chọn
        });
    }
}

function updateSelectedCount() {
    const count = selectedStudents.filter(Boolean).length; // Đếm số checkbox được chọn
    document.getElementById('count').innerText = count; // Cập nhật số lượng vào thẻ hiển thị
}

function renderPagination() {
    const pagination = document.getElementById('pagination');
    pagination.innerHTML = '';

    const totalPages = Math.ceil(students.length / studentsPerPage);

    const createButton = (text, page) => {
        const button = document.createElement('button');
        button.innerText = text;
        button.onclick = () => {
            currentPage = page;
            renderStudents();
            renderPagination();
            updateSelectedCount(); // Cập nhật số dòng được chọn
        };
        return button;
    };

    if (totalPages <= 1) return;

    // Nút trang đầu
    if (currentPage > 1) {
        pagination.appendChild(createButton('«', 1));
    }

    // Nút trang trước
    if (currentPage > 1) {
        pagination.appendChild(createButton('‹', currentPage - 1));
    }

    // Hiển thị các trang
    const pageRange = 2; // Số lượng trang hiển thị xung quanh trang hiện tại
    const startPage = Math.max(1, currentPage - pageRange);
    const endPage = Math.min(totalPages, currentPage + pageRange);

    if (startPage > 1) {
        pagination.appendChild(createButton('1', 1));
        if (startPage > 2) {
            const dots = document.createElement('span');
            dots.className = 'dots';
            dots.innerText = '...';
            pagination.appendChild(dots);
        }
    }

    for (let i = startPage; i <= endPage; i++) {
        const button = createButton(i, i);
        if (i === currentPage) {
            button.classList.add('active');
        }
        pagination.appendChild(button);
    }

    if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
            const dots = document.createElement('span');
            dots.className = 'dots';
            dots.innerText = '...';
            pagination.appendChild(dots);
        }
        pagination.appendChild(createButton(totalPages, totalPages));
    }

    // Nút trang tiếp theo
    if (currentPage < totalPages) {
        pagination.appendChild(createButton('›', currentPage + 1));
    }

    // Nút trang cuối
    if (currentPage < totalPages) {
        pagination.appendChild(createButton('»', totalPages));
    }
}

// Xử lý sự kiện lưu lớp học
document.getElementById('FormCreateClass').addEventListener('submit', async function(event) {
    event.preventDefault();

        // Hiển thị hộp thoại xác nhận
    const confirmed = confirm("Bạn có chắc chắn muốn lập danh sách lớp này không?");

    // Nếu người dùng không xác nhận, dừng lại
    if (!confirmed) {
        return;
    }
    const className = document.getElementById('class-name').value;
    const gradeLevel = document.getElementById('grade-level1').value;
    const yearInput = document.getElementById('year-input').value;
    const teacherSelect = document.getElementById('teacher-list');
    const teacherValue = teacherSelect.value;
    const totalSelected = selectedStudents.filter(Boolean).length; // Đếm số học sinh đã chọn

    const errorMessages = [];

    const newClassData = {
        tenLop: className,
        siSo: totalSelected,
        khoi: gradeLevel,
        maGVCN: teacherValue,
    };

    // Bước 1: Gọi API để thêm lớp
    const classResponse = await fetch('/api/lop', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newClassData)
    });

    if (!classResponse.ok) {
        const classErrorData = await classResponse.json();
        errorMessages.push(...classErrorData.errors || [classErrorData.message]);
    } else {
        const classData = await classResponse.json();
        const maLop = classData.maLop;

        // Bước 2: Kiểm tra và tạo học kỳ nếu chưa có
        const semesters = ['Học Kỳ 1', 'Học Kỳ 2'];
        for (const semester of semesters) {
            const semesterResponse = await fetch('/api/hoc-ky', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ ten_hoc_ky: semester, nam_hoc: yearInput })
            });

            // Nếu học kỳ đã tồn tại, không cần làm gì thêm
            if (semesterResponse.status === 409) {
                continue;
            }
            // Kiểm tra lỗi khác
            if (!semesterResponse.ok) {
                const semesterErrorData = await semesterResponse.json();
                errorMessages.push(...semesterErrorData.errors || [semesterErrorData.message]);
            }
        }

        // Bước 3: Thêm học sinh vào lớp
        await Promise.all(students.map(async (student, index) => {
            if (selectedStudents[index]) { // Kiểm tra nếu học sinh được chọn
                const studentClassData = {
                    maHocSinh: student.maHocSinh,
                    maLop: maLop,
                    namHoc: yearInput
                };
                const studentResponse = await fetch('/api/hoc-sinh-lop', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(studentClassData)
                });
                if (!studentResponse.ok) {
                    const studentErrorData = await studentResponse.json();
                    errorMessages.push(...studentErrorData.errors || [studentErrorData.message]);
                }
            }
        }));
    }

    // Thông báo lỗi nếu có
    if (errorMessages.length > 0) {
        alert('Có lỗi xảy ra:\n' + errorMessages.join('\n'));
    } else {
        // Hiển thị thông tin lớp học
        document.getElementById('class-name-display').innerText = className;
        document.getElementById('teacher-name-display').innerText = teacherSelect.options[teacherSelect.selectedIndex].text; // Tên giáo viên
        document.getElementById('grade-level-display').innerText = gradeLevel;
        document.getElementById('year-display').innerText = yearInput;

        // Ẩn giao diện lớp học và hiện giao diện danh sách học sinh
        document.getElementById('class-list').style.display = 'none';
        document.getElementById('student-list-success').style.display = 'block';

        const studentListBody = document.getElementById('student-list-success-body');
        studentListBody.innerHTML = '';

        // Hiển thị thông tin học sinh trong bảng
        let count = 1; // Bắt đầu từ 1
        students.forEach((student, index) => {
            if (selectedStudents[index]) { // Hiển thị chỉ học sinh được chọn
                studentListBody.innerHTML += `
                    <tr>
                        <td>${count++}</td> <!-- Sử dụng biến count -->
                        <td>${student.ho + ' ' + student.ten || 'Chưa có'}</td>
                        <td>${student.gioiTinh || 'Chưa có'}</td>
                        <td>${student.ngaySinh || 'Chưa có'}</td>
                        <td>${student.diaChi || 'Chưa có'}</td>
                    </tr>
                `;
            }
        });
    }
});

//
function continueAdding() {
    // Reset các trường nhập liệu
    document.getElementById('class-name').value = '';
    document.getElementById('grade-level1').value = ''; // Đặt lại giá trị chọn
    document.getElementById('year-input').value = ''; // Đặt lại giá trị chọn
    document.getElementById('teacher-list').value = ''; // Đặt lại giá trị chọn
    document.getElementById('count').textContent = '0'; // Reset số lượng học sinh đã chọn

    // Reset checkbox học sinh
    const checkboxes = document.querySelectorAll('.student-checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.checked = false;
    });

    // Ẩn giao diện danh sách học sinh và hiện giao diện thêm lớp học
    document.getElementById('class-list').style.display = 'block'; // Hiện giao diện thêm lớp học
    document.getElementById('student-list-success').style.display = 'none'; // Ẩn giao diện danh sách học sinh
}


////////////////---------------
//Thong tin HS-QLHS
let changesMade = false;

function searchStudents() {
    const studentId = document.getElementById('student_manage-id').value;

    // Gọi API để lấy dữ liệu học sinh
    fetch(`/api/manage_students?studentId=${studentId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Không tìm thấy học sinh.');
            }
            return response.json();
        })
        .then(student => {
            // Hiển thị thông tin học sinh trong thẻ
            document.getElementById('student_manage-name').innerText = `${student.ho} ${student.ten}`;
            document.getElementById('student_manage-id-display').innerText = student.maHocSinh;
            document.getElementById('student_manage-dob').value = student.ngaySinh;
            document.getElementById('student_manage-gender').value = student.gioiTinh;
            document.getElementById('student_manage-address').value = student.diaChi;
            document.getElementById('student_manage-phone').value = student.soDienThoai;
            document.getElementById('student_manage-email').value = student.email;

            // Hiện thẻ thông tin học sinh
            document.getElementById('student_manage-info-card').style.display = 'block';
            document.getElementById('not-found-message').style.display = 'none';
        })
        .catch(error => {
            alert(error.message);
            document.getElementById('student_manage-info-card').style.display = 'none';
            document.getElementById('not-found-message').style.display = 'block';
        });
}

function markChanged() {
    changesMade = true;
}

function confirmSave() {
    if (!changesMade) {
        alert('Không có thay đổi nào để lưu.');
        return;
    }

    if (confirm('Bạn có chắc chắn muốn lưu những thay đổi này?')) {
        const student = {
            maHocSinh: document.getElementById('student_manage-id-display').innerText,
            ho: document.getElementById('student_manage-name').innerText.split(' ')[0],
            ten: document.getElementById('student_manage-name').innerText.split(' ')[1],
            ngaySinh: document.getElementById('student_manage-dob').value,
            diaChi: document.getElementById('student_manage-address').value,
            soDienThoai: document.getElementById('student_manage-phone').value,
            email: document.getElementById('student_manage-email').value,
            gioiTinh: document.getElementById('student_manage-gender').value
        };

        // Gọi API để lưu dữ liệu
        fetch('/api/update_students', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify([student]) // Gửi dưới dạng danh sách
        })
        .then(response => {
            if (response.ok) {
                alert('Thông tin đã được lưu thành công!');
                changesMade = false; // Đặt lại trạng thái
            } else {
                alert('Có lỗi xảy ra khi lưu thông tin.');
            }
        });
    }
}

//function editStudent() {
//    // Thực hiện chức năng sửa thông tin học sinh (nếu cần)
//    alert('Chức năng sửa thông tin học sinh.');
//}
//het QLHS


/////////////////--------------
//Dieu chinh Lop
const Khoi = {
    KHOI_10: 10,
    KHOI_11: 11,
    KHOI_12: 12
};

function loadClasses() {
    const academicYear = document.getElementById('academic-year').value;
    const grade = document.getElementById('grade-select').value;

    // Ẩn các block không cần thiết
    document.getElementById('class-details').style.display = 'none';
    document.getElementById('student-list-details').innerHTML = '';

    if (academicYear && grade) {
        // Gọi API để lấy danh sách lớp
        fetch(`/api/list_classes?academicYear=${academicYear}&grade=${grade}`)
            .then(response => response.json())
            .then(classes => {
                const classList = document.getElementById('class-list-items');
                classList.innerHTML = ''; // Xóa danh sách hiện tại

                if (classes.length === 0) {
                    // Không có lớp học nào
                    const noClassLabel = document.createElement('li');
                    noClassLabel.className = 'list-group-item text-center';
                    noClassLabel.innerText = 'Không có lớp học nào';
                    classList.appendChild(noClassLabel);
                } else {
                    // Nạp danh sách lớp
                    classes.forEach(classItem => {
                        const li = document.createElement('li');
                        li.className = 'list-group-item d-flex justify-content-between align-items-center';
                        li.innerText = classItem.tenLop;
                        const button = document.createElement('button');
                        button.className = 'btn btn-info btn-sm';
                        button.innerText = 'Xem';
                        button.onclick = () => viewClass(classItem.maLop);
                        li.appendChild(button);
                        classList.appendChild(li);
                    });
                }

                // Hiển thị container danh sách lớp
                document.getElementById('class-list-container').style.display = 'block';
            })
            .catch(error => {
                console.error('Lỗi:', error);
                alert('Có lỗi xảy ra khi tải danh sách lớp.');
            });
    }
}

function viewClass(classId) {
    // Gọi API để lấy thông tin lớp và danh sách học sinh
    fetch(`/api/class/${classId}`)
        .then(response => response.json())
        .then(classData => {
            // Cập nhật thông tin lớp
            document.getElementById('class-name-details').innerText = classData.tenLop;
            document.getElementById('class-size-details').innerText = classData.siSo;

            // Đặt giá trị cho các trường trong popup chỉnh sửa
            document.getElementById('edit-class-name').value = classData.tenLop; // Để chỉnh sửa
            document.getElementById('edit-class-size').value = classData.siSo; // Chỉ đọc
//            document.getElementById('edit-grade').value = classData.khoi; // Có thể lấy từ API nếu cần

            const studentList = document.getElementById('student-list-details');
            studentList.innerHTML = ''; // Xóa danh sách học sinh hiện tại

            classData.hocSinh.forEach(student => {
                const li = document.createElement('li');
                li.className = 'list-group-item d-flex justify-content-between align-items-center';
                li.innerText = `${student.ho} ${student.ten}`;
                const deleteBtn = document.createElement('button');
                deleteBtn.className = 'btn btn-danger btn-sm';
                deleteBtn.innerText = 'Xóa';
                deleteBtn.onclick = () => confirmDeleteStudent(student.maHocSinh, classId);
                li.appendChild(deleteBtn);
                studentList.appendChild(li);
            });

            document.getElementById('class-details').style.display = 'block';
        });
}
//
function showEditClassPopup() {
    const className = document.getElementById('class-name-details').innerText;
    const classSize = document.getElementById('class-size-details').innerText;

    // Đặt giá trị cho các trường trong popup
    document.getElementById('edit-class-name').value = className;
    document.getElementById('edit-class-size').value = classSize; // Chỉ đọc
//    document.getElementById('edit-grade').value = ''; // Có thể lấy từ API nếu cần

    const modal = new bootstrap.Modal(document.getElementById('editClassModal'));
    modal.show();
}

function saveClassEdit() {
    const newClassName = document.getElementById('edit-class-name').value;
    const oldClassName = document.getElementById('class-name-details').innerText;

    if (newClassName !== oldClassName) {
        if (confirm('Bạn có chắc chắn muốn thay đổi tên lớp?')) {
            fetch(`/api/update_class_name`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ oldClassName, newClassName })
            })
            .then(response => {
                if (response.ok) {
                    return response.json(); // Chuyển đổi phản hồi thành JSON
                } else {
                    alert('Có lỗi xảy ra khi lưu tên lớp.');
                    throw new Error('Error updating class name');
                }
            })
            .then(data => {
                // Gọi viewClass với class_id được trả về từ API
                viewClass(data.class_id); // Sử dụng class_id từ phản hồi
                alert('Tên lớp đã được cập nhật.');
                const modal = bootstrap.Modal.getInstance(document.getElementById('editClassModal'));
                loadClasses();
                modal.hide();
            })
            .catch(error => {
                console.error('Lỗi:', error);
                alert('Có lỗi xảy ra khi lưu tên lớp.');
            });
        }
    } else {
        alert('Tên lớp không thay đổi.');
        const modal = bootstrap.Modal.getInstance(document.getElementById('editClassModal'));
        modal.hide();
    }
}
//

document.getElementById('academic-year').addEventListener('change', function() {
    const grade = document.getElementById('grade-select').value;

    // Kiểm tra nếu Năm Học hoặc Khối không được chọn
    if (this.value === '' ) {
        // Ẩn thông tin lớp khi năm học hoặc khối không được chọn
        document.getElementById('class-details').style.display = 'none';
        document.getElementById('class-list-container').style.display = 'none';
        document.getElementById('student-list-details').innerHTML = '';
    } else {
        // Nếu cả Năm Học và Khối đều được chọn
        loadClasses();
    }
});

// Cũng cần thêm sự kiện cho khối
document.getElementById('grade-select').addEventListener('change', function() {
    const academicYear = document.getElementById('academic-year').value;

    // Kiểm tra nếu Năm Học hoặc Khối không được chọn
    if (this.value === '') {
        // Ẩn thông tin lớp khi năm học hoặc khối không được chọn
        document.getElementById('class-details').style.display = 'none';
        document.getElementById('class-list-container').style.display = 'none';
        document.getElementById('student-list-details').innerHTML = '';
    } else {
        // Nếu cả Năm Học và Khối đều được chọn
        loadClasses();
    }
});

function confirmDeleteStudent(studentId, classId) {
    if (confirm('Bạn có chắc chắn muốn xóa học sinh này khỏi lớp?')) {
        fetch(`/api/delete_student`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ studentId, classId })
        })
        .then(response => {
            if (response.ok) {
                alert('Học sinh đã được xóa.');
                viewClass(classId); // Tải lại thông tin lớp
            } else {
                alert('Có lỗi xảy ra khi xóa học sinh.');
            }
        });
    }
}

function showAddStudentPopup() {
    const modal = new bootstrap.Modal(document.getElementById('addStudentModal'));
    modal.show();
}

function confirmAddStudent() {
    const studentId = document.getElementById('student_id_display').innerText; // Lấy mã học sinh từ thông tin hiển thị
    const className = document.getElementById('class-name-details').innerText; // Lấy tên lớp từ thông tin hiện có

    if (!studentId) {
        alert('Không có thông tin học sinh để thêm.');
        return;
    }

    if (confirm('Bạn có chắc chắn muốn thêm học sinh này vào lớp?')) {
        fetch(`/api/add_student`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ maHocSinh: studentId, tenLop: className })
        })
        .then(response => {
            if (response.ok) {
                return response.json(); // Chuyển đổi phản hồi thành JSON
            } else {
                throw new Error('Có lỗi xảy ra khi thêm học sinh: ' + response.statusText);
            }
        })
        .then(data => {
            alert(data.message); // Hiển thị thông báo
            const modal = bootstrap.Modal.getInstance(document.getElementById('addStudentModal'));
            modal.hide();
            viewClass(data.classId); // Tải lại thông tin lớp bằng classId
        })
        .catch(error => {
            alert(error.message); // Hiển thị thông báo lỗi
        });
    }
}

function searchStudent() {
    const studentId = document.getElementById('student_id_input').value.trim();

    if (!studentId) {
        alert('Vui lòng nhập mã học sinh.');
        return;
    }

    // Gọi API để lấy dữ liệu học sinh
    fetch(`/api/manage_students?studentId=${studentId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Không tìm thấy học sinh.');
            }
            return response.json();
        })
        .then(student => {
            // Hiển thị thông tin học sinh
            document.getElementById('student_name').innerText = `${student.ho} ${student.ten}`;
            document.getElementById('student_id_display').innerText = student.maHocSinh;
            document.getElementById('student_dob_display').innerText = student.ngaySinh;
            document.getElementById('student_gender_display').innerText = student.gioiTinh;
            document.getElementById('student_address_display').innerText = student.diaChi;
            document.getElementById('student_phone_display').innerText = student.soDienThoai;
            document.getElementById('student_email_display').innerText = student.email;

            // Hiện thẻ thông tin học sinh
            document.getElementById('student_info_container').style.display = 'block';
            document.getElementById('not_found_message').style.display = 'none';
        })
        .catch(error => {
            alert(error.message);
            document.getElementById('student_info_container').style.display = 'none';
            document.getElementById('not_found_message').style.display = 'block';
        });
}

function resetAddStudentModal() {
    // Xóa nội dung trong các trường thông tin
    document.getElementById('student_id_input').value = '';
    document.getElementById('student_info_container').style.display = 'none';
    document.getElementById('not_found_message').style.display = 'none';

    // Xóa nội dung hiển thị thông tin học sinh
    document.getElementById('student_name').innerText = '';
    document.getElementById('student_id_display').innerText = '';
    document.getElementById('student_dob_display').innerText = '';
    document.getElementById('student_gender_display').innerText = '';
    document.getElementById('student_address_display').innerText = '';
    document.getElementById('student_phone_display').innerText = '';
    document.getElementById('student_email_display').innerText = '';
}

document.getElementById('addStudentModal').addEventListener('show.bs.modal', resetAddStudentModal);
//
function confirmNavigation(event) {
            if (!confirm("Bạn có chắc chắn muốn trở về không?")) {
                event.preventDefault(); // Ngăn không cho chuyển hướng
            }
        }


