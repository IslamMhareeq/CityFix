from flask import Flask
from flask_pymongo import PyMongo
from auth.main import auth_bp
from main.main import main_bp
from main.user_roles import user_roles_bp
from reports.reports import reports_bp
from reports.done_reports import done_reports_bp
from config import Config
import urllib.parse
import os
import atexit
from dotenv import load_dotenv
import socket

# NEW imports for browser-auto-open
import webbrowser
from threading import Timer


def create_app():
    # تحميل المتغيرات من .env
    load_dotenv()
    
    app = Flask(__name__)
    
    # إعداد التهيئة من كلاس Config
    app.config.from_object(Config)
    
    # إعداد مفتاح السر للتطبيق
    app.secret_key = os.environ.get("SECRET_KEY", "your-secret-key-here")
    
    # إعداد اتصال MongoDB باستخدام اسم المستخدم وكلمة المرور من .env
    raw_username = os.getenv("raw_username")
    raw_password = os.getenv("raw_password")
    
    if not raw_username or not raw_password:
        raise ValueError("Environment variables raw_username and/or raw_password not set")

    username = urllib.parse.quote_plus(raw_username)
    password = urllib.parse.quote_plus(raw_password)

    app.config["MONGO_URI"] = (
        f"mongodb+srv://{username}:{password}@cluster0.05icn.mongodb.net/App"
        "?retryWrites=true&w=majority&appName=Cluster0"
    )
    
    # تهيئة الاتصال مع Mongo
    mongo = PyMongo(app)
    app.mongo = mongo

    # تسجيل الـ Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(reports_bp)
    app.register_blueprint(user_roles_bp)
    app.register_blueprint(done_reports_bp)
    app.register_blueprint(main_bp)
    
    return app


if __name__ == '__main__':
    app = create_app()
    
    # استخراج عنوان IP المحلي
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print("=" * 50)
    print("🌐 CityFix Server Starting...")
    print("=" * 50)
    print(f"📱 Access from your phone:")
    print(f"   http://{local_ip}:5000")
    print("=" * 50)
    print(f"💻 Local access:")
    print(f"   http://localhost:5000")
    print(f"   http://127.0.0.1:5000")
    print("=" * 50)
    print("📶 Make sure your phone is on the same WiFi network!")
    print("=" * 50)
    
    # تشغيل الخادم
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
