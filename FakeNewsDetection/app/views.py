from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from joblib import dump, load
import os, numpy as np

# Paths for model
model_dir = os.path.dirname(__file__)
clf_path = os.path.join(model_dir, 'clf.pkl')

# Train small fake-news model if missing
def ensure_model():
    if not os.path.exists(clf_path):
        texts = [
            "NASA confirms water found on Mars",
            "Cure for cancer discovered by local man in garage",
            "Government launches new tax reform policy",
            "Aliens land in my backyard yesterday night",
            "Study shows coffee improves productivity",
            "Click here to win a free iPhone now",
        ]
        labels = [0,1,0,1,0,1]  # 1=fake, 0=real
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import Pipeline
        pipe = Pipeline([
            ('tfidf', TfidfVectorizer(stop_words='english', max_features=5000)),
            ('lr', LogisticRegression(max_iter=500))
        ])
        pipe.fit(texts, labels)
        dump(pipe, clf_path)
    return load(clf_path)

# Signup view
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('dashboard')
    return render(request, 'signup.html')

# Dashboard view - login required
@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'result': ''})

# Prediction - login required
@login_required
def predict(request):
    if request.method == 'POST':
        try:
            text = request.POST.get('text', '')
            pipe = ensure_model()
            pred = pipe.predict([text])[0]
            proba = pipe.predict_proba([text])[0][int(pred)]
            label = 'FAKE' if int(pred)==1 else 'REAL'
            return render(request, 'dashboard.html', {'result': f'{label} (confidence {proba:.2f})'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return redirect('dashboard')

# Health check
def health(request):
    return JsonResponse({'status': 'ok'})
