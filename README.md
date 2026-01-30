# FastPrint Technical Test

A Django project built for the FastPrint Junior Programmer specific test.

## Features
- Fetches products from external API securely.
- CRUD operations for products.
- PostgreSQL database integration.
- Filtering by status "bisa dijual".
- Responsive UI using Bootstrap 5.

## Prerequisites
- Python 3.8+
- PostgreSQL
- Pip

## Installation

1. **Clone the repository** (or extract files)
   ```bash
   cd fastprint_test
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Database**
   - Ensure PostgreSQL is running.
   - Create a database named `fastprint_db`.
   - Update `fastprint_test/settings.py` DATABASES section if your credentials differ from:
- User: your_db_user
- Password: your_db_password
- Host: `localhost`

4. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## Usage

### 1. Sync Data from API
This project includes a management command to fetch data from the recruitment API.
The API requires a dynamic username, so you must provide it as an argument.

```bash
python manage.py sync_products auto
```

Example:
```bash
python manage.py sync_products tesprogrammer001
```

This command will:
- Generate the required MD5 authentication hash.
- Fetch data from `recruitment.fastprint.co.id`.
- Store Categories, Statuses, and Products in the local database.

### 2. Run the Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000` in your browser.

## Project Structure
- `products/`: Main application containing Models, Views, Forms, and Management Commands.
- `fastprint_test/`: Project settings.
- `products/management/commands/sync_products.py`: Logic for API consumption.

## Notes
- **Authentication**: The API requires a password format of MD5(`bisacoding-DD-MM-YY`). This is handled automatically in `sync_products.py`.
- **Delete Confirmation**: Implemented using standard JavaScript `confirm()` in `product_list.html`.
