# Penguin Reads
Welcome to Penguin Reads: Your Linux Haven for Code Gems! 🐧💻 Immerse yourself in a byte-sized paradise of programming notes and tech blogs, guided by Penguin himself!

### Initial Setup:

Before taking the plunge into migrations, make sure to set up your environment. Create a `.env` file at the project's root with the following content:

```env
SECRET_KEY=your_secret_key_here
DEBUG=True  # Set to False in production

# Email Config
EMAIL_HOST_USER=your_mail@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

To generate app passwords, head to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).

### Run Migrations:

Let's get those migrations rolling for each app:

- **Users App:**
  ```bash
  python manage.py makemigrations users
  ```

- **Library App:**
  ```bash
  python manage.py makemigrations library
  ```

- **Blog App:**
  ```bash
  python manage.py makemigrations blog
  ```

### Apply Migrations:

Apply the migrations for all apps:

```bash
python manage.py migrate
```

### Create Superuser:

Want to wield superpowers? Create a superuser:

```bash
python manage.py createsuperuser
```