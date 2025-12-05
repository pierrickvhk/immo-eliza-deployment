# 🏡 Immo Eliza Price Predictor

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-success.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-ff4b4b.svg)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue.svg)](https://www.docker.com/)
[![Render](https://img.shields.io/badge/Render-Deployed-46e3b7.svg)](https://render.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

End-to-end Machine Learning · FastAPI · Docker · Streamlit  
Predicting Belgian real estate prices using structural, comfort, and location features.

---

# 📁 Project Root Structure

```root
immo-eliza-deployment/
│
├── api/
│   ├── __init__.py
│   ├── app.py
│   ├── predict.py
│   ├── schemas.py
│   └── test_api.py
│
├── streamlit/
│   └── app.py
│
├── .dockerignore
├── .gitignore
├── dockerfile
├── README.md
└── requirements.txt
```

---

## 🚀 Project Overview

This project simulates a complete production-like workflow, transforming a trained ML model into a fully deployed application accessible both for developers and end users.

### It includes:

### ✔ Machine Learning
- Scikit-Learn Random Forest model  
- Clean preprocessing pipeline  
- Feature transformation  
- Prediction + derived price per m²  

### ✔ Backend (FastAPI)
- Fully validated JSON schemas  
- Robust error handling  
- Clear OpenAPI documentation  
- Dockerized  
- Deployed on Render  

### ✔ Frontend (Streamlit)
- Full UI redesign  
- Custom banner & background  
- Smart layout & grouping  
- Random Example Generator  
- Live API predictions  
- User-friendly experience  

---

## 🔧 Installation

### 1. Clone the repository

git clone https://github.com/pierrickvhk/immo-eliza-deployment.git
cd immo-eliza-deployment

## 🖥 Run FastAPI Backend Locally

    cd api
    uvicorn api.app:app --reload

API Docs available at:  
➡️ http://127.0.0.1:8000/docs  

---

## 🎨 Run Streamlit Frontend

    cd streamlit
    streamlit run app.py

The UI includes:
- Banner & background styling  
- Professional layout  
- Real-time API calls  
- Random example generator  
- Error-safe UX  

---

## 🐳 Docker Usage

**Build the container**

    docker build -t immo-eliza-api .

**Run the container**

    docker run -p 8000:8000 immo-eliza-api

Your API now runs at:  
➡️ http://localhost:8000  

---

## 📡 Example API Request

    {
      "data": {
        "property_type": "house",
        "subtype_of_property": "bungalow",
        "location": {
          "province": "Antwerpen",
          "postcode": 2000,
          "locality": "Antwerpen",
          "region": "Vlaanderen",
          "country": "Belgium"
        },
        "number_of_bedrooms": 3,
        "livable_surface": 120,
        "total_land_surface": 300,
        "number_of_bathrooms": 1,
        "terrace": true,
        "garden": true
      }
    }

---

## ❤️ My Personal Experience

This project was an incredibly enjoyable part of my AI & Data Science journey.

I truly loved:
- Seeing raw data evolve into a working ML model  
- Transforming the model into a real API  
- Running everything inside Docker  
- Deploying the backend with Render  
- Building a polished Streamlit UI  
- Watching everything come alive step by step  

This wasn’t “just a school assignment” —  
It genuinely felt like creating a real, production-ready product from scratch.  
I’m proud of both the technical result and the process that brought it to life.

---

## 👤 Author

**Pierrick Van Hoecke**  
AI & Data Science Student — BeCode Ghent  

🔗 GitHub: https://github.com/pierrickvhk  
🔗 LinkedIn: https://www.linkedin.com/in/pierrick-van-hoecke-60b305310  

---

## 📬 Contact

Feel free to reach out for improvements, questions, or collaboration opportunities.  
I’m passionate about ML engineering, backend development, and building real products.
