📊 Excelsior — AI-Powered Excel Assistant (MVP)

Excelsior is a backend system designed to enable natural language interaction with Excel spreadsheets. Users can upload `.xlsx` files and preview their structure via a REST API, setting the foundation for LLM-powered formula generation and data manipulation.


✅ Features (MVP Stage)
- Upload .xlsx files and persist them by file_id
- Preview sheet names, headers, and top 5 rows via API
- FastAPI service and core file structure
- Defined models, routers, and utilities for clean modularity
- cURL-based upload and preview testing support
- LLM integration via /generate-formula scaffold

---

🚀 Quick Start

1. Clone & Install
# Clone the repo
git clone <your_repo_url>
cd excelsior

# Create & activate virtual environment
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

2. Launch the API
uvicorn main:app --reload
Browse to http://127.0.0.1:8000/healthcheck to confirm the service is up.

📑 API Reference
# POST /upload-excel
# Upload an Excel workbook.

# Form‑Data:
Key	  Type	Description
file	File	The .xlsx file

# Response 
{
  "file_id": "abc-123",
  "message": "File uploaded successfully"
}

# GET /preview-sheet/{file_id}
# Retrieve basic metadata and a sample of the uploaded workbook.

# Response
{
  "sheets": ["Sheet1"],
  "headers": ["Name", "Region", "Sales", "Profit"],
  "sample": [
    ["Alice", "West", 1200, 300],
    ["Bob",   "East",  950, 200]
  ]
}

# 🧪 cURL Examples

# 1. Upload a workbook
curl -X POST -F "file=@sample.xlsx" \
     http://127.0.0.1:8000/upload-excel

# 2. Preview its contents
curl http://127.0.0.1:8000/preview-sheet/<file_id>

🔧 Future Plans / MVP Improvements
- Add React frontend with react-data-grid for editable sheet display
- Integrate local SLM to parse user commands to optimize functionality
- Replace in-memory file cache with Redis for multi-user support
- Enable file overwrite and modification tracking
- Develop WebSocket sync for real-time collaboration (multi-user live editing)
- Add authentication and per-user file isolation using Supabase or JWT (Spring Boot)
- Write unit + integration tests for every route and service layer
- Dockerize for full backend deployment and dev consistency

🧑‍💻 Author

Created by Dylan Hoang for Project Excelsior 🚀