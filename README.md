# Fatrix-Chat-Assistant
A full-stack AI-powered assistant web application built with Flask, featuring a machine learning NLP engine for intent classification, sentiment analysis, and secure user authentication.

# Fatrix.chat 🤖

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Flask-Framework-green.svg" alt="Flask">
  <img src="https://img.shields.io/badge/ML-Scikit--learn-orange.svg" alt="ML">
</p>

Fatrix.chat is a full-stack AI-powered assistant web application. It leverages advanced Natural Language Processing (NLP) techniques and a secure backend architecture to deliver a seamless, context-aware conversational experience[cite: 2, 3, 6].

---

## 🏗 Project Architecture

### 1. Machine Learning & NLP Engine (`AFA_chat.py`)
The core intelligence of the application:
- **Preprocessing:** Uses **NLTK** for tokenization, lemmatization, and noise reduction[cite: 2].
- **Classification:** Implements **TF-IDF Vectorization** (unigrams & bigrams) coupled with a **Logistic Regression** model for high-accuracy intent prediction[cite: 2, 6].
- **Sentiment Analysis:** Integrates **TextBlob** to adapt responses based on user sentiment[cite: 2].
- **Robustness:** Features a **Jaccard similarity** fallback mechanism for handling ambiguous inputs[cite: 2].

### 2. Backend & Security (`app.py`)
A secure and scalable server implementation:
- **Framework:** Developed with **Flask** for efficient routing and API management[cite: 3].
- **Database:** Uses **Flask-SQLAlchemy** with **SQLite** for robust data persistence[cite: 3].
- **Authentication:** Features end-to-end user management with secure password hashing via `werkzeug.security`[cite: 3].

---

## 🛠 Technical Stack
| Category | Technology |
| :--- | :--- |
| **Backend** | Python, Flask, Flask-SQLAlchemy |
| **ML/NLP** | NLTK, Scikit-learn, TextBlob |
| **Database** | SQLite |
| **Frontend** | HTML5, CSS3, JavaScript |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- pip

### Installation
1. **Clone the repo**
   ```bash
   git clone [https://github.com/yourusername/Fatrix-Chat-Assistant.git](https://github.com/yourusername/Fatrix-Chat-Assistant.git)
