# 🎬 Movies Recommender System (ML + NLP)

## 📌 Overview

This project is an **end-to-end Movie Recommendation System** enhanced with **Sentiment Analysis** using Machine Learning and Natural Language Processing (NLP).

It recommends movies based on **content similarity** and also analyzes **user sentiment** from IMDb-style reviews using a trained ML model.

The project is designed to be **interview-ready**, **industry-aligned**, and **easy to run locally**.

---

## 🚀 Key Features

* 🎥 Content-based Movie Recommendation
* 🧠 TF-IDF Vectorization for similarity
* ❤️ Sentiment Analysis (Positive / Negative)
* 📦 Pre-trained ML models for fast execution
* 🧪 Jupyter notebooks for training & experiments
* 🖥️ Python-based backend (ready for API/UI extension)

---

## 🧠 Technologies Used

* **Python 3**
* **Pandas, NumPy** – data processing
* **Scikit-learn** – ML models
* **NLTK** – text preprocessing
* **TF-IDF Vectorizer** – feature extraction
* **Pickle (.pkl)** – model persistence
* **Jupyter Notebook** – experiments & training

---

## 📂 Project Structure

```
MRRreal/
│
├── app.py / main.py              # Application entry point
├── movies_metadata.csv           # Movie dataset
├── df.pkl                        # Preprocessed movie dataframe
├── tfidf.pkl                     # TF-IDF vectorizer
├── tfidf_matrix.pkl              # Movie similarity matrix
├── indices.pkl                   # Movie index mapping
├── sentiment_model.pkl           # Trained sentiment classifier
├── sentiment_vectorizer.pkl      # Sentiment vectorizer
├── movie_sentiment.pkl           # Cached sentiment results
├── requirements.txt              # Dependencies
├── train_sentiment_model.ipynb   # Model training notebook
├── TODO.md                       # Future improvements
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/naitiiik31/Movies_Recommender.git
cd Movies_Recommender
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the project

```bash
python main.py
```

✅ No retraining required – models are preloaded.

---

## 📊 How Recommendation Works

1. Movie metadata is vectorized using **TF-IDF**
2. **Cosine similarity** is calculated between movies
3. Given a movie title, top similar movies are returned

---

## ❤️ Sentiment Analysis Pipeline

1. Text cleaning (lowercase, stopwords, stemming)
2. TF-IDF vectorization
3. Classification using trained ML model
4. Output: **Positive / Negative sentiment**

---

## 🧪 Training Details

Training notebooks are included for transparency:

* Feature engineering
* Model comparison
* Accuracy evaluation
* Final model selection

> Models are saved as `.pkl` for reuse in production.

---

## 🎥 Project Demo Video
Watch the complete working demo here:
[https://your-video-link](https://github.com/naitiiik31/Movies_Recommender/releases/tag/v1.0)

---

🔮 Future Scope

🤝 Collaborative Filtering using user–item interactions

📊 Evaluation Metrics like Precision@K, Recall@K, NDCG

🌐 Deploy as REST API using FastAPI or Flask

🖥️ Frontend Integration using Streamlit or React

🧠 Deep Learning Models (Word2Vec, BERT embeddings)

☁️ Cloud Deployment (AWS / Azure / GCP)

📈 User Feedback Loop to improve recommendations over time

---

## 📌 Dataset

IMDb dataset is not included due to size limitations.

Download from:
[https://ai.stanford.edu/~amaas/data/sentiment/](https://ai.stanford.edu/~amaas/data/sentiment/)

---

## 👨‍💻 Author

**Naitikkumar Patel**

📎 GitHub: [https://github.com/naitiiik31](https://github.com/naitiiik31)

---

## ⭐ If you like this project

Give it a ⭐ on GitHub — it helps a lot!
