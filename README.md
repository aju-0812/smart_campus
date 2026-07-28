# Smart Campus Autonomous Multi-Agent AI System (Phase 1)

This project implements a modular, scalable, and high-performance **Smart Campus Autonomous Multi-Agent AI System** containing a central **Campus Orchestrator Agent** (built via **LangGraph**) routing queries to two specialized agents:
1. **Timetable Agent**: Features conflict detection and schedule optimization using a **Constraint Satisfaction Problem (CSP) / Genetic backtracking solver**.
2. **Attendance Agent**: Features course-wise attendance metrics and **predictive debarment risk alerts** trained via a **Random Forest classifier**.

---

## Technology Stack

* **Backend**: FastAPI (Python 3.11+), SQLAlchemy (ORM), LangGraph (Agentic Workflow), Scikit-Learn / Pandas / Numpy (ML/Data)
* **Frontend**: React.js, Vite, HSL-Tailored Dark Mode Styling System (Glassmorphic design)
* **Database**: PostgreSQL (or local SQLite for zero-setup execution out-of-the-box)
* **Deployment**: Docker, Docker Compose

---

## Project Structure

```text
smart-campus/
├── backend/
│   ├── app/
│   │   ├── api/             # API Router endpoints
│   │   ├── core/            # Database engine and config
│   │   ├── models/          # SQLAlchemy Database schemas
│   │   ├── schemas/         # Pydantic input/output validation models
│   │   ├── agents/          # LangGraph orchestrator and Backtracking CSP Solver
│   │   └── ml/              # Random Forest training and inference
│   ├── scripts/             # Database initialization and synthetic seeding
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/                 # React UI Dashboard components and styling
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Local Installation & Setup

### 1. Backend Setup
1. Open a terminal and navigate to the `backend/` folder:
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   # On Windows (PowerShell):
   .\.venv\Scripts\Activate.ps1
   # On Linux/macOS:
   source .venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Initialize the database and generate **550,000+ rows of synthetic data** (150 faculty, 250 classrooms, 300 courses, 2,500 students, 50,000 timetable slots, and 500,000 attendance logs):
   ```bash
   python scripts/seed_db.py
   ```
5. Start the FastAPI development server:
   ```bash
   python app/main.py
   ```
   The backend will be running at `http://127.0.0.1:8000`. You can inspect the Swagger docs at `http://127.0.0.1:8000/docs`.

### 2. Frontend Setup
1. Open a new terminal and navigate to the `frontend/` folder:
   ```bash
   cd frontend
   ```
2. Install npm packages:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   Open your browser and navigate to `http://localhost:5173`. You can log in using any sample student ID, such as `S10001`, `S10002`, or `S10003`.

---

## Running with Docker Compose

To build and run the entire application using containers:
```bash
docker-compose up --build
```
* Backend: `http://localhost:8000`
* Frontend: `http://localhost:5173`
