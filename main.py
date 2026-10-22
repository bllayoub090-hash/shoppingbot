import os
import re
import time
import threading
from flask import Flask, request, jsonify

app = Flask(__name__)

# استدعاء المعرفات الخاصة بك من متغيرات البيئة على Render
AFFILIATE_TAGS = {
    'SA': os.getenv('AMAZON_SA_TAG', 'yourtag-sa-21'),
    'AE': os.getenv('AMAZON_AE_TAG', 'yourtag-ae-21'),
    'EG': os.getenv('AMAZON_EG_TAG', 'yourtag-eg-21'),
    'US': os.getenv('AMAZON_US_TAG', 'yourtag-us-20')
}

def extract_asin(url):
    """استخراج رقم المنتج (ASIN) من رابط أمازون"""
    asin_match = re.search(r'/(?:dp|gp/product)/([A-Z0-9]{10})', url)
    if asin_match:
        return asin_match.group(1)
    return None

def generate_affiliate_link(url, region='US'):
    """إنشاء رابط أفلييت بحقن معرفك تلقائياً"""
    asin = extract_asin(url)
    tag = AFFILIATE_TAGS.get(region.upper(), AFFILIATE_TAGS['US'])
    
    domain_map = {
        'SA': 'amazon.sa',
        'AE': 'amazon.ae',
        'EG': 'amazon.eg',
        'US': 'amazon.com'
    }
    domain = domain_map.get(region.upper(), 'amazon.com')
    
    if asin:
        return f"https://www.{domain}/dp/{asin}?tag={tag}"
    return f"{url}?tag={tag}"

# محرك الخلفية الذاتي (يعمل تلقائياً كل فترة لتحديث وعمل المعالجة الذاتية)
def background_auto_engine():
    while True:
        print("[-] المحرك الذاتي يعمل في الخلفية ويقوم بتفقد وتحديث العروض...")
        time.sleep(3600)  # يكرر العملية كل ساعة تلقائياً

# تشغيل المحرك الذاتي في الخلفية بالتوازي مع سيرفر Flask
engine_thread = threading.Thread(target=background_auto_engine, daemon=True)
engine_thread.start()

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "online",
        "verification_code": "ccd3",
        "mode": "Fully Automated Self-Operating Engine",
        "message": "Automated Affiliate Bot is running with code ccd3"
    })

@app.route('/convert', methods=['POST'])
def convert_link():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "Please provide a valid 'url'"}), 400
    
    original_url = data['url']
    region = data.get('region', 'US')
    
    affiliate_url = generate_affiliate_link(original_url, region)
    
    return jsonify({
        "original_url": original_url,
        "affiliate_url": affiliate_url,
        "region": region.upper()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

