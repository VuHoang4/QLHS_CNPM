
function showContent(contentId) {
document.getElementById('default-view').style.display = 'none';
const contentItems = document.querySelectorAll('.content-item');
contentItems.forEach(item => {
    item.style.display = 'none';
});

const form = document.getElementById('common-form');
form.style.display = 'block'; // Thay đổi display thành block để hiển thị

document.getElementById(contentId).style.display = 'block';
fetchCommonData(contentId);

const saveButton = document.querySelector('.button-group button[type="submit"]');
const backButton = document.getElementById('backButton');

    if (contentId === 'enter-grades') {
        saveButton.textContent = 'Lưu điểm'; // Văn bản cho Nhập Điểm
        document.getElementById('semester-container').style.display = 'block'; // Hiện phần chọn kỳ học
        document.getElementById('studentTable').style.display = 'table'; // Hiện bảng nhập điểm
        document.getElementById('score-table').style.display = 'none'; // Ẩn bảng điểm môn học

        // Sử dụng saveButton.onclick để xử lý sự kiện submit
        saveButton.onclick = function(event) {
            // Ngăn chặn hành động gửi form mặc định
            event.preventDefault();

            const inputs = document.querySelectorAll('.number-input');
            let isValid = true;

            inputs.forEach((input) => {
                const value = input.value.trim(); // Lấy giá trị và bỏ khoảng trắng
                const errorMessage = input.nextElementSibling; // Lấy thẻ span bên cạnh input

                // Kiểm tra xem giá trị có trống không
                if (value === '') {
                    errorMessage.style.display = 'none'; // Ẩn thông báo lỗi nếu trống
                    input.classList.remove('invalid-input'); // Xóa lớp viền không hợp lệ
                } else if (isNaN(value) || value < 0 || value > 10) {
                    errorMessage.textContent = 'Điểm phải nằm trong khoảng từ 0 đến 10.';
                    errorMessage.style.display = 'block'; // Hiển thị thông báo lỗi
                    input.classList.add('invalid-input'); // Thêm lớp để thay đổi viền
                    isValid = false; // Đánh dấu là không hợp lệ
                } else {
                    errorMessage.style.display = 'none'; // Ẩn thông báo lỗi nếu hợp lệ
                    input.classList.remove('invalid-input'); // Xóa lớp viền không hợp lệ
                }
            });

            if (isValid) {
                // Nếu tất cả các trường hợp hợp lệ, thực hiện lưu điểm
                const confirmed = confirm('Bạn có chắc chắn muốn lưu điểm không?');
                if (confirmed) {
                    try {
                        savePoints(event); // Gọi hàm savePoints
                        alert('Lưu điểm thành công!'); // Hiển thị thông báo thành công
                        handleSelectChange(); // Gọi hàm handleClassChange
                    } catch (error) {
                        console.error('Có lỗi xảy ra khi lưu điểm:', error);
                        alert('Đã xảy ra lỗi khi lưu điểm. Vui lòng thử lại.');
                    }
                }
            }
        };


    } else if (contentId === 'export-grades') {
        saveButton.textContent = 'Xem bảng điểm'; // Văn bản cho Xuất Bảng Điểm
        document.getElementById('semester-container').style.display = 'none'; // Ẩn phần chọn kỳ học
        document.getElementById('studentTable').style.display = 'none'; // Ẩn bảng nhập điểm

        // Hiện bảng điểm môn học khi nhấn nút "Xem bảng điểm"
        saveButton.onclick = function(event) {
            event.preventDefault(); // Ngăn chặn hành động mặc định của nút
            const selectedClass = document.getElementById('class').value;
            const selectedSubject = document.getElementById('subject').value;
            if (selectedClass && selectedSubject) {
                document.getElementById('score-table').style.display = 'block'; // Hiện bảng điểm môn học
                document.getElementById('academicYearDisplay').textContent = document.getElementById('academicYear').textContent.trim();


                // Logic để nạp dữ liệu vào bảng điểm
                loadScoreTable(selectedSubject, selectedClass, document.getElementById('academicYear').textContent.trim());
            } else {
                document.getElementById('score-table').style.display = 'none'; // Ẩn bảng điểm nếu chưa chọn lớp hoặc môn
                alert('Vui lòng chọn lớp và môn trước khi xem bảng điểm.');
            }
        };
    }


                // Sử dụng backButton.onclick để xử lý sự kiện click
        backButton.onclick = function(event) {
            // Ngăn chặn hành động mặc định của thẻ a
            event.preventDefault();

            // Hiển thị hộp thoại xác nhận
            const userConfirmed = confirm("Bạn có chắc chắn muốn trở về không?");

            // Nếu người dùng xác nhận, điều hướng đến trang
            if (userConfirmed) {
                window.location.href = this.href; // Điều hướng đến liên kết
            }
        };
}

function fetchCommonData(contentId) {
        const maNguoiDung = window.maNguoiDung; // Lấy mã người dùng từ Flask

        fetch(`/get_classes/${maNguoiDung}`)
            .then(response => response.json())
            .then(data => {
                const selectElement = document.getElementById('class');
                selectElement.innerHTML = '<option value="">Chọn lớp...</option>';

                for (const [maLop, tenLop] of Object.entries(data)) {
                    const option = document.createElement('option');
                    option.value = maLop;
                    option.textContent = tenLop;
                    selectElement.appendChild(option);
                }
            })
            .catch(error => console.error('Error fetching classes:', error));

        const academicYearEl = document.getElementById('academicYear');
        const namHoc = academicYearEl.textContent.trim();
        loadSemesters(namHoc); // Nạp kỳ học
    }


function loadSubjects(maLop) {
    const subjectSelect = document.getElementById('subject');

    // Gọi API để lấy danh sách môn học với maLop
    fetch(`/fetch_subjects?maLop=${maLop}`)
        .then(response => response.json())
        .then(data => {
            // Xóa tất cả các option hiện có trước khi nạp mới
            subjectSelect.innerHTML = '<option value="">Chọn môn...</option>'; // Thêm option mặc định

            // Nạp các option vào select
            data.forEach(subject => {
                const option = document.createElement('option');
                option.value = subject.maMonHoc; // Giá trị của option
                option.textContent = subject.tenMonHoc; // Hiển thị tên môn học
                subjectSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error:', error));
}

function handleClassChange() {
    const classSelect = document.getElementById('class');
    const maLop = classSelect.value; // Lấy giá trị của lớp đã chọn

    // Gọi loadSubjects với maLop
    if (maLop) {
        loadSubjects(maLop);

        // Gọi hàm nạp học sinh
        loadStudents(maLop);
    } else {
        // Nếu không có lớp nào được chọn, có thể xóa các môn học
        const subjectSelect = document.getElementById('subject');
        subjectSelect.innerHTML = '<option value="">Chọn môn...</option>'; // Thêm option mặc định
    }
}

function handleSelectChange() {
    const classValue = document.getElementById('class').value;
    const subjectValue = document.getElementById('subject').value;
    const semesterValue = document.getElementById('semester').value;

    // Kiểm tra xem cả ba thẻ select đều có giá trị
    if (classValue && subjectValue && semesterValue) {
        const academicYear = document.getElementById('academicYear').textContent.split('-')[0]; // Lấy năm học
        loadPoints(subjectValue, semesterValue); // Gọi hàm loadPoints với môn học và kỳ học
    }
}

function loadSemesters(namHoc) {
        const semesterSelect = document.getElementById('semester');

        fetch(`/fetch_semesters/${namHoc}`)
            .then(response => response.json())
            .then(data => {
                semesterSelect.innerHTML = '<option value="">Chọn kỳ học...</option>';

                data.forEach(semester => {
                    const option = document.createElement('option');
                    option.value = semester.maHocKy;
                    option.textContent = semester.tenHocKy;
                    semesterSelect.appendChild(option);
                });
            })
            .catch(error => console.error('Error fetching semesters:', error));
    }



// Hàm để thêm input cho điểm trong toàn bộ cột
// Hàm để thêm input cho điểm trong toàn bộ cột
function addInputPoint(columnClass, maxInputs) {
    const inputGroups = document.querySelectorAll(`.${columnClass}`);

    inputGroups.forEach((container) => {
        const currentInputs = container.querySelectorAll('input').length;
        const currentLabels = container.querySelectorAll('label').length;

        // Tính tổng số lượng input và label hiện tại
        const totalEntries = currentInputs + currentLabels;

        // Đảm bảo có ít nhất 1 input và không vượt quá maxInputs
        if (totalEntries < maxInputs) {
            const newInput = document.createElement('div');
            newInput.className = "input-group mb-2";
            newInput.innerHTML = `
                <input type="number" step="0.01" class="number-input form-control"  min="0" max="10" style="width: 90px;" placeholder="Điểm" >
                <span class="error-message" style="color: red; display: none;"></span>
            `;
            container.appendChild(newInput);
        }
    });
}

// Hàm để xóa input mới nhất trong cột, đảm bảo ít nhất 1 input hoặc label còn lại
function removeLastInput(columnClass) {
    const inputGroups = document.querySelectorAll(`.${columnClass}`);

    inputGroups.forEach(container => {
        const inputs = container.querySelectorAll('input');
        const labels = container.querySelectorAll('label');

        // Tính tổng số lượng input và label hiện tại
        const totalEntries = inputs.length + labels.length;

        // Đảm bảo còn lại ít nhất 1 input hoặc label
        if (totalEntries > 1) {
            if (inputs.length > 0) {
                // Xóa thẻ input mới nhất
                inputs[inputs.length - 1].parentElement.remove();
            }
        }
    });
}

// Hàm để nạp học sinh vào bảng
function loadStudents(maLop) {
    fetch(`/fetch_students/${maLop}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const tableBody = document.getElementById('studentTableBody');
            tableBody.innerHTML = ''; // Xóa dữ liệu cũ

            // Tạo hàng cho các nút thêm và xóa input
            const buttonRow = document.createElement('tr');
            buttonRow.innerHTML = `
                <td colspan="2"></td> <!-- Chiếm 2 ô cho tên học sinh -->
                <td>
                    <button type="button" class="btn btn-success btn-sm" onclick="addInputPoint('points15', 5)">+ Thêm cột điểm 15'</button>
                    <button type="button" class="btn btn-danger btn-sm" onclick="removeLastInput('points15')">- Xóa cột điểm 15'</button>
                </td>
                <td>
                    <button type="button" class="btn btn-success btn-sm" onclick="addInputPoint('points1', 3)">+ Thêm cột điểm 1 tiết</button>
                    <button type="button" class="btn btn-danger btn-sm" onclick="removeLastInput('points1')">- Xóa cột điểm 1 tiết</button>
                </td>
                <td>
                    <button type="button" class="btn btn-success btn-sm" onclick="addInputPoint('pointsThi', 1)">+ Thêm cột điểm thi</button>

                </td>
            `;
            tableBody.appendChild(buttonRow); // Thêm hàng nút vào đầu bảng

            // Tạo hàng cho từng học sinh
            data.students.forEach((student, index) => {  // Thay đổi ở đây
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${index + 1}</td>
                    <td data-ma-hoc-sinh="${student.maHocSinh}">${student.tenHocSinh}</td> <!-- Mã học sinh lưu trong data attribute -->
                    <td class="points15"></td>
                    <td class="points1"></td>
                    <td class="pointsThi"></td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching students:', error));
}

function loadPoints(maMonHoc, maHocKy) {
    const rows = document.querySelectorAll('#studentTableBody tr');
    const maHocSinhs = [];

    // Lấy danh sách mã học sinh từ các dòng
    rows.forEach(row => {
        const maHocSinh = getMaHocSinhFromRow(row);
        if (maHocSinh) {
            maHocSinhs.push(maHocSinh);
        }
    });

     // Reset bảng điểm trước khi nạp dữ liệu mới
    rows.forEach(row => {
        const pointContainers = row.querySelectorAll('.points15, .points1, .pointsThi');
        pointContainers.forEach(container => {
            // Xóa tất cả các label và input hiện có
            container.innerHTML = '';
        });
    });

    // Gọi API với danh sách mã học sinh
    fetch('/fetch_points', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            maMonHoc: maMonHoc,
            maHocKy: maHocKy,
            maHocSinhs: maHocSinhs
        })
    })
    .then(response => response.json())
    .then(diemData => {
        const pointsMap = {};
        diemData.forEach(diem => {
            const maHocSinh = diem.maHocSinh;
            if (!pointsMap[maHocSinh]) {
                pointsMap[maHocSinh] = [];
            }
            pointsMap[maHocSinh].push(diem);
        });

        rows.forEach(row => {
            const currentMaHocSinh = getMaHocSinhFromRow(row);
            const pointContainer15 = row.querySelector(`.points15`);
            const pointContainer1 = row.querySelector(`.points1`);
            const pointContainerCuoiKi = row.querySelector(`.pointsThi`);

            // Kiểm tra nếu có điểm cho học sinh này
            if (pointsMap[currentMaHocSinh]) {
                pointsMap[currentMaHocSinh].forEach(diem => {
                    let columnClass;
                    switch (diem.loaiDiem) {
                        case 'Kiểm Tra Mười Lăm Phút':
                            columnClass = 'points15';
                            break;
                        case 'Kiểm Tra Một Tiết':
                            columnClass = 'points1';
                            break;
                        case 'Kiểm Tra Cuối Kì':
                            columnClass = 'pointsThi';
                            break;
                    }

                    const pointContainer = row.querySelector(`.${columnClass}`);
                    if (pointContainer) {
                                                // Tạo một thẻ div để bọc thông tin điểm
                        const pointWrapper = document.createElement('div');
                        pointWrapper.classList.add('point-wrapper'); // Thêm lớp nếu cần để quản lý kiểu dáng

                        // Tạo thẻ div cho phần "Điểm thứ ..."
                        const pointLabel = document.createElement('div');
                        pointLabel.textContent = `Điểm thứ ${diem.soThuTuDiem} :`; // Phần thông tin điểm
                        pointLabel.classList.add('point-info'); // Thêm lớp nếu cần

                        // Tạo thẻ label cho giá trị điểm
                        const newLabel = document.createElement('label');
                        newLabel.textContent = diem.diem; // Giá trị điểm
                        newLabel.classList.add('label-highlight'); // Thêm lớp nổi bật

                        // Thêm pointLabel vào pointWrapper
                        pointWrapper.appendChild(pointLabel);

                        // Thêm label ngay sau pointLabel vào pointWrapper
                        pointWrapper.appendChild(newLabel); // Đảm bảo label nằm ngay sau div

                        // Thêm pointWrapper vào pointContainer
                        pointContainer.appendChild(pointWrapper);

                        // Tính số lượng input và label hiện tại
                        const currentInputs = pointContainer.querySelectorAll('input').length;
                        const currentLabels = pointContainer.querySelectorAll('label').length;
                        const totalEntries = currentInputs + currentLabels;

                        // Thêm input mới nếu chưa đạt tối đa

                    }
                });
            } else {
                // Nếu không có điểm, vẫn thêm ít nhất 1 input mới
                if (pointContainer15) {
                    const currentInputs = pointContainer15.querySelectorAll('input').length;
                    const currentLabels = pointContainer15.querySelectorAll('label').length;
                    const totalEntries = currentInputs + currentLabels;

                    // Thêm input nếu chưa đủ
                    if (totalEntries < 5) {
                        const newInput = document.createElement('div');
                        newInput.className = "input-group mb-2";
                        newInput.innerHTML = `
                            <input type="number" step="0.01" class="number-input form-control"  min="0" max="10" style="width: 90px;" placeholder="Điểm" >
                            <span class="error-message" style="color: red; display: none;"></span>
                        `;
                        pointContainer15.appendChild(newInput);
                    }
                }
                // Lặp lại cho các cột khác (points1, pointsCuoiKi) nếu cần
                if (pointContainer1) {
                    const currentInputs = pointContainer1.querySelectorAll('input').length;
                    const currentLabels = pointContainer1.querySelectorAll('label').length;
                    const totalEntries = currentInputs + currentLabels;

                    // Thêm input nếu chưa đủ
                    if (totalEntries < 3) { // Giả sử tối đa 3 cho điểm 1 tiết
                        const newInput = document.createElement('div');
                        newInput.className = "input-group mb-2";
                        newInput.innerHTML = `
                            <input type="number" step="0.01" class="number-input form-control"  min="0" max="10"  style="width: 90px;" placeholder="Điểm" >
                            <span class="error-message" style="color: red; display: none;"></span>
                        `;
                        pointContainer1.appendChild(newInput);
                    }
                }
                // Tương tự cho cột điểm cuối kỳ nếu cần
                if (pointContainerCuoiKi) {
                    const currentInputs = pointContainerCuoiKi.querySelectorAll('input').length;
                    const currentLabels = pointContainerCuoiKi.querySelectorAll('label').length;
                    const totalEntries = currentInputs + currentLabels;

                    // Thêm input nếu chưa đủ
                    if (totalEntries < 3) { // Giả sử tối đa 3 cho điểm 1 tiết
                        const newInput = document.createElement('div');
                        newInput.className = "input-group mb-2";
                        newInput.innerHTML = `
                            <input type="number" step="0.01" class="number-input form-control"  min="0" max="10"  style="width: 90px;" placeholder="Điểm" >
                            <span class="error-message" style="color: red; display: none;"></span>
                        `;
                        pointContainerCuoiKi.appendChild(newInput);
                    }
                }
            }
        });
    })
    .catch(error => console.error('Error fetching points:', error));
}

// Giả sử có hàm để lấy mã học sinh từ tên học sinh
function getMaHocSinhFromRow(row) {
    // Tìm thẻ <td> chứa tên học sinh
    const tenHocSinhCell = row.querySelector('td[data-ma-hoc-sinh]');
    if (tenHocSinhCell) {
        return tenHocSinhCell.getAttribute('data-ma-hoc-sinh'); // Trả về mã học sinh
    }
    return null; // Nếu không tìm thấy
}

 // Hàm để lưu điểm
// Gán sự kiện submit cho form
//document.getElementById('Form-Point').addEventListener('submit', function(event) {
//    // Ngăn chặn hành động gửi form mặc định
//    event.preventDefault();
//
//    // Hiển thị hộp thoại xác nhận
//    const confirmed = confirm('Bạn có chắc chắn muốn lưu điểm không?');
//
//    // Nếu người dùng nhấn OK, gọi hàm savePoints
//    if (confirmed) {
//        savePoints(event); // Gọi hàm savePoints
//    }
//    // Nếu người dùng nhấn Cancel, không làm gì
//});
//
// // Lắng nghe sự kiện click trên nút trở về
//    document.getElementById('backButton').addEventListener('click', function(event) {
//        // Ngăn chặn hành động mặc định của thẻ a
//        event.preventDefault();
//
//        // Hiển thị hộp thoại xác nhận
//        const userConfirmed = confirm("Bạn có chắc chắn muốn trở về không?");
//
//        // Nếu người dùng xác nhận, điều hướng đến trang
//        if (userConfirmed) {
//            window.location.href = this.href; // Điều hướng đến liên kết
//        }
//    });

function savePoints(event) {
    event.preventDefault(); // Ngăn chặn hành động mặc định của form

       const rows = document.querySelectorAll('#studentTableBody tr');

    const maMonHoc = document.querySelector('#subject').value; // Mã môn học
    const maHocKy = document.querySelector('#semester').value; // Mã học kỳ

    rows.forEach(row => {
        const maHocSinh = getMaHocSinhFromRow(row);

        // Lấy điểm từ các input trong cột điểm 15 phút và 1 tiết
        const inputs15 = row.querySelectorAll('.points15 input');
        const inputs1 = row.querySelectorAll('.points1 input');
        const inputsThi = row.querySelectorAll('.pointsThi input');

        // Kiểm tra và lưu điểm cho inputs15 nếu có input
        if (inputs15.length > 0) {
            inputs15.forEach(input => {
                if (input.value) {
                    const giaTriDiem = input.value;
                    const loaiDiem = 'Kiểm Tra Mười Lăm Phút';
                    add_diem(giaTriDiem, loaiDiem, maMonHoc, maHocSinh, maHocKy);
                }
            });
        }

        // Kiểm tra và lưu điểm cho inputs1 nếu có input
        if (inputs1.length > 0) {
            inputs1.forEach(input => {
                if (input.value) {
                    const giaTriDiem = input.value;
                    const loaiDiem = 'Kiểm Tra Một Tiết';
                    add_diem(giaTriDiem, loaiDiem, maMonHoc, maHocSinh, maHocKy);
                }
            });
        }

        // Lấy điểm từ cột điểm thi cuối kỳ
        if (inputsThi.length > 0) {
            inputsThi.forEach(input => {
                if (input.value) {
                    const giaTriDiem = input.value;
                    const loaiDiem = 'Kiểm Tra Cuối Kì';
                    add_diem(giaTriDiem, loaiDiem, maMonHoc, maHocSinh, maHocKy);
                }
            });
        }

    });
}

// Hàm để gọi API lưu điểm
function add_diem(gia_tri_diem, loai_diem, ma_mon_hoc, ma_hoc_sinh, ma_hoc_ky) {
    fetch("/add_diem", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            gia_tri_diem: gia_tri_diem,
            loai_diem: loai_diem,
            ma_mon_hoc: ma_mon_hoc,
            ma_hoc_sinh: ma_hoc_sinh,
            ma_hoc_ky: ma_hoc_ky
        })
    })
    .then(response => {
        if (response.ok) {
            console.log(`Điểm ${gia_tri_diem} đã được lưu cho học sinh ${ma_hoc_sinh}`);
        } else {
            console.error('Lỗi khi lưu điểm:', response.statusText);
        }
    })
    .catch(error => console.error('Lỗi mạng:', error));
}

//
//
async function loadScoreTable(maMonHoc, maLop, namHoc) {
    try {
        // Lấy tất cả học kỳ dựa trên năm học
        const hocKyResponse = await fetch(`/fetch_hoc_ky/${namHoc}`);
        const hocKyData = await hocKyResponse.json();
        const hocKyList = hocKyData; // Lưu danh sách kỳ học

        // Lấy danh sách học sinh từ lớp
        const studentsResponse = await fetch(`/fetch_students/${maLop}`);
        const data = await studentsResponse.json();

        const scoreTableBody = document.getElementById('scoreTableBody');
        scoreTableBody.innerHTML = ''; // Xóa dữ liệu cũ

        // Lấy tên lớp
        const tenLop = data.tenLop;

        // Duyệt qua từng học sinh
        for (const [index, student] of data.students.entries()) {
            let diemHK1 = [];
            let diemHK2 = [];

            // Tạo mảng các promises từ các yêu cầu fetch
            for (const hocKy of hocKyList) {
                const maHocKy = hocKy.maHocKy;
                const lastTwoChars = maHocKy.slice(-2); // Lấy 2 ký tự cuối

                // Lấy điểm theo mã học sinh và mã môn học
                const diemResponse = await fetch(`/fetch_scores/${student.maHocSinh}/${maHocKy}/${maMonHoc}`);
                const diemList = await diemResponse.json();

                // Phân loại điểm vào HK1 hoặc HK2
                if (lastTwoChars === '01') {
                    diemHK1 = diemHK1.concat(diemList); // Điểm HK1
                } else if (lastTwoChars === '02') {
                    diemHK2 = diemHK2.concat(diemList); // Điểm HK2
                }
            }

            // Tính điểm trung bình cho HK1 nếu có điểm
            let diemTBHK1 = '-'; // Mặc định
            if (diemHK1.length > 0) {
                const averageResponseHK1 = await fetch('/calculate_average', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ diemList: diemHK1 })
                });
                const averageHK1 = await averageResponseHK1.json();
                diemTBHK1 = averageHK1.average_score.toFixed(2); // Lưu điểm trung bình HK1
            }

            // Tính điểm trung bình cho HK2 nếu có điểm
            let diemTBHK2 = '-'; // Mặc định
            if (diemHK2.length > 0) {
                const averageResponseHK2 = await fetch('/calculate_average', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ diemList: diemHK2 })
                });
                const averageHK2 = await averageResponseHK2.json();
                diemTBHK2 = averageHK2.average_score.toFixed(2); // Lưu điểm trung bình HK2
            }

            // Tạo hàng cho bảng điểm
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${student.tenHocSinh}</td>
                <td>${tenLop}</td> <!-- Tên lớp -->
                <td>${diemTBHK1}</td>
                <td>${diemTBHK2}</td>
            `;
            scoreTableBody.appendChild(row);
        }

        console.log('Đã hoàn thành việc tải bảng điểm.');
    } catch (error) {
        console.error('Error:', error);
    }
}



document.getElementById('exportButton').addEventListener('click', async () => {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    // Thêm font chữ hỗ trợ tiếng Việt
    doc.setFont("Helvetica");

    // Lấy dữ liệu từ bảng
    const table = document.getElementById('scoreTable');
    const rows = table.getElementsByTagName('tr');

    const data = [];
    for (let i = 0; i < rows.length; i++) {
        const cols = rows[i].getElementsByTagName('td');
        const rowData = [];
        for (let j = 0; j < cols.length; j++) {
            rowData.push(cols[j].innerText);
        }
        data.push(rowData);
    }

    // Thêm tiêu đề bảng
    doc.autoTable({
        head: [Array.from(rows[0].cells).map(cell => cell.innerText)],
        body: data.slice(1), // loại bỏ tiêu đề
        styles: { font: "Helvetica" },
    });

    // Lưu file PDF
    const pdfFile = doc.output('blob');

    // Hiển thị thông báo xác nhận
    if (confirm("Bạn có muốn xuất file PDF và gửi email không?")) {
        doc.save('danhsach_hocsinh.pdf');

        // Lấy mã lớp và môn học từ phần tử HTML
        const maLop = document.getElementById('class').value; // Lấy giá trị mã lớp đã chọn
        const subjectSelect = document.getElementById('subject');// Lấy giá trị môn học đã chọn
        const selectedOption = subjectSelect.options[subjectSelect.selectedIndex];
        const selectedSubjectName = selectedOption.text; // Lấy tên môn học

        // Lấy danh sách học sinh để gửi email
        const studentsResponse = await fetch(`/fetch_students/${maLop}`);
        const studentData = await studentsResponse.json();
        const tenLop = studentData.tenLop;

        // Duyệt qua danh sách học sinh và gửi email
        for (const student of studentData.students) {
            const email = student.email; // Lấy email thật của học sinh

            const formData = new FormData();
            formData.append('pdf', pdfFile, 'danhsach_hocsinh.pdf');
            formData.append('email', email); // Địa chỉ email nhận
            formData.append('message', `Gửi em: ${student.tenHocSinh}\nLớp: ${tenLop}\nThông tin về bảng điểm môn: ${selectedSubjectName}\nThông tin cụ thể được đính kèm ở file bên dưới.`);

            try {
                const response = await fetch('/send_email', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                console.log(`Email đã gửi đến ${student.tenHocSinh}:`, result);
            } catch (error) {
                console.error(`Lỗi khi gửi email đến ${student.tenHocSinh}:`, error);
            }
        }

        alert('Đã gửi email cho tất cả học sinh!');
    }
});