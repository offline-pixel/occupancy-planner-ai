# Occupancy Planner Backend

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-green.svg)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.7.4-blueviolet.svg)](https://docs.pydantic.dev/)

A FastAPI backend service that provides intelligent workspace recommendations based on natural language queries and real-time occupancy data.

## Features

- Natural language processing for workspace queries
- Real-time occupancy data integration
- Desk recommendation engine
- Policy-aware filtering
- Modular architecture with clean separation of concerns

## 🚀 Quick Demo

**Watch a short demo of the system in action:**

<video src="https://github.com/offline-pixel/occupancy-planner-ai/raw/main/frontend.mov" width="800" controls autoplay loop muted></video>

**Note:** The video may take a moment to load depending on your internet connection.

## Project Structure

```bash
occupancy-planner/
├── backend/
│   ├── app/                  # Core application logic
│   │   ├── models/           # Pydantic data models
│   │   ├── routers/          # API endpoint definitions
│   │   ├── services/         # Business logic services
│   │   └── main.py          # FastAPI app initialization
│   ├── data/                # Static data files
│   │   ├── verge_spaces.json
│   │   ├── verge_desks.json
│   │   └── ...
│   ├── venv/                # Virtual environment
│   ├── .env.example         # Environment variables template
│   ├── main.py              # Application entry point
│   ├── requirements.txt     # Dependencies
│   └── README.md            # This file
```

### Installation
Clone the repository

```bash
git clone https://github.com/your-username/occupancy-planner.git
cd occupancy-planner/backend
```
Set up Python 3.13 environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies with compatibility fixes

```bash
export PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 # optional
pip install --no-cache-dir -r requirements.txt
```
NOTE: Do install these two as well as per your system requirements post setting up your virtual environment
```
pip3 install spacy
python3 -m spacy download en_core_web_sm
```

Set up environment variables

```bash
cp .env.example .env
# Edit .env with your actual values
```
Running the Application
```bash
uvicorn main:app --reload
```
The API will be available at http://localhost:8000


### API Documentation
Interactive documentation is automatically available at:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

### Key Components
Data Models (`app/models/data_models.py`)

**Space**: Physical workspace areas

**Desk**: Individual workstations

**OccupancyData**: Real-time usage metrics

**ParsedQuery**: Structured query representation

### Services (`app/services/`)
`data_loader.py`: Manages static data loading

`llm_service.py`: Natural language processing

`recommendation_service.py`: Desk recommendation logic

### API Endpoints (`app/routers/occupancy.py`)
`POST /api/v1/query-occupancy`: Main recommendation endpoint

`GET /api/v1/data/spaces`: Debug endpoint for space data

`GET /api/v1/data/desks`: Debug endpoint for desk data

### Example Usage
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/query-occupancy",
    json={"query_text": "Find me a quiet desk near window on 3rd floor for tomorrow morning"}
)
print(response.json())
```


### License
Distributed under the MIT License. See LICENSE for more information.

### Contact
Creator - [Deepak Ranolia] - d.ranolia92@gmail.com

## Support This Project

If you find this project useful, consider supporting its development:

[![Donate with PayPal](https://img.shields.io/badge/Donate-PayPal-blue.svg?logo=paypal)](https://www.paypal.com/paypalme/dranolia)
