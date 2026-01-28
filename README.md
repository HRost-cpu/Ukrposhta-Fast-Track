# 🇺🇦 Українська: Ukrposhta Fast-Track Pro
Ukrposhta Fast-Track Pro — це автоматизоване робоче місце оператора, розроблене для максимально швидкого створення поштових відправлень через API Укрпошти. Проєкт вирішує проблему складності офіційного API, де для реєстрації однієї посилки потрібно послідовно виконати 6 окремих запитів.

✨ Основні можливості:
Автоматизація "в один клік": Система самостійно реєструє адреси, клієнтів та створює ТТН (відправлення) одним натисканням кнопки.
Висока швидкість: Завдяки асинхронній архітектурі на базі httpx, запити до API обробляються паралельно.![ukrposhta](https://github.com/user-attachments/assets/e724df03-45e9-4aec-b8a0-c7afd012ce34)

Друк ярликів: Миттєва генерація та завантаження PDF-стікерів для маркування посилок.
Сучасний інтерфейс: Адаптивний дизайн з підтримкою темної теми.
Portable-запуск: Автоматичне налаштування середовища (Python 3.12, venv, залежності) через один файл launch.bat.

🛠 Технологічний стек:
Backend: Flask (Async mode), HTTPX.
Frontend: Tailwind CSS, JavaScript (ES6+).
DevOps: uv package manager для миттєвого розгортання.

🚀 Швидкий старт:
Клонуйте репозиторій.
Запустіть файл launch.bat.
Введіть свій Bearer Token в інтерфейсі та починайте роботу.

# 🇺🇸 English: Ukrposhta Fast-Track Pro
Ukrposhta Fast-Track Pro is an automated operator console designed to streamline the creation of shipments via the Ukrposhta API. This project simplifies the complex API workflow, which typically requires 6 sequential steps to register a single parcel.

✨ Key Features:
One-Click Automation: The system automatically handles address registration, client creation, and shipment (TTN) generation in one go.
High Performance: Utilizes an asynchronous architecture powered by httpx to process API requests in parallel.
Sticker Printing: Instant generation and download of PDF shipping labels.
Modern UI: Responsive design, featuring a native dark mode.
Zero Configuration: A launch.bat file automatically sets up Python 3.12, the virtual environment, and all dependencies using the uv manager.

🛠 Tech Stack:
Backend: Flask (Async mode), HTTPX.
Frontend: Tailwind CSS, JavaScript (ES6+).
DevOps: uv package manager for instant environment provisioning.

🚀 Quick Start:
Clone the repository.
Run the launch.bat file.
Enter your Bearer Token in the console and start shipping.
