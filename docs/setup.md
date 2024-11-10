# Project Setup Guide for Life Blood Squad

This guide will walk you through the setup process for running the Life Blood Squad project locally on Windows 11. 
The project uses an Anaconda environment, Python 3.10, and Flask for backend functionality.

## Prerequisites

Ensure that the following are installed on your system:

- **Anaconda**: For creating and managing the environment.
- **Python 3.10**
- **Git**: For version control.

## Setup Steps

### 1. Clone the Repository

Start by cloning the project repository:

```bash
git clone https://github.com/your-repo-url/life-blood-squad.git
cd life-blood-squad
```

### 2. Create a Virtual Environment

Using Anaconda, create and activate a virtual environment for this project:

```bash
conda create -n life-blood-env python=3.10
conda activate life-blood-env
```

### 3. Install Dependencies

Ensure you have a `requirements.txt` file in the project root directory. Use the following command to install the necessary dependencies:

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` File

In the root directory, create a `.env` file to store environment variables required by the project. Use the following structure (replace placeholder values with your actual data):

```plaintext
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL='mysql+pymysql://username:password@localhost/database_name'
SECRET_KEY='your_secret_key'
GOOGLE_MAPS_API='your_google_maps_api_key'
BASE_MAPS_URL='https://maps.googleapis.com/maps/api/distancematrix/json'
BASE_MAIL_ADDRESS='your_email_address@gmail.com'
ADMIN_MAIL_ADDRESS='admin_email_address@gmail.com'
MAIL_SERVER='smtp.gmail.com'
MAIL_PORT=587
MAIL_USERNAME='your_email@gmail.com'
MAIL_PASSWORD='your_email_password'
MAIL_USE_TLS=True
MAIL_USE_SSL=False
```

### 5. Start the Application

To run the application, use the following command:

```bash
python run.py
```

This will start the server. You should see output confirming the app is running, and you can access the site at `http://localhost:5000`.

## Working with Git

To keep your contributions organized, create a new branch for each feature or fix:

1. **Create a branch**:

   ```bash
   git checkout -b feature/branch-name
   ```

2. **Make your changes** and **commit** them:

   ```bash
   git add .
   git commit -m "Add your commit message here"
   ```

3. **Push to the branch** on the remote repository:

   ```bash
   git push origin feature/branch-name
   ```

4. **Create a Pull Request** from your branch to the main branch in the GitHub repository.

---

Following these steps, you should be able to set up, configure, and start developing on the Life Blood Squad project with ease. Happy coding!
