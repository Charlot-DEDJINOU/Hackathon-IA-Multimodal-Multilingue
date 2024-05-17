# SMART-VT-APP

Welcome to the backend of SMART-VT-APP project! This guide will help you clone the project, set up the backend, and start the FastAPI server. Follow each step carefully for a successful installation.

## Prerequisites

- Kali Linux (or another Linux distribution)
- Python 3.x
- Git
- Stable internet connection

## 1. Clone the Project

Start by cloning the project's GitHub repository using the following command:
```bash
git clone https://github.com/mathias-kinninkpo/SMART-VT-APP.git
```

## 2. Set Up the Backend

### 2.a Configure the Virtual Environment

1. Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2. Create a virtual environment:
    ```bash
    python -m venv myenv
    ```
3. Activate the virtual environment:
    ```bash
    source myenv/bin/activate
    ```
4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### 2.b Environment Variables

Before starting the server, you need to set up environment variables. Create a `.env` file in the `backend` directory and add the following lines:

```env
MONGO_URI=mongodb+srv://username:password@dbname.id.mongodb.net/
DATABASE_NAME=your_dbname
API_KEY="api key for assembly ai" ## Optional
BASE_URL=your_base_url ## For example: http://127.0.0.1:8000/
```

- **MONGO_URI**: The connection URI for your MongoDB database.
- **DATABASE_NAME**: The name of your MongoDB database.
- **API_KEY**: An API key for Assembly AI (optional).
- **BASE_URL**: The base URL of your project (e.g., `http://127.0.0.1:8000/`).

### 2.c Start the FastAPI Server

Start the FastAPI server using the following command:

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

## Conclusion

Your FastAPI server should now be running at `http://127.0.0.1:8000/`. You are ready to start using SMART-VT-APP!

If you encounter any issues or have questions, feel free to check the documentation or open an issue on the GitHub repository.
