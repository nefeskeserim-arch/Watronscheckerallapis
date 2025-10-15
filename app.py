from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests
import time
import os
from functools import lru_cache
import json
from collections import defaultdict
import threading

app = Flask(__name__)
CORS(app)

# 🚀 RENDER.COM OPTIMIZE RATE LIMITER
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["2000 per day", "300 per hour", "50 per minute", "3 per second"],
    storage_uri="memory://"
)

# 📊 RENDER FRIENDLY DDoS KORUMA
REQUEST_LOG = defaultdict(list)
SUSPICIOUS_IPS = set()

# WATRONS BRANDING
WATRONS_TELEGRAM = "t.me/watronschecker"
WATRONS_CREATOR = "@tanrigibi"
APP_NAME = "Watrons Checker"

def check_ddos_protection(ip):
    """Basit ama etkili DDoS koruması"""
    now = time.time()
    
    # 1 saniyede 10'dan fazla istek?
    recent_requests = [req_time for req_time in REQUEST_LOG[ip] if now - req_time < 1]
    if len(recent_requests) > 10:
        SUSPICIOUS_IPS.add(ip)
        return False
    
    # 1 dakikada 100'den fazla istek?
    minute_requests = [req_time for req_time in REQUEST_LOG[ip] if now - req_time < 60]
    if len(minute_requests) > 100:
        SUSPICIOUS_IPS.add(ip)
        return False
    
    REQUEST_LOG[ip] = recent_requests[-100:]
    return True

@app.before_request
def before_request():
    """Her istekten önce DDoS kontrolü"""
    client_ip = get_remote_address()
    
    if not check_ddos_protection(client_ip):
        return jsonify({
            "error": "Rate limit exceeded", 
            "message": "Too many requests",
            "telegram": WATRONS_TELEGRAM,
            "creator": WATRONS_CREATOR
        }), 429
    
    REQUEST_LOG[client_ip].append(time.time())

# TÜM API'LER (Aynı liste)
TARGET_APIS = {
    "secmen": "http://api.nabi.gt.tc/secmen",
    "ogretmen": "http://api.nabi.gt.tc/ogretmen",
    "yabanci": "http://api.nabi.gt.tc/yabanci",
    "log": "http://api.nabi.gt.tc/log",
    "vesika2": "http://api.nabi.gt.tc/vesika2",
    "tapu2": "http://api.nabi.gt.tc/tapu2",
    "iskaydi": "http://api.nabi.gt.tc/iskaydi",
    "sertifika2": "http://api.nabi.gt.tc/sertifika2",
    "papara": "http://api.nabi.gt.tc/papara",
    "ininal": "http://api.nabi.gt.tc/ininal",
    "turknet": "http://api.nabi.gt.tc/turknet",
    "serino": "http://api.nabi.gt.tc/serino",
    "firma": "http://api.nabi.gt.tc/firma",
    "craftrise": "http://api.nabi.gt.tc/craftrise",
    "sgk2": "http://api.nabi.gt.tc/sgk2",
    "plaka2": "http://api.nabi.gt.tc/plaka2",
    "plakaismi": "http://api.nabi.gt.tc/plakaismi",
    "plakaborc": "http://api.nabi.gt.tc/plakaborc",
    "akp": "http://api.nabi.gt.tc/akp",
    "aifoto": "http://api.nabi.gt.tc/aifoto",
    "insta": "http://api.nabi.gt.tc/insta",
    "facebook_hanedan": "http://api.nabi.gt.tc/facebook_hanedan",
    "uni": "http://api.nabi.gt.tc/uni",
    "lgs_hanedan": "http://api.nabi.gt.tc/lgs_hanedan",
    "okulno_hanedan": "http://api.nabi.gt.tc/okulno_hanedan",
    "tc_sorgulama": "http://api.nabi.gt.tc/tc_sorgulama",
    "tc_pro_sorgulama": "http://api.nabi.gt.tc/tc_pro_sorgulama",
    "hayat_hikayesi": "http://api.nabi.gt.tc/hayat_hikayesi",
    "ad_soyad": "http://api.nabi.gt.tc/ad_soyad",
    "ad_soyad_pro": "http://api.nabi.gt.tc/ad_soyad_pro",
    "is_yeri": "http://api.nabi.gt.tc/is_yeri",
    "vergi_no": "http://api.nabi.gt.tc/vergi_no",
    "yas": "http://api.nabi.gt.tc/yas",
    "tc_gsm": "http://api.nabi.gt.tc/tc_gsm",
    "gsm_tc": "http://api.nabi.gt.tc/gsm_tc",
    "adres": "http://api.nabi.gt.tc/adres",
    "hane": "http://api.nabi.gt.tc/hane",
    "apartman": "http://api.nabi.gt.tc/apartman",
    "ada_parsel": "http://api.nabi.gt.tc/ada_parsel",
    "adi_il_ilce": "http://api.nabi.gt.tc/adi_il_ilce",
    "aile": "http://api.nabi.gt.tc/aile",
    "aile_pro": "http://api.nabi.gt.tc/aile_pro",
    "es": "http://api.nabi.gt.tc/es",
    "sulale": "http://api.nabi.gt.tc/sulale",
    "lgs": "http://api.nabi.gt.tc/lgs",
    "e_kurs": "http://api.nabi.gt.tc/e_kurs",
    "ip": "http://api.nabi.gt.tc/ip",
    "dns": "http://api.nabi.gt.tc/dns",
    "whois": "http://api.nabi.gt.tc/whois",
    "subdomain": "http://api.nabi.gt.tc/subdomain",
    "leak": "http://api.nabi.gt.tc/leak",
    "telegram": "http://api.nabi.gt.tc/telegram",
    "sifre_encrypt": "http://api.nabi.gt.tc/sifre_encrypt",
    "gpt4mini": "https://kvz-nab.yapayzeka-api.gt.tc/gpt4mini",
    "gemini1.5pro": "https://kvz-nab.yapayzeka-api.gt.tc/gemini1.5pro",
    "gpt5model": "https://kvz-nab.yapayzeka-api.gt.tc/gpt5model",
    "deepseek": "https://kvz-nab.yapayzeka-api.gt.tc/deepseek",
    "hava": "https://nabi-yeni-api.onrender.com/command/hava",
    "kur": "https://nabi-yeni-api.onrender.com/command/kur",
    "steam_kod": "https://nabi-yeni-api.onrender.com/command/steam_kod",
    "vp_kod": "https://nabi-yeni-api.onrender.com/command/vp_kod",
    "free": "https://nabi-yeni-api.onrender.com/command/free",
    "kalp": "https://nabi-yeni-api.onrender.com/command/kalp",
    "sigma": "https://nabi-yeni-api.onrender.com/command/sigma",
    "live": "https://nabi-yeni-api.onrender.com/command/live",
    "imposter": "https://nabi-yeni-api.onrender.com/command/imposter",
    "play_kod": "https://nabi-yeni-api.onrender.com/command/play_kod",
    "uc_kod": "https://nabi-yeni-api.onrender.com/command/uc_kod",
    "midasbuy": "https://nabi-yeni-api.onrender.com/command/midasbuy",
    "predunyam": "https://nabi-yeni-api.onrender.com/command/predunyam",
    "smsonay": "https://nabi-yeni-api.onrender.com/command/smsonay",
    "zara": "https://nabi-yeni-api.onrender.com/command/zara",
    "exxen": "https://nabi-yeni-api.onrender.com/command/exxen",
    "blutv": "https://nabi-yeni-api.onrender.com/command/blutv",
    "amazon": "https://nabi-yeni-api.onrender.com/command/amazon",
    "purna": "https://nabi-yeni-api.onrender.com/command/purna",
    "mlbb_kod": "https://nabi-yeni-api.onrender.com/command/mlbb_kod",
    "kazandiriyo": "https://nabi-yeni-api.onrender.com/command/kazandiriyo",
    "robux_kod": "https://nabi-yeni-api.onrender.com/command/robux_kod",
    "carparking": "https://nabi-yeni-api.onrender.com/command/carparking",
    "roblox": "https://nabi-yeni-api.onrender.com/command/roblox",
    "twitter": "https://nabi-yeni-api.onrender.com/command/twitter",
    "netflix": "https://nabi-yeni-api.onrender.com/command/netflix",
    "pubg": "https://nabi-yeni-api.onrender.com/command/pubg",
    "hepsiburada": "https://nabi-yeni-api.onrender.com/command/hepsiburada",
    "hotmail": "https://nabi-yeni-api.onrender.com/command/hotmail",
    "valorant": "https://nabi-yeni-api.onrender.com/command/valorant",
    "facebook": "https://nabi-yeni-api.onrender.com/command/facebook",
    "troy": "https://nabi-yeni-api.onrender.com/command/troy",
    "iyzico": "https://he.nabinin-sikis-cc-api.gt.tc/iyzico"
}

class APIProxy:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Watrons-Proxy/1.0',
            'Accept': 'application/json'
        })
    
    def clean_response(self, data):
        """TÜM Nabi bilgilerini temizle ve Watrons branding ekle"""
        if isinstance(data, dict):
            cleaned = {}
            for key, value in data.items():
                # NABI BİLGİLERİNİ TAMAMEN TEMİZLE
                if key.lower() in ["creator", "telegram", "channel", "admin", "owner"]:
                    if any(nabi_word in str(value).lower() for nabi_word in ["nabi", "sukazatkinis", "@sukazatkinis", "nabisystem"]):
                        continue
                
                # RESPONSE İÇİNDEKİ RESPONSE'U ÇIKAR
                if key == "response" and isinstance(value, dict):
                    cleaned.update(self.clean_response(value))
                else:
                    cleaned[key] = self.clean_response(value)
            
            # WATRONS BRANDING EKLE (sadece ana response'ta)
            if not any(key in cleaned for key in ["telegram", "channel"]):
                cleaned["telegram"] = WATRONS_TELEGRAM
                cleaned["creator"] = WATRONS_CREATOR
            
            return cleaned
        elif isinstance(data, list):
            return [self.clean_response(item) for item in data]
        else:
            return data
    
    def add_watrons_branding(self, response_data):
        """Watrons branding ekle"""
        if isinstance(response_data, dict):
            response_data["telegram"] = WATRONS_TELEGRAM
            response_data["creator"] = WATRONS_CREATOR
            response_data["app"] = APP_NAME
        return response_data
    
    def forward_request(self, target_url, params, method="GET"):
        try:
            timeout = (10, 30)
            
            if method == "GET":
                response = self.session.get(target_url, params=params, timeout=timeout)
            else:
                response = self.session.post(target_url, data=params, timeout=timeout)
            
            if response.status_code == 200:
                data = response.json()
                cleaned_data = self.clean_response(data)
                branded_data = self.add_watrons_branding(cleaned_data)
                return branded_data, 200
            else:
                # HATA DURUMUNDA DA WATRONS BRANDING
                error_data = {
                    "error": f"API hatası: {response.status_code}",
                    "message": "Servis geçici olarak kullanılamıyor",
                    "telegram": WATRONS_TELEGRAM,
                    "creator": WATRONS_CREATOR
                }
                return error_data, response.status_code
                
        except requests.exceptions.Timeout:
            return {
                "error": "API timeout - servis yanıt vermiyor",
                "telegram": WATRONS_TELEGRAM,
                "creator": WATRONS_CREATOR
            }, 504
        except requests.exceptions.ConnectionError:
            return {
                "error": "Bağlantı hatası - API'ye ulaşılamıyor", 
                "telegram": WATRONS_TELEGRAM,
                "creator": WATRONS_CREATOR
            }, 503
        except Exception as e:
            return {
                "error": f"Beklenmeyen hata: {str(e)}",
                "telegram": WATRONS_TELEGRAM, 
                "creator": WATRONS_CREATOR
            }, 500

proxy = APIProxy()

# 🏠 ANA SAYFA
@app.route("/")
@limiter.limit("10 per minute")
def home():
    return jsonify({
        "message": "Watrons Checker API",
        "creator": WATRONS_CREATOR,
        "telegram": WATRONS_TELEGRAM,
        "services": list(TARGET_APIS.keys()),
        "total_services": len(TARGET_APIS),
        "status": "active",
        "ddos_protection": "enabled"
    })

# 📊 HEALTH CHECK
@app.route("/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "app": APP_NAME,
        "telegram": WATRONS_TELEGRAM,
        "creator": WATRONS_CREATOR,
        "timestamp": time.time(),
        "active_ips": len(REQUEST_LOG),
        "suspicious_ips": len(SUSPICIOUS_IPS)
    })

# 🔄 DYNAMIC API PROXY
@app.route("/api/<path:service_name>", methods=["GET", "POST"])
@limiter.limit("30 per minute")
def api_proxy(service_name):
    client_ip = get_remote_address()
    REQUEST_LOG[client_ip].append(time.time())
    
    if service_name not in TARGET_APIS:
        return jsonify({
            "error": "Service not found",
            "available_services": list(TARGET_APIS.keys())[:10],
            "telegram": WATRONS_TELEGRAM,
            "creator": WATRONS_CREATOR
        }), 404
    
    target_url = TARGET_APIS[service_name]
    
    if request.method == "GET":
        params = request.args.to_dict()
    else:
        params = request.get_json() if request.is_json else request.form.to_dict()
    
    result, status_code = proxy.forward_request(
        target_url, 
        params, 
        request.method
    )
    
    return jsonify(result), status_code

# 🧹 PERIODIC CLEANUP
def cleanup_old_requests():
    while True:
        time.sleep(300)
        now = time.time()
        for ip in list(REQUEST_LOG.keys()):
            REQUEST_LOG[ip] = [t for t in REQUEST_LOG[ip] if now - t < 3600]
            if not REQUEST_LOG[ip]:
                del REQUEST_LOG[ip]

if __name__ == "__main__":
    cleanup_thread = threading.Thread(target=cleanup_old_requests, daemon=True)
    cleanup_thread.start()
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
