from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests
import time
import os
from collections import defaultdict

app = Flask(__name__)

# 🛡️ DDoS KORUMA - RATE LIMITING
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["500 per day", "100 per hour", "20 per minute"],
    storage_uri="memory://",
)

# 🚨 IP BAZLI KORUMA
REQUEST_TRACKER = defaultdict(list)
BLOCKED_IPS = set()

def check_ddos_protection(ip):
    """DDoS koruma kontrolü"""
    now = time.time()
    
    # 1 dakika içinde 30'dan fazla istek?
    recent_requests = [req_time for req_time in REQUEST_TRACKER[ip] if now - req_time < 60]
    if len(recent_requests) > 30:
        BLOCKED_IPS.add(ip)
        return False
    
    # 1 saniyede 5'ten fazla istek?
    second_requests = [req_time for req_time in recent_requests if now - req_time < 1]
    if len(second_requests) > 5:
        BLOCKED_IPS.add(ip)
        return False
    
    REQUEST_TRACKER[ip] = recent_requests[-50:]  # Son 50 isteği tut
    return True

@app.before_request
def before_each_request():
    """Her istekten önce DDoS kontrolü"""
    client_ip = get_remote_address()
    
    if client_ip in BLOCKED_IPS:
        return jsonify({
            "error": "Blocked - Too many requests",
            "message": "IP adresiniz geçici olarak bloke edildi",
            "telegram": "https://t.me/watronschecker"
        }), 429
    
    if not check_ddos_protection(client_ip):
        return jsonify({
            "error": "Rate limit exceeded", 
            "message": "Çok fazla istek gönderdiniz",
            "telegram": "https://t.me/watronschecker"
        }), 429
    
    REQUEST_TRACKER[client_ip].append(time.time())

# WATRONS BRANDING
WATRONS_TELEGRAM = "https://t.me/watronschecker"
WATRONS_CREATOR = "@tanrigibi"
APP_NAME = "Watrons Checker"

# TÜM API'LER
TARGET_APIS = {
    # ANA NABI API'LERİ
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
    
    # YAPAY ZEKA API'LERİ
    "gpt4mini": "https://kvz-nab.yapayzeka-api.gt.tc/gpt4mini",
    "gemini1.5pro": "https://kvz-nab.yapayzeka-api.gt.tc/gemini1.5pro",
    "gpt5model": "https://kvz-nab.yapayzeka-api.gt.tc/gpt5model",
    "deepseek": "https://kvz-nab.yapayzeka-api.gt.tc/deepseek",
    
    # COMMAND API'LERİ
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

@app.route('/')
@limiter.limit("10 per minute")
def home():
    return jsonify({
        "message": "Watrons Checker API",
        "creator": WATRONS_CREATOR,
        "telegram": WATRONS_TELEGRAM,
        "total_apis": len(TARGET_APIS),
        "status": "active",
        "ddos_protection": "enabled",
        "rate_limits": "500/day, 100/hour, 20/minute"
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "app": APP_NAME,
        "timestamp": time.time(),
        "blocked_ips": len(BLOCKED_IPS),
        "active_ips": len(REQUEST_TRACKER)
    })

@app.route('/api/<service_name>', methods=['GET', 'POST'])
@limiter.limit("30 per minute")
def api_proxy(service_name):
    if service_name not in TARGET_APIS:
        return jsonify({
            "error": "API not found", 
            "available_apis": list(TARGET_APIS.keys())[:10],
            "telegram": WATRONS_TELEGRAM
        }), 404
    
    target_url = TARGET_APIS[service_name]
    
    try:
        if request.method == 'GET':
            params = request.args.to_dict()
            response = requests.get(target_url, params=params, timeout=10)
        else:
            data = request.get_json() if request.is_json else request.form.to_dict()
            response = requests.post(target_url, data=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            # Nabi bilgilerini temizle ve Watrons ekle
            if isinstance(result, dict):
                if 'creator' in result:
                    result['creator'] = WATRONS_CREATOR
                if 'telegram' in result:
                    result['telegram'] = WATRONS_TELEGRAM
                else:
                    result['telegram'] = WATRONS_TELEGRAM
            return jsonify(result)
        else:
            return jsonify({
                "error": f"API error: {response.status_code}",
                "telegram": WATRONS_TELEGRAM
            }), response.status_code
            
    except requests.exceptions.Timeout:
        return jsonify({
            "error": "API timeout",
            "telegram": WATRONS_TELEGRAM
        }), 504
    except Exception as e:
        return jsonify({
            "error": f"Internal error: {str(e)}",
            "telegram": WATRONS_TELEGRAM
        }), 500

# 🧹 Temizleme thread'i
import threading
def cleanup_old_ips():
    """Eski IP kayıtlarını temizle"""
    while True:
        time.sleep(300)  # 5 dakikada bir
        now = time.time()
        for ip in list(REQUEST_TRACKER.keys()):
            REQUEST_TRACKER[ip] = [t for t in REQUEST_TRACKER[ip] if now - t < 3600]
            if not REQUEST_TRACKER[ip]:
                del REQUEST_TRACKER[ip]

# Thread'i başlat
cleanup_thread = threading.Thread(target=cleanup_old_ips, daemon=True)
cleanup_thread.start()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
