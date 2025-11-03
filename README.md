## FastAPI File Server

Xavfsiz va cheklangan fayl saqlash xizmati: fayllarni yuklash, diskda shifrlab saqlash, autentifikatsiya va rate limiting bilan himoyalash, kunlik papkalar bo'yicha saqlash, SHA-256 orqali dublikatlarni aniqlash, Tortoise ORM bilan Postgres bazasida yozuvlarni yuritish va `app/file_records.xlsx` faylida tarixni log qilish.

### Xususiyatlar

#### Yangi qo'shilgan xususiyatlar (2025-11-03)

1. **Fayl formatlari cheklovi**
   - Ruxsat etilgan fayl turlari:
     - txt (text/plain)
     - pdf (application/pdf)
     - png (image/png)
     - jpg/jpeg (image/jpeg)
     - doc (application/msword)
     - docx (application/vnd.openxmlformats-officedocument.wordprocessingml.document)
   - Maksimal fayl hajmi: 50MB

2. **Xavfsizlik qo'shimchalari**
   - Fayllarni shifrlash (Fernet encryption)
   - JWT token asosida autentifikatsiya
   - Rate limiting:
     - Yuklash: 10 ta so'rov/minutiga
     - Yuklab olish: 30 ta so'rov/minutiga

#### Asosiy xususiyatlar
- **/upload/** orqali fayl yuklash (`multipart/form-data`)
- **Dublikatlarni aniqlash**: fayl hash (SHA-256) bo'yicha
- **Kunlik kataloglar**: `app/uploaded_files/YYYY-MM-DD/`
- **Excel log**: `app/file_records.xlsx` ga har bir yozuv
- **Postgres**: Tortoise ORM orqali `files` jadvali
- **Faylni olish**: `GET /{date}/{filename}`

### Texnologiyalar
- FastAPI, Starlette
- Tortoise ORM (Postgres)
- Pydantic v2
- Pandas (Excel log uchun)
- Uvicorn (ASGI server)

---

## O'rnatish

1) Python 3.12 tavsiya etiladi. Virtual muhit yaratish:

```bash
python -m venv env
env\Scripts\activate
```

2) Redis o'rnatish (Rate limiting uchun):

Windows uchun:
- Redis serverni yuklab oling: https://github.com/microsoftarchive/redis/releases
- O'rnatish va ishga tushirish

Linux uchun:
```bash
sudo apt-get install redis-server
sudo service redis-server start
```

3) Kutubxonalarni o'rnatish:

```bash
pip install -r requirements.txt
```

Eslatma: Agar `requirements.txt` kodlash muammosi sabab o'qilmasa, quyidagilarni qo'llab turing: faylni UTF-8 sifatida saqlash yoki muhim paketlarni qo'lda o'rnatish (`fastapi`, `uvicorn`, `tortoise-orm`, `python-dotenv`, `pandas`, `openpyxl`, `psycopg2-binary`).

3) .env faylini yarating (loyiha ildizida):

```env
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_NAME=files_db
DATABASE_HOST=127.0.0.1
```

Postgres lokal serveringizda mos ravishda qiymatlarni kiriting. Ulanish satri `postgres://{USER}:{PASSWORD}@{HOST}/{NAME}` formatida ishlatiladi.

4) Bazani tayyorlash

Ilova ishga tushganda Tortoise `generate_schemas=True` orqali jadval(lar)ni yaratadi. Alohida migratsiya bosqichi talab qilinmaydi.

---

## Ishga tushirish

Variant A (skript orqali):

```bash
python manage.py
```

Variant B (qo'lda):

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Brauzer: `http://127.0.0.1:8000`

OpenAPI hujjatlari: `http://127.0.0.1:8000/docs`

---

## API

- `GET /` – Sog'liq tekshiruvi. `{ "message": "Project is working!" }` qaytaradi.

- `POST /upload/` – Fayl yuklash
  - Body: `multipart/form-data` (kalit: `file`)
  - Muvaffaqiyat: `{ "message": "File uploaded successfully", "url": "/YYYY-MM-DD/<saved_name>" }`
  - Agar dublikat bo'lsa: `{ "message": "File already exists", "url": "/YYYY-MM-DD/<saved_name>" }`

- `GET /{date}/{filename}` – Faylni yuklab olish
  - `date` formati: `YYYY-MM-DD`
  - `filename`: saqlangan nom (`app/utils/file.py` uni vaqt prefiksi bilan yaratadi)

### cURL namunalar

```bash
# Fayl yuklash
curl -X POST "http://127.0.0.1:8000/upload/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/local/file.png"

# Yuklangan faylni olish
curl -O "http://127.0.0.1:8000/2025-10-30/20251030212602905303_db404bf2e8d24de9b6dacbf3b9ec41e0"
```

---

## Arxitektura ko'rinishi

- `app/main.py` – FastAPI ilovasi, routerlarni ulash, Tortoise ro'yxatdan o'tkazish
- `app/database.py` – Tortoise ORM sozlamalari va ulanish hayoti
- `app/models/file.py` – `files` jadvali modeli
- `app/schemas/file.py` – Pydantic sxemalari
- `app/routers/file.py` – Yuklash va faylni qaytarish endpointlari
- `app/utils/file.py` – Diskka saqlash hamda Excel log funksiyalari
- `app/uploaded_files/` – Fayllar saqlanadigan papka (kun bo'yicha)
- `app/file_records.xlsx` – Yozuvlar Excel logi

---

## Ishlash mantig'i (qisqa)

1) `POST /upload/` faylni qabul qiladi va butun fayl bo'yicha SHA-256 hash hisoblaydi.
2) Agar `files.hash_code` bo'yicha mavjud yozuv topsa – dublikat deb belgilanadi va oldingi fayl URL'i qaytariladi.
3) Aks holda, fayl `app/uploaded_files/YYYY-MM-DD/` ichida noyob nom bilan saqlanadi.
4) Yozuv Tortoise ORM orqali Postgres bazasiga va qo'shimcha ravishda `app/file_records.xlsx` ga qo'shiladi.

---

## Muhit va xavfsizlik eslatmalari

- Yuklangan fayllar ommaga ochiq yo'l orqali qaytariladi. Agar xususiy saqlash kerak bo'lsa, avtorizatsiya va ruxsat nazoratini qo'shing.
- Fayl hajmi cheklovlari, ruxsat etilgan MIME turlarini whitelisting qilish tavsiya etiladi.
- Excel log (pandas) yirik hajmda sekinlashishi mumkin; uzoq muddat uchun faqat DB'ga tayanish yoki alohida audit jadvali tavsiya etiladi.

---

## Rivojlantirish

- Test uchun `http://127.0.0.1:8000/docs` dan foydalaning.
- Windows muhitida yo'l ajratkichlari (`\\` va `/`) bilan ehtiyot bo'ling; kod `os.path.join` ishlatadi.

---

## Litsenziya

Ushbu loyiha uchun litsenziya ko'rsatilmagan. Kerak bo'lsa `LICENSE` fayli qo'shing.

---

## Qo'shimcha muhim sozlamalar (yangilangan)

Quyidagi sozlamalar loyiha ishga tushishi uchun muhim. Loyihaning ildizida `.env` fayl yarating va kerakli qiymatlarni kiriting.

Masalan:

```env
# To'liq DB URL (Postgres yoki boshqa)
DATABASE_URL=postgres://user:password@127.0.0.1/dbname

# Redis (rate limiter uchun)
REDIS_URL=redis://localhost:6379

# JWT token yaratish uchun maxfiy kalit
JWT_SECRET_KEY=change_this_to_a_strong_secret

# Fernet kaliti (fayllarni shifrlash uchun)
# PowerShell misol (kalit yarating va .env ga joylang):
# python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
FERNET_KEY=<your_fernet_key_here>

# TESTING=1 — test muhitida ilova 500 xatolariga traceback JSON qo'shadi (faqat testlar uchun)
TESTING=1
```

Eslatma: agar `FERNET_KEY` ni bermasangiz, ilova ishga tushganda yangi kalit yaratadi; productionda kalitni doimiy saqlash zarur.

## Testlar

Qanday ishlatish:

1. Virtual muhitni faollashtiring va dependencylarni o'rnating:

```powershell
env\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Redis serverni ishga tushuring (mahalliy) yoki `REDIS_URL` ni moslab bering.

3. Testlarni ishga tushirish:

```powershell
# Barcha testlar
pytest -q

# Yoki bitta testni -s bilan, tracebackni konsolga chiqarish uchun
pytest tests/test_app.py::test_upload_with_token -q -s -vv
```

Eslatma: testlar Tortoise uchun in-memory sqlite ishlatadi va FastAPILimiter uchun Redis talabi mavjud.

## Qo'shilgan xususiyatlar (qisqacha)

- Fayl turlari va hajmi cheklovi (ALLOWED_EXTENSIONS va MAX_FILE_SIZE = 50MB)
- Fayllarni diskga yozishdan avval Fernet bilan shifrlash
- JWT token asosidagi autentifikatsiya (`/token` - test endpoint)
- Redis asosidagi rate limiting (fastapi-limiter)
- Testlar: `tests/test_app.py` (async httpx AsyncClient + tortoise in-memory DB)

## Git — commit va push (PowerShell)

Quyidagi buyruqlar sizning o'zgartirishlaringizni commit qilib remote ga yuboradi. Agar yangi branch ochmoqchi bo'lsangiz, `feature/tests` nomi misol.

```powershell
# Joriy o'zgartirishlarni tekshirish
git status

# (Ixtiyoriy) yangi branch yaratish va unga o'tish
git checkout -b feature/tests

# O'zgartirishlarni stage qilish
git add -A

# Commit qilish
git commit -m "Add file validation, encryption, JWT auth, rate limiting and tests"

# Remote ga push qilish (yangi branch uchun upstream bilan)
git push -u origin feature/tests

# Agar master branchda commit qilsangiz va bevosita master ga push qilmoqchi bo'lsangiz:
git push origin master
```

PR tavsiyasi: master ga bevosita push qilishdan oldin branch yaratib, GitHub orqali Pull Request ochib ko'rib chiqishni tavsiya qilamiz.

---

Agar READMEda qo'shimcha o'zgartirish yoki tarjima kerak bo'lsa, qaysi bo'limga ko'proq detallar kerakligini ayting va men yangilayman.


