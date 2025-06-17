# 📊 Excelsior — AI-Powered Excel Assistant (MVP)

Excelsior is a backend system designed to enable natural language interaction with Excel spreadsheets. Users can upload `.xlsx` files and preview their structure via a REST API, setting the foundation for LLM-powered formula generation and data manipulation.

---

## ✅ Features (MVP Stage)
- Upload `.xlsx` Excel files and assign them UUIDs
- Persist uploaded files to `uploads/` directory
- Preview sheet names, column headers, and first 5 data rows

---

## 🚀 Getting Started

### 1. Clone + Set Up Environment
```bash
git clone <your_repo_url>
cd excelsior
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

### 2. Run the API
```bash
uvicorn main:app --reload
```

Open in browser: [http://127.0.0.1:8000/healthcheck](http://127.0.0.1:8000/healthcheck)

---

## 📂 Folder Structure
```
excelsior/
├── main.py
├── routers/
│   └── upload.py
├── services/
│   └── excel_parser.py
├── uploads/                # Uploaded Excel files
├── requirements.txt
```

---

## 🧪 API Endpoints

### `POST /upload-excel`
Upload an Excel file.

**form-data Body:**
- `file`: `.xlsx` file

**Response:**
```json
{ "file_id": "abc-123", "message": "File uploaded successfully" }
```

### `GET /preview-sheet/{file_id}`
Preview metadata from uploaded Excel file.

**Response:**
```json
{
  "sheets": ["Sheet1"],
  "headers": ["Name", "Region", "Sales", "Profit"],
  "sample": [
    ["Alice", "West", 1200, 300],
    ["Bob", "East", 950, 200]
  ]
}
```

---

## 🧪 Test via curl

### Upload File:
```bash
curl -X POST -F "file=@sample.xlsx" http://127.0.0.1:8000/upload-excel
```

### Preview File:
```bash
curl http://127.0.0.1:8000/preview-sheet/<file_id>
```

---

## 🔜 Coming Soon (Week 2+)
- Natural Language → Excel Formula (`/generate-formula`)
- LLM-assisted transformations (highlight, drop rows, etc.)
- File overwrite and download with modifications

---

## 🧠 Author
Built by Dylan as part of Project Excelsior 🚀