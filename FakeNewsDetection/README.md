📰 Fake News Detection

A machine learning project to classify news articles as real or fake using natural language processing (NLP) techniques.

📌 Features

Preprocessing of news text (tokenization, stopword removal, stemming/lemmatization).

Vectorization using TF-IDF / Bag of Words.

Training multiple ML models (Logistic Regression, Naive Bayes, SVM, etc.).

Evaluation with accuracy, precision, recall, and F1-score.

Simple script/notebook to predict if a given news text is fake or real.


🗂 Project Structure

FakeNewsDetection/
│── dataset/              # Training/testing dataset (CSV files)
│── notebook.ipynb        # Jupyter notebook with training + evaluation
│── requirements.txt      # Dependencies
│── app/                  # Flask/Django app (if applicable)
│── README.md             # Project documentation

⚙ Installation & Setup

1. Clone the repository:

git clone https://github.com/vishal7415/ML-Projects.git
cd ML-Projects/FakeNewsDetection


2. Create and activate a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows


3. Install dependencies:

pip install -r requirements.txt



▶ Usage

Run the Jupyter Notebook to train/test the models:

jupyter notebook notebook.ipynb

If a Flask/Django app is included:

python app.py

Then open http://127.0.0.1:5000/ in your browser.


📊 Results

Achieved XX% accuracy using Logistic Regression.

Other models tested: Naive Bayes, SVM, Random Forest.

Example confusion matrix and classification report are included in the notebook.


🔮 Future Improvements

Use deep learning models (LSTM, BERT).

Deploy as a web app.

Add live news scraping + real-time classification.


📜 License

This project is licensed under the MIT License – see the LICENSE file for details.
