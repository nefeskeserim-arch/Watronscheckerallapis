from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests
import time
import os
from collections import defaultdict
import logging

app = Flask(__name__)

# DDoS koruma
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["500 per day", "100 per hour", "20 per minute"],
    storage_uri="memory://",
)

REQUEST_TRACKER = defaultdict(list)
BLOCKED_IPS = set()
REQUEST_COUNTER = 0

def check_ddos_protection(ip):
    now = time.time()
    recent = [t for t in REQUEST_TRACKER[ip] if now - t < 60]
    if len(recent) > 30:
        BLOCKED_IPS.add(ip)
        return False
    sec_req = [t for t in recent if now - t < 1]
    if len(sec_req) > 5:
        BLOCKED_IPS.add(ip)
        return False
    REQUEST_TRACKER[ip] = recent[-50:]
    return True

@app.before_request
def before_each_request():
    global REQUEST_COUNTER
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
    REQUEST_COUNTER += 1

    if REQUEST_COUNTER % 1000 == 0:
        keys = list(REQUEST_TRACKER.keys())
        for ip in keys:
            if len(REQUEST_TRACKER[ip]) > 50:
                REQUEST_TRACKER[ip] = REQUEST_TRACKER[ip][-20:]
        if len(keys) > 2000:
            for ip in keys[:1000]:
                del REQUEST_TRACKER[ip]

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

WATRONS_TELEGRAM = "https://t.me/watronschecker"
WATRONS_CREATOR = "@tanrigibi"

def get_base_url():
    return request.host_url.rstrip('/')

# --- Tüm API’ler (senin verdiğin liste) ---
TARGET_APIS = {
    "secmen": {"url": "http://api.nabi.gt.tc/secmen", "params": ["tc"]},
    "ogretmen": {"url": "http://api.nabi.gt.tc/ogretmen", "params": ["tc"]},
    "yabanci": {"url": "http://api.nabi.gt.tc/yabanci", "params": ["tc"]},
    "log": {"url": "http://api.nabi.gt.tc/log", "params": ["site", "message", "level"]},
    "vesika2": {"url": "http://api.nabi.gt.tc/vesika2", "params": ["tc"]},
    "tapu2": {"url": "http://api.nabi.gt.tc/tapu2", "params": ["tc"]},
    "iskaydi": {"url": "http://api.nabi.gt.tc/iskaydi", "params": ["tc"]},
    "sertifika2": {"url": "http://api.nabi.gt.tc/sertifika2", "params": ["tc"]},
    "papara": {"url": "http://api.nabi.gt.tc/papara", "params": ["numara"]},
    "ininal": {"url": "http://api.nabi.gt.tc/ininal", "params": ["barkod"]},
    "turknet": {"url": "http://api.nabi.gt.tc/turknet", "params": ["numara"]},
    "serino": {"url": "http://api.nabi.gt.tc/serino", "params": ["seri"]},
    "firma": {"url": "http://api.nabi.gt.tc/firma", "params": ["vergi_no"]},
    "craftrise": {"url": "http://api.nabi.gt.tc/craftrise", "params": ["eposta"]},
    "sgk2": {"url": "http://api.nabi.gt.tc/sgk2", "params": ["tc"]},
    "plaka2": {"url": "http://api.nabi.gt.tc/plaka2", "params": ["plaka"]},
    "plakaismi": {"url": "http://api.nabi.gt.tc/plakaismi", "params": ["plaka"]},
    "plakaborc": {"url": "http://api.nabi.gt.tc/plakaborc", "params": ["plaka"]},
    "akp": {"url": "http://api.nabi.gt.tc/akp", "params": ["tc"]},
    "aifoto": {"url": "http://api.nabi.gt.tc/aifoto", "params": ["prompt"]},
    "insta": {"url": "http://api.nabi.gt.tc/insta", "params": ["kullaniciadi"]},
    "facebook_hanedan": {"url": "http://api.nabi.gt.tc/facebook_hanedan", "params": ["tc"]},
    "uni": {"url": "http://api.nabi.gt.tc/uni", "params": ["tc"]},
    "lgs_hanedan": {"url": "http://api.nabi.gt.tc/lgs_hanedan", "params": ["tc"]},
    "okulno_hanedan": {"url": "http://api.nabi.gt.tc/okulno_hanedan", "params": ["tc"]},
    "tc_sorgulama": {"url": "http://api.nabi.gt.tc/tc_sorgulama", "params": ["tc"]},
    "tc_pro_sorgulama": {"url": "http://api.nabi.gt.tc/tc_pro_sorgulama", "params": ["tc"]},
    "hayat_hikayesi": {"url": "http://api.nabi.gt.tc/hayat_hikayesi", "params": ["tc"]},
    "ad_soyad": {"url": "http://api.nabi.gt.tc/ad_soyad", "params": ["ad", "soyad"]},
    "ad_soyad_pro": {"url": "http://api.nabi.gt.tc/ad_soyad_pro", "params": ["ad", "soyad"]},
    "is_yeri": {"url": "http://api.nabi.gt.tc/is_yeri", "params": ["tc"]},
    "vergi_no": {"url": "http://api.nabi.gt.tc/vergi_no", "params": ["vergi_no"]},
    "yas": {"url": "http://api.nabi.gt.tc/yas", "params": ["tc"]},
    "tc_gsm": {"url": "http://api.nabi.gt.tc/tc_gsm", "params": ["tc"]},
    "gsm_tc": {"url": "http://api.nabi.gt.tc/gsm_tc", "params": ["gsm"]},
    "adres": {"url": "http://api.nabi.gt.tc/adres", "params": ["tc"]},
    "hane": {"url": "http://api.nabi.gt.tc/hane", "params": ["tc"]},
    "apartman": {"url": "http://api.nabi.gt.tc/apartman", "params": ["tc"]},
    "ada_parsel": {"url": "http://api.nabi.gt.tc/ada_parsel", "params": ["tc"]},
    "adi_il_ilce": {"url": "http://api.nabi.gt.tc/adi_il_ilce", "params": ["il", "ilce"]},
    "aile": {"url": "http://api.nabi.gt.tc/aile", "params": ["tc"]},
    "aile_pro": {"url": "http://api.nabi.gt.tc/aile_pro", "params": ["tc"]},
    "es": {"url": "http://api.nabi.gt.tc/es", "params": ["tc"]},
    "sulale": {"url": "http://api.nabi.gt.tc/sulale", "params": ["tc"]},
    "lgs": {"url": "http://api.nabi.gt.tc/lgs", "params": ["tc"]},
    "e_kurs": {"url": "http://api.nabi.gt.tc/e_kurs", "params": ["tc"]},
    "ip": {"url": "http://api.nabi.gt.tc/ip", "params": ["ip"]},
    "dns": {"url": "http://api.nabi.gt.tc/dns", "params": ["domain"]},
    "whois": {"url": "http://api.nabi.gt.tc/whois", "params": ["domain"]},
    "subdomain": {"url": "http://api.nabi.gt.tc/subdomain", "params": ["domain"]},
    "leak": {"url": "http://api.nabi.gt.tc/leak", "params": ["eposta"]},
    "telegram": {"url": "http://api.nabi.gt.tc/telegram", "params": ["kullaniciadi"]},
    "sifre_encrypt": {"url": "http://api.nabi.gt.tc/sifre_encrypt", "params": ["sifre"]},
    "gpt4mini": {"url": "https://kvz-nab.yapayzeka-api.gt.tc/gpt4mini", "params": ["soru"]},
    "gemini1.5pro": {"url": "https://kvz-nab.yapayzeka-api.gt.tc/gemini1.5pro", "params": ["soru"]},
    "gpt5model": {"url": "https://kvz-nab.yapayzeka-api.gt.tc/gpt5model", "params": ["soru"]},
    "deepseek": {"url": "https://kvz-nab.yapayzeka-api.gt.tc/deepseek", "params": ["soru"]},
    "hava": {"url": "https://nabi-yeni-api.onrender.com/command/hava", "params": ["sehir"]},
    "kur": {"url": "https://nabi-yeni-api.onrender.com/command/kur", "params": []},
    "steam_kod": {"url": "https://nabi-yeni-api.onrender.com/command/steam_kod", "params": []},
    "vp_kod": {"url": "https://nabi-yeni-api.onrender.com/command/vp_kod", "params": []},
    "free": {"url": "https://nabi-yeni-api.onrender.com/command/free", "params": []},
    "kalp": {"url": "https://nabi-yeni-api.onrender.com/command/kalp", "params": []},
    "sigma": {"url": "https://nabi-yeni-api.onrender.com/command/sigma", "params": []},
    "live": {"url": "https://nabi-yeni-api.onrender.com/command/live", "params": []},
    "imposter": {"url": "https://nabi-yeni-api.onrender.com/command/imposter", "params": []},
    "play_kod": {"url": "https://nabi-yeni-api.onrender.com/command/play_kod", "params": []},
    "uc_kod": {"url": "https://nabi-yeni-api.onrender.com/command/uc_kod", "params": []},
    "midasbuy": {"url": "https://nabi-yeni-api.onrender.com/command/midasbuy", "params": []},
    "predunyam": {"url": "https://nabi-yeni-api.onrender.com/command/predunyam", "params": []},
    "smsonay": {"url": "https://nabi-yeni-api.onrender.com/command/smsonay", "params": ["gsm"]},
    "zara": {"url": "https://nabi-yeni-api.onrender.com/command/zara", "params": []},
    "exxen": {"url": "https://nabi-yeni-api.onrender.com/command/exxen", "params": []},
    "blutv": {"url": "https://nabi-yeni-api.onrender.com/command/blutv", "params": []},
    "amazon": {"url": "https://nabi-yeni-api.onrender.com/command/amazon", "params": []},
    "purna": {"url": "https://nabi-yeni-api.onrender.com/command/purna", "params": []},
    "mlbb_kod": {"url": "https://nabi-yeni-api.onrender.com/command/mlbb_kod", "params": []},
    "kazandiriyo": {"url": "https://nabi-yeni-api.onrender.com/command/kazandiriyo", "params": []},
    "robux_kod": {"url": "https://nabi-yeni-api.onrender.com/command/robux_kod", "params": []},
    "carparking": {"url": "https://nabi-yeni-api.onrender.com/command/carparking", "params": []},
    "roblox": {"url": "https://nabi-yeni-api.onrender.com/command/roblox", "params": []},
    "twitter": {"url": "https://nabi-yeni-api.onrender.com/command/twitter", "params": []},
    "netflix": {"url": "https://nabi-yeni-api.onrender.com/command/netflix", "params": []},
    "pubg": {"url": "https://nabi-yeni-api.onrender.com/command/pubg", "params": []},
    "hepsiburada": {"url": "https://nabi-yeni-api.onrender.com/command/hepsiburada", "params": []},
    "hotmail": {"url": "https://nabi-yeni-api.onrender.com/command/hotmail", "params": []},
    "valorant": {"url": "https://nabi-yeni-api.onrender.com/command/valorant", "params": []},
    "facebook": {"url": "https://nabi-yeni-api.onrender.com/command/facebook", "params": []},
    "troy": {"url": "https://nabi-yeni-api.onrender.com/command/troy", "params": []},
    "iyzico": {"url": "https://he.nabinin-sikis-cc-api.gt.tc/iyzico", "params": []},
}

@app.route('/')
@limiter.limit("10 per minute")
def home():
    base_url = get_base_url()
    api_list = {}
    for name, info in TARGET_APIS.items():
        example = f"{base_url}/api/{name}"
        if info["params"]:
            example += "?" + "&".join([f"{p}=deger" for p in info["params"]])
        api_list[name] = {
            "url": f"{base_url}/api/{name}",
            "target_api": info["url"],
            "parameters": info["params"],
            "example": example
        }
    return jsonify({
        "message": "Watrons Checker API",
        "creator": WATRONS_CREATOR,
        "telegram": WATRONS_TELEGRAM,
        "base_url": base_url,
        "total_apis": len(TARGET_APIS),
        "status": "active",
        "apis": api_list
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": time.time(),
        "base_url": get_base_url()
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
    api_info = TARGET_APIS[service_name]
    target_url = api_info["url"]
    expected_params = api_info["params"]
    try:
        if request.method == 'GET':
            params = request.args.to_dict()
        else:
            params = request.get_json() if request.is_json else request.form.to_dict()
        missing = [p for p in expected_params if p not in params or not params[p]]
        if missing:
            return jsonify({
                "error": "Missing parameters",
                "required_params": expected_params,
                "missing": missing,
                "example": f"{get_base_url()}/api/{service_name}?{'&'.join([f'{p}=deger' for p in expected_params])}",
                "telegram": WATRONS_TELEGRAM
            }), 400
        timeout = 60
        for attempt in range(3):
            try:
                if request.method == 'GET':
                    resp = requests.get(target_url, params=params, timeout=timeout)
                else:
                    resp = requests.post(target_url, data=params, timeout=timeout)
                if resp.status_code == 200:
                    result = resp.json()
                    result["telegram"] = WATRONS_TELEGRAM
                    result["creator"] = WATRONS_CREATOR
                    return jsonify(result)
                elif resp.status_code >= 500:
                    continue
                else:
                    return jsonify({
                        "error": f"API error: {resp.status_code}",
                        "telegram": WATRONS_TELEGRAM
                    }), resp.status_code
            except requests.exceptions.Timeout:
                if attempt < 2:
                    time.sleep(2)
                    continue
                return jsonify({
                    "error": "API timeout after 3 attempts",
                    "telegram": WATRONS_TELEGRAM
                }), 504
        return jsonify({
            "error": "All attempts failed",
            "telegram": WATRONS_TELEGRAM
        }), 500
    except Exception as e:
        return jsonify({
            "error": f"Internal error: {str(e)}",
            "telegram": WATRONS_TELEGRAM
        }), 500

@app.route('/api/<service_name>/help', methods=['GET'])
def api_help(service_name):
    if service_name not in TARGET_APIS:
        return jsonify({"error": "API not found", "telegram": WATRONS_TELEGRAM}), 404
    info = TARGET_APIS[service_name]
    base_url = get_base_url()
    return jsonify({
        "api": service_name,
        "your_endpoint": f"{base_url}/api/{service_name}",
        "target_api": info["url"],
        "required_parameters": info["params"],
        "example": f"{base_url}/api/{service_name}?{'&'.join([f'{p}=deger' for p in info['params']])}",
        "telegram": WATRONS_TELEGRAM
    })

if __name__ == '__main__':
    log = logging.getLogger('werkzeug')
    log.disabled = True
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
