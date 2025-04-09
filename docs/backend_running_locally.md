# 🚀 Running Locally

This guide provides all the necessary steps to run the **GPT Not Found** backend project locally using **Python** and **FastAPI**.

---

## ✅ Prerequisites

Before proceeding, ensure that you have the following tools installed:

- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/)

---

## 📦 Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/AlvaroLucioRibeiro/GPT-Not-Found-Backend.git
cd GPT-Not-Found-Backend
```

---

### 2. Create a Virtual Environment

To isolate your project dependencies, create a virtual environment:

```bash
python -m venv venv
```

---

### 3. Activate the Virtual Environment

#### On **Linux/MacOS**:

```bash
source venv/bin/activate
```

#### On **Windows** (Command Prompt):

```cmd
venv\Scripts\activate
```

#### On **Windows** (PowerShell):

```powershell
venv\Scripts\Activate.ps1
```

---

### 4. Install Dependencies

Make sure you have the `requirements.txt` file in the root directory. Then install all dependencies:

```bash
pip install -r requirements.txt
```

---

### 5. Run the Application

With everything set up, you can now run the FastAPI app:

```bash
python src/main.py
```

This will start the server and expose the API locally.

---

### 6. Access the API Docs

Once running, open your browser and navigate to:

```
http://127.0.0.1:8000/docs
```

This will open the **Swagger UI**, where you can test the endpoints.

---
