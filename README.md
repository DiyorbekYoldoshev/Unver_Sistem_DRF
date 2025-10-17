# Unver_Sistem_DRF
Universitet Sistem Django Rest Framework

Universitetdagi barcha jarayonlarni (studentlar, teacherlar, employee va boshqaruv) yagona tizimda boshqarish.

| Rol                      | Tavsif                                                           | Asosiy vakolatlar                                                                               |
| ------------------------ | ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| **Admin (Super Admin)**  | Butun tizimni nazorat qiladi (universitet rahbari)               | Barcha userlarni boshqarish, fakultet/bo‘lim/fan yaratish, o‘qituvchi yoki xodim qo‘shish       |
| **Employee (Xodim)**     | Dekanat, kotiba, bo‘lim rahbari kabi texnik yoki boshqaruv xodim | Studentlarni qo‘shish, baholarni tasdiqlash, attendance kiritish, o‘qituvchilarga yordam berish |
| **Teacher (O‘qituvchi)** | Fanni o‘qituvchi shaxs                                           | Talabalarni ko‘rish, baho kiritish, attendance kiritish, dars jadvalini boshqarish              |
| **Student (Talaba)**     | Foydalanuvchi (o‘quvchi)                                         | O‘z baholari, jadvali, dars davomati, fanlari va xabarlarini ko‘rish                            |

fayl joylashuvi
university_project/
│
├── core/                     # umumiy logika, signal, utils, service, base models
│   ├── models.py
│   ├── utils.py
│   ├── services/
│   ├── signals.py
│   └── management/
│
├── admin_panel/              # superadmin uchun (universitet boshqaruvi)
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── permissions.py
│
├── employee/                 # xodimlar (dekanat, bo‘lim rahbarlari)
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── permissions.py
│
├── teacher/                  # o‘qituvchilar
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── permissions.py
│
├── student/                  # talabalar
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── permissions.py
│
├── accounts/                 # custom user modeli + auth
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── managers.py
│   └── permissions.py
│
├── telegram_integration/     # bot uchun (core bilan ishlaydi)
│   ├── bot.py
│   ├── handlers/
│   ├── services/
│   └── utils.py
│
└── settings.py, manage.py, requirements.txt, .env



ROLS
🔹 accounts app

Bu autentifikatsiya (login, register, token, roles) va asosiy foydalanuvchi modeli (User) joylashadigan joy.

Custom User modeli (User(AbstractUser)).

JWT autentifikatsiya (login/logout/register).

Role (admin, teacher, employee, student) maydoni shu yerda.

Signal orqali profil avtomatik yaratiladi (masalan, TeacherProfile).

👉 Ya’ni accounts — har bir foydalanuvchining kirish tizimi.


_____________________________________________________________________________________________________________________________
🔹 admin_panel app

Bu super admin uchun boshqaruv moduli — universitetdagi barcha narsani yaratadi va boshqaradi.

Masalan:

Fakultet va bo‘limlar (Faculty, Department).

O‘qituvchi, student, employee yaratish va ularga role biriktirish.

Statistikalar: talabalar soni, o‘qituvchilar, o‘quv yili ma’lumotlari.

👉 admin_panel — boshqaruv markazi.
U accountsdagi foydalanuvchilardan foydalanadi, lekin ularni ma’mur sifatida boshqaradi.


_____________________________________________________________________________________________________________________________

🧱 4. employee app — nima qiladi?

Employee bu dekanat yoki fakultet xodimlari. Ular:

Talabalarni ro‘yxatga oladi (student profil yaratadi).

Teacherlarni fakultet bo‘yicha bog‘laydi.

Student baholarini tasdiqlaydi (teacher kiritganini ko‘radi).

Attendance (davomat)ni kuzatadi.

Reportlar yaratadi (masalan, “5-kurs Informatika fakulteti o‘qituvchilari”).


_____________________________________________________________________________________________________________________________

👨‍🏫 5. teacher app — o‘qituvchi uchun

Teacherlar:

O‘z fanlarini (Subject) boshqaradi.

O‘quv guruhlarini (Group) ko‘radi.

Baholar (Grade) kiritadi.

Davomat (Attendance) belgilaydi.

O‘z fan jadvalini (Schedule) tahrir qiladi.


_____________________________________________________________________________________________________________________________
🧑‍🎓 6. student app — talaba uchun

Studentlar:

O‘z baholari (Grade)ni ko‘radi.

Davomat (Attendance) holatini ko‘radi.

Dars jadvalini oladi.

Teacher bilan xabar almashadi (keyinchalik bot orqali ham).

Profilini yangilaydi.


_____________________________________________________________________________________________________________________________

🧠 7. core app — umumiy modellar va xizmatlar

core — bu barcha app’lar foydalanadigan umumiy “foundation”.
Bu yerda:

Faculty, Department, Subject, Group, Grade, Attendance, Schedule kabi modellar bo‘ladi.

BaseModel (created_at, updated_at)

signals.py (profil yaratish)

services/ (telegram, email, logging)

utils.py (slug generator, ID yaratish, random code)

_____________________________________________________________________________________________________________________________

🏛 1. academic (asosiy o‘quv obyektlar)
Model	Maydonlar	Aloqalar
Faculty	name, code	—
Department	name, code	Faculty
Group	name, year	Department
Subject	name, code, credit	Department
Schedule	subject, teacher, group, day, start_time, end_time	Subject + Teacher + Group
Grade	student, subject, score, exam_type	Student + Subject
Attendance	student, subject, date, status	Student + Subject


_________________________________________________________________________________________________________________________
👤 2. accounts (foydalanuvchilar bazasi)
Bu app barcha foydalanuvchilarni (Admin, Teacher, Student, Employee) yagona User modeli orqali boshqaradi.

Model	Maydonlar	Aloqalar
User	username, email, password, role (choices: admin, teacher, student, employee), is_active, date_joined	—
Profile	user, first_name, last_name, phone, gender, birth_date, address, image	User
role orqali foydalanuvchi turi aniqlanadi. Har biri o‘z appida qo‘shimcha ma’lumotlar bilan kengaytiriladi.


_________________________________________________________________________________________________________________________
🧑‍🏫 3. teachers (o‘qituvchilar ma’lumotlari)
Model	Maydonlar	Aloqalar
Teacher	user (OneToOne), department, position, specialization, degree	User + Department
TeacherSchedule	teacher, subject, group, day, start_time, end_time	Teacher + Subject + Group
TeacherActivity	teacher, description, date	Teacher


_________________________________________________________________________________________________________________________
🎓 4. students (talabalar ma’lumotlari)
Model	Maydonlar	Aloqalar
Student	user (OneToOne), student_id, group, enrollment_year, status	User + Group
StudentRecord	student, subject, grade, attendance	Student + Subject
StudentComplaint	student, message, created_at	Student


_________________________________________________________________________________________________________________________
🧰 5. employees (universitet xodimlari)
Model	Maydonlar	Aloqalar
Employee	user (OneToOne), position, department, hire_date, salary	User + Department
Task	employee, title, description, status, deadline	Employee
Report	employee, report_text, created_at	Employee

_________________________________________________________________________________________________________________________
🧑‍💼 6. admin_panel (boshqaruv va ruxsat tizimi)
Model	Maydonlar	Aloqalar
Role	name, description	—
Permission	code_name, description	—
RolePermission	role, permission	Role + Permission
UserRole	user, role	User + Role
Log	user, action, timestamp, ip_address	User
READMI
