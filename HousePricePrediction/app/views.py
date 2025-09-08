# app/views.py
import os
import numpy as np
from joblib import load, dump

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# --- ML model helpers (kept as before) ---
model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')

def ensure_model():
    if not os.path.exists(model_path):
        from sklearn.linear_model import LinearRegression
        X = np.array([
            [2, 800, 5],
            [3, 1200, 7],
            [4, 1600, 8],
            [1, 600, 4],
            [5, 2200, 9]
        ], dtype=float)
        y = np.array([40, 75, 120, 35, 200], dtype=float)
        reg = LinearRegression().fit(X, y)
        dump(reg, model_path)
    return load(model_path)

# --- Public home (landing/prediction link or info) ---
@login_required(login_url="login")
def home(request):
    # if you want to force login before showing prediction link, comment below redirect
    return render(request, "home.html")

# --- Protected dashboard and predict ---
@login_required(login_url="login")
def dashboard_view(request):
    # Show dashboard + last prediction if any
    return render(request, "dashboard.html")

@login_required(login_url="login")
def predict(request):
    result = ""
    if request.method == "POST":
        try:
            rooms = float(request.POST.get("rooms", 3))
            area = float(request.POST.get("area", 1200))
            loc = float(request.POST.get("loc", 7))
            model = ensure_model()
            pred = model.predict([[rooms, area, loc]])[0]
            result = f"₹ {pred:.2f} lakhs"
            messages.success(request, f"Prediction successful: {result}")
        except Exception as e:
            messages.error(request, f"Prediction error: {e}")
            return render(request, "dashboard.html", {"result": ""})
    return render(request, "dashboard.html", {"result": result})

def health(request):
    return JsonResponse({"status": "ok"})

# ---------- AUTH VIEWS ----------
def signup_view(request):
    next_url = request.POST.get("next") or request.GET.get("next") or ""
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        email = (request.POST.get("email") or "").strip()
        password1 = request.POST.get("password1") or ""
        password2 = request.POST.get("password2") or ""

        if not username or not password1 or not password2:
            messages.error(request, "Please fill all required fields.")
            return render(request, "signup.html", {"next": next_url})

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "signup.html", {"next": next_url})

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Choose another.")
            return render(request, "signup.html", {"next": next_url})

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        auth_login(request, user)
        messages.success(request, "Account created — you are now logged in.")
        return redirect(next_url or "dashboard")

    return render(request, "signup.html", {"next": next_url})

def login_view(request):
    # support ?next=/some/page/
    next_url = request.POST.get("next") or request.GET.get("next") or ""
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""

        if not username or not password:
            messages.error(request, "Please enter username and password.")
            return render(request, "login.html", {"next": next_url})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect(next_url or "dashboard")
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "login.html", {"next": next_url})

    return render(request, "login.html", {"next": next_url})

def logout_view(request):
    auth_logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")
