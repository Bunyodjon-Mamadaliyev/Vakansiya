# 🚀 JobConnect API

Xush kelibsiz

---

## 📌 Platforma Umumiy Ko'rinishi
JobConnect imkoniyatlari:

- 🧑‍💼 Ish beruvchilar kompaniya profillari yaratadi va ish e'lonlarini joylaydi
- 👨‍🎓 Ish izlovchilar rezyume tayyorlab, ishga ariza topshiradi
- 🔍 To‘liq imkoniyatli ish qidirish va filtrlash
- 🔔 Bildirishnomalar va 💡 aqlli ish tavsiyalari
- 📈 Real vaqt statistikasi va boshqaruv paneli

---

## 🔧 Texnologik Paket

- **Backend:** Django 4.2+, Django REST Framework 3.14+
- **Ma'lumotlar bazasi:** PostgreSQL
- **Avtorizatsiya:** JWT (djangorestframework-simplejwt)
- **Keshlash:** Redis
- **Hujjatlar:** Swagger / Redoc

---

## 🚦 API Imkoniyatlari

| Imkoniyat                 | Tavsif                                                                  |
|--------------------------|-------------------------------------------------------------------------|
| 👤 Avtorizatsiya          | JWT asosidagi kirish, ro'yxatdan o'tish va foydalanuvchini boshqarish   |
| 🏢 Ish Beruvchi Asboblari | Kompaniya profillari, ish e'lonlari, arizalarni boshqarish               |
| 🧑‍🎓 Ish Qidiruvchi Asboblari | Profil yaratish, rezyume yuklash, ariza tarixini ko‘rish               |
| 🔍 Qidiruv va Filtr       | Nom, kategoriya, joylashuv, maosh, tajriba bo‘yicha izlash               |
| 📨 Bildirishnomalar       | Ariza yangilanishlari va yangi ishlar haqida real vaqt ogohlantirish    |
| 📊 Statistika va Tahlillar| Ish ko‘rishlar, arizalar soni, yollash konversiyasi                     |

---

## 🔐 Avtorizatsiya Endpointlari

```
🔑 /api/auth/register/       [POST] - Yangi foydalanuvchini ro'yxatdan o'tkazish (qidiruvchi/beruvchi)
🔐 /api/auth/login/          [POST] - JWT orqali tizimga kirish
🔐 /api/auth/logout/         [POST] - Chiqish (tokenni qora ro'yxatga olish)
👤 /api/auth/user/           [GET]  - Tizimga kirgan foydalanuvchi ma'lumotlarini olish
```

---

## 🏢 Ish Beruvchi Endpointlari

```
🏭 /api/employers/profile/           [GET, POST]       - Kompaniya profilingizni yaratish/ko‘rish
📝 /api/employers/jobs/              [GET, POST]       - Ish joylashtirish / ro‘yxatini olish
📄 /api/employers/jobs/{id}/         [GET, PUT, DELETE] - Bitta ish e'lonini boshqarish
👀 /api/employers/jobs/{id}/apps/    [GET]             - Arizachilar ro'yxatini ko'rish
```

---

## 👨‍🎓 Ish Qidiruvchi Endpointlari

```
📄 /api/seekers/profile/            [GET, POST]        - Profil yaratish yoki yangilash
📎 /api/seekers/resume/             [POST]             - Rezyumeni yuklash (PDF, DOCX)
📤 /api/seekers/apply/{job_id}/     [POST]             - Ishga ariza topshirish
🕓 /api/seekers/applications/       [GET]              - Ariza tarixini ko‘rish
⭐ /api/seekers/saved-jobs/         [GET, POST]        - Sevimli ishlarni saqlash yoki ko‘rish
```

---

## 📚 Ish Ro'yxatlari va Filtrlar

```
🧭 /api/jobs/                      [GET]              - Barcha ishlar ro'yxati (sahifalangan)
🔍 /api/jobs/search/               [GET]              - Qidiruv va filtr (nom, kategoriya, joylashuv, va h.k.)
🎯 /api/jobs/{id}/                 [GET]              - Bitta ish tafsilotlari
📌 /api/jobs/{id}/recommendations/ [GET]              - O‘xshash ishlar tavsiyasi
```

---

## 🔔 Bildirishnomalar

```
🔔 /api/notifications/             [GET]              - Foydalanuvchi uchun barcha bildirishnomalar
📬 /api/notifications/mark-read/   [POST]             - Bildirishnomalarni o‘qilgan deb belgilash
```

---

## 📈 Statistika va Tahlil

```
📊 /api/stats/dashboard/           [GET]              - Ish ko‘rishlar, arizalar va trendlar
📈 /api/stats/user-activity/       [GET]              - Foydalanuvchiga oid faollik statistikasi
```

---

## 🧪 Testlash

- 🔬 `pytest-django` orqali view va serializer testlari
- ✅ Muhim biznes logikalar uchun 100% test qamrovi

---

## 🧾 O'rnatish

```bash
# Reponi klonlash
$ git clone https://github.com/Bunyodjon-Mamadaliyev/Vakansiya.git
$ cd Vakansiya

# Virtual muhit yaratish
$ python -m venv env 
$ source env/bin/activate

# Kutubxonalarni o‘rnatish
$ pip install -r requirements.txt

# Migratsiyalarni qo‘llash
$ python manage.py migrate

# Superuser yaratish
$ python manage.py createsuperuser

# Serverni ishga tushurish
$ python manage.py runserver
```

---

## 📖 API Hujjatlari

- Swagger UI: `http://localhost:8000/swagger/`
- Redoc: `http://localhost:8000/redoc/`

---

## 🌍 Versiyalash va Til

- Barcha APIlar `/api/v1/` bilan boshlanadi
- Accept-Language: `uz`, `en`, `ru` (yaqin kelajakda to‘liq qo‘llab-quvvatlanadi)

---

## 🔒 Xavfsizlik

- Yozish operatsiyalari uchun JWT autentifikatsiyasi talab qilinadi
- Foydalanuvchi faqat o‘ziga tegishli ma’lumotlarni ko‘ra va o‘zgartira oladi
- Fayl yuklash format va hajm bo‘yicha tekshiriladi
- Rate limiting va loglash tizimi mavjud

---

## 🧠 Tez Orada

- 🎯 AI asosidagi ish moslik algoritmi
- 📅 Suhbatga chaqiruv rejalashtirish
- 🔗 LinkedIn/Telegram OAuth orqali kirish

---


