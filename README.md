# PC Shops Parser

## Tavsif
**PC Shops Parser** - bu onlayn do'konlardagi barcha noutbuklarni bir joyga to'plash va qidirishni osonlashtirish uchun yaratilgan parser. Ushbu loyiha turli e-commerce saytlaridan ma'lumotlarni yig'ib, yagona ma'lumotlar bazasida jamlaydi.

## Ishlatilgan texnologiyalar
- **Python 3.x**
- **BeautifulSoup4** (BS4) - HTML sahifalarni tahlil qilish uchun
- **Selenium** - Dinamik sahifalarni yuklab olish uchun
- **Django** - Backend va API uchun
- **SQLite** - Ma'lumotlar bazasi uchun

## O'rnatish

1. Loyihani klonlash:
   ```bash
   git clone https://github.com/username/pc-shops-parser.git
   cd pc-shops-parser
   ```
2. Virtual muhit yaratish va faollashtirish:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux yoki MacOS
   .venv\Scripts\activate  # Windows
   ```
3. Talab qilinadigan kutubxonalarni o'rnatish:
   ```bash
   pip install -r requirements.txt
   ```
4. Django ma'lumotlar bazasini sozlash:
   ```bash
   python manage.py migrate
   ```
5. Selenium uchun WebDriver'ni sozlash (Google Chrome yoki Firefox):
   ```bash
   wget https://chromedriver.storage.googleapis.com/version/chromedriver_linux64.zip  # Linux uchun
   ```
   Yoki Windows uchun [rasmiy sahifadan](https://chromedriver.chromium.org/downloads) yuklab oling.

## Ishga tushirish

1. Django serverini ishga tushirish:
   ```bash
   python manage.py runserver
   ```
2. Parserni ishga tushirish:
   ```bash
   python main.py
   ```

## Muallif
- **GitHub** - [axmadJ3](https://github.com/axmadJ3)

