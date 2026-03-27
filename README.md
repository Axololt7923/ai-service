![FastAPi](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-8E75B2?style=flat&logo=googlegemini&logoColor=white)
![Sentence Transformers](https://img.shields.io/badge/Sentence_Transformers-FFD21E?style=flat&logo=huggingface&logoColor=black)
![CUDA](https://img.shields.io/badge/PyTorch-%2B_CUDA-EE4C2C?style=flat&logo=pytorch&logoColor=white)
![MakeFile](https://img.shields.io/badge/MakeFile-003366?style=flat&logo=database&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6F61?style=flat&logo=database&logoColor=white)

# JobMatch AI Service

AI service for CV parsing and job recommendation, built with FastAPI and ChromaDB.

## Tech Stack

- **FastAPI** — REST API framework
- **Google Gemini** — CV parsing
- **Sentence Transformers** — Text embedding (paraphrase-multilingual-MiniLM-L12-v2)
- **ChromaDB** — Vector database for similarity search

## Project Structure
```
ai-service/
├── app/
│   ├── main.py              # FastAPI entrypoint
│   ├── config.py            # Configuration & model initialization
│   ├── routers/
│   │   ├── cv.py            # CV parsing endpoints
│   │   └── recommend.py     # Job recommendation endpoints
│   ├── services/
│   │   ├── cv_parser.py     # PDF parsing with Gemini
│   │   ├── embedder.py      # Text embedding with MiniLM
│   │   └── vector_store.py  # ChromaDB operations
│   └── schemas/
│       ├── cv.py            # CV request/response schemas
│       └── job.py           # Job request/response schemas
├── requirements.txt
├── Makefile
└── README.md
```

## Prerequisites

- Python 3.14
- CUDA-compatible GPU (optional, CPU fallback supported)
- Google Gemini API key

> [!WARNING]
> **Warning about GPU:** Currently, this project is only configured and tested for GPU support on Windows. If you are using Linux or macOS, you may need to modify the installation script to accommodate your specific CUDA installation.

## Installation

1. ***Clone the repository***
```bash
git clone https://github.com/Axololt7923/ai-service.git
cd ai-service
```
2. ***Create virtual environment***

* **Windows:**
```bash
python -m venv venv
.venv/Scripts/activate
make install
```

* **Linux/MacOS:**
```bash
python -m venv venv
source venv/bin/activate
make install
```

> [!WARNING]
> **Warning for Windows users:** If you are using Windows, you may need to install the `make` utility.
```bash
    choco install make
```

3. ***Create `.env` file***
```
GEMINI_API_KEY=your_gemini_api_key
CHROMA_PATH=./chroma_data
SENTENCE_TRANSFORMERS_HOME=./models

#Optional
HF_TOKEN=your_huggingface_token
```
*(Optional: Set `HF_TOKEN` to your HuggingFace token to get faster model downloads)*

## Running
```bash
make run
```

## API Reference

The project provides a RESTful API system. You can view the full interactive documentation (Swagger UI) by running the server and accessing `/docs`.

### Authentication

Most APIs (except `/health`) require authentication using an API Key.

* **Header:** `X-API-KEY`
* **Value:** `<YOUR_API_KEY>`

### Endpoint List

| Tag        |  Method  | Endpoint                  | Description                                              |
|:-----------|:--------:|:--------------------------|:---------------------------------------------------------|
| **CV**     |  `POST`  | `/cv_parsed`              | Extract, analyze, and store a CV (Upload PDF).           |
| **CV**     |  `GET`   | `/cv_parsed`              | Retrieve a list of parsed CVs (with pagination).         |
| **CV**     | `DELETE` | `/cv_parsed/{chroma_id}`  | Delete a CV from the database.                           |
| **Job**    |  `POST`  | `/jobs`                   | Create or update job information (Upsert Job).           |
| **Job**    |  `GET`   | `/jobs`                   | Retrieve job listings (with pagination or filter by ID). |
| **Job**    |  `GET`   | `/jobs/recommend/{cv_id}` | **[AI Core]** Recommend the most suitable jobs for a CV. |
| **Job**    | `DELETE` | `/jobs/{chroma_id}`       | Delete a job.                                            |
| **System** |  `GET`   | `/health`                 | Check the server status.                                 |

---

### Core API Details

#### 1. CV Processing and Parsing (`POST /cv_parsed`)

Receives a CV file, processes it using AI, generates vector embeddings, and stores it in the database.

* **Content-Type:** `multipart/form-data`

**Request Body:**

* `file` (binary): CV file (PDF)
* `user_id` (string): ID of the user who owns the CV

**Response (200 OK):**

```json
{
  "chroma_id": "string",
  "skills": ["Python", "FastAPI"],
  "experience_years": 2.5,
  "education_level": "string",
  "languages": ["English", "Vietnamese"],
  "summary": "string"
}
```

---

#### 2. Add Job Data (`POST /jobs`)

Add a new job description to the system to be used for matching.

* **Content-Type:** `application/json`

**Request Body:**

```json
{
  "job_id": "string",
  "title": "string",
  "description": "string",
  "requirements": "string",
  "company": "string"
}
```

---

#### 3. Smart Job Recommendation (`GET /jobs/recommend/{cv_id}`)

Performs semantic matching between a stored CV and the job database to find the most suitable jobs.

* **Path Parameters:**

  * `cv_id` (String): ID of the parsed CV (`chroma_id`)

* **Query Parameters:**

  * `top_k` (Integer): Number of job recommendations (Default: 10)

**Response (200 OK):**

```json
[
  {
    "job_id": "string",
    "similarity": 0.92
  }
]
```

## Environment Variables

| Variable                     | Description                   | Required                                   |
|------------------------------|-------------------------------|--------------------------------------------|
| `GEMINI_API_KEY`             | Google Gemini API key         | Yes                                        |
| `CHROMA_PATH`                | ChromaDB storage path         | No (default: ./chroma_data)                |
| `SENTENCE_TRANSFORMERS_HOME` | Model cache path              | No (default: ~/.cache)                     |
| `HF_TOKEN`                   | HuggingFace token             | No                                         |
| `FIXED_API_KEY`              | Fixed API key for testing     | No (default: "random-api-key-12345678910") |
| `ENABLE_API_KEY`             | Enable API key authentication | No (default: true)                         |


## Deployment
FUTURE UPDATES