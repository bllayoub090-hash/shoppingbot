
from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# إعدادات معرّفات الشراكة (Store IDs) للأسواق المختلفة
# يمكنك تعديلها لاحقاً أو سحبها من Environment Variables في Render
AMAZON_STORES = {
    "sa": os.environ.get("AMAZON_SA_ID", "shoppingbot-sa-21"),
    "ae": os.environ.get("AMAZON_AE_ID", "shoppingbot-ae-21"),
    "eg": os.environ.get("AMAZON_EG_ID", "shoppingbot-eg-21"),
    "com": os.environ.get("AMAZON_US_ID", "shoppingbot-us-20"),
}


@app.route("/")
def home():
  return jsonify({
      "status": "online",
      "message": "Shopping Bot API is active and running 24/7!",
      "supported_regions": list(AMAZON_STORES.keys()),
  })


@app.route("/search", methods=["POST"])
def search_products():
  data = request.json or {}
  query = data.get("query", "")
  region = data.get("region", "sa").lower()

  if not query:
    return (
        jsonify({
            "error": "Please provide a product query (e.g., 'laptop', 'phone')"
        }),
        400,
    )

  # التأكد من دعم الدولة المطلوبة، وإلا فالافتراضية هي السعودية
  store_id = AMAZON_STORES.get(region, AMAZON_STORES["sa"])

  # محاكاة توليد الروابط الذكية وعمولات الأفلييت (يمكن ربطها بـ API الرسمي لاحقاً)
  affiliate_links = {
      "sa": f"https://www.amazon.sa/s?k={query}&tag={AMAZON_STORES['sa']}",
      "ae": f"https://www.amazon.ae/s?k={query}&tag={AMAZON_STORES['ae']}",
      "eg": f"https://www.amazon.eg/s?k={query}&tag={AMAZON_STORES['eg']}",
      "com": f"https://www.amazon.com/s?k={query}&tag={AMAZON_STORES['com']}",
  }

  return jsonify({
      "query": query,
      "selected_region": region,
      "active_store_id": store_id,
      "generated_affiliate_links": affiliate_links,
      "status": "success",
  })


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
