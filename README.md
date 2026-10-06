# 🎓 Student Performance Analyzer

A clean, fully functional web application built with **Python** and **Streamlit** to analyze student academic performance from a CSV file.

---

## ✨ Features

- 📂 **CSV Upload** — Upload any CSV file with student marks
- ✅ **Data Validation** — Validates required columns and mark ranges (0–100)
- 📊 **Auto Calculations** — Total, Average, Percentage, Grade, Pass/Fail for every student
- 📈 **Dashboard Metrics** — Total students, class average, highest average, pass/fail rates
- 🏆 **Top 5 Students** — Ranked by average marks
- 📚 **Subject-wise Averages** — Class performance per subject
- 📉 **Charts** — Grade distribution, pass/fail pie chart, subject averages bar chart
- 🔍 **Student Search** — Search by name
- 👤 **Student Profile** — Detailed view with per-subject bar chart and weakest subject
- 💡 **Performance Insights** — Auto-generated insights from actual data
- 💾 **Download Results** — Export analyzed data as CSV
- ⚙️ **Adjustable Passing Mark** — Set any passing threshold via sidebar slider

---

## 🛠️ Technologies

| Technology   | Purpose                        |
|--------------|-------------------------------|
| Python 3.9+  | Core language                 |
| Streamlit    | Web UI framework              |
| Pandas       | Data loading and manipulation |
| Matplotlib   | Charts and visualizations     |

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/student-performance-analyzer.git
cd student-performance-analyzer
```

### 2. (Recommended) Create a virtual environment

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 📄 CSV Format

Your CSV file must have exactly these columns (case-sensitive):

```
Name,Math,Science,English,Computer
```

**Example:**

```csv
Name,Math,Science,English,Computer
Alice Johnson,92,88,95,90
Bob Smith,74,65,70,78
Carol White,85,91,82,88
```

**Rules:**
- All subject marks must be numeric values between **0** and **100**.
- Student names must not be empty.
- Column headers must match exactly.

A ready-to-use sample file `sample_students.csv` (20 students) is included in the project.

---

## 🎓 Grading System

| Grade | Range     |
|-------|-----------|
| A+    | 90 – 100  |
| A     | 80 – 89   |
| B     | 70 – 79   |
| C     | 60 – 69   |
| D     | 50 – 59   |
| E     | 40 – 49   |
| F     | Below 40  |

Default passing mark: **40** (adjustable via sidebar).

---

## 📁 Project Structure

```
student-performance-analyzer/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── sample_students.csv     # Sample data (20 students)
├── README.md               # Project documentation
└── .gitignore              # Git ignore rules
```

---

## 🚀 GitHub Instructions

### Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Student Performance Analyzer"
git branch -M main
git remote add origin https://github.com/your-username/student-performance-analyzer.git
git push -u origin main
```

### Deploy on Streamlit Cloud (optional)

1. Push the repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Click **New app** → select your repo → set main file to `app.py`.
4. Click **Deploy**.

---

## 📸 App Sections

1. **Sidebar** — Upload CSV and adjust passing mark
2. **Class Summary** — 5 metric cards (students, average, highest, pass/fail rates)
3. **Performance Insights** — Auto-generated text insights
4. **Visual Analytics** — Bar and pie charts
5. **Top 5 Students** — Ranked table
6. **Subject Averages** — Per-subject class averages
7. **Complete Results Table** — All students with color-coded pass/fail
8. **Search** — Find a student by name
9. **Student Profile** — Individual marks, grade, weakest subject, chart
10. **Download** — Export full results as CSV

---

## 📜 License

MIT License — free to use and modify.
