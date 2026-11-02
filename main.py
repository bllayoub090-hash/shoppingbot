import asyncio
import httpx
from loguru import logger
from datetime import datetime

# إعداد ملف تسجيل الأخطاء والعمليات في الخلفية
logger.add("bot_actions.log", rotation="50 MB", retention="10 days", level="INFO")

class PlatformFetcher:
    def __init__(self, platform_name: str, country: str, target_url: str):
        self.platform_name = platform_name
        self.country = country
        self.target_url = target_url

    async def fetch(self, client: httpx.AsyncClient):
        """جلب البيانات بشكل غير متزامن لتوفير الوقت والموارد"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "ar-SA,ar;q=0.9,en;q=0.8"
        }
        
        try:
            logger.info(f"جاري فحص المنصة: {self.platform_name} في {self.country}...")
            
            # محاكاة لصفقة تم اصطيادها
            simulated_deal = {
                "platform": self.platform_name,
                "country": self.country,
                "deal_title": "خصم ترويجي استثنائي",
                "promo_code": f"GULF-{self.platform_name.upper()}-50",
                "detected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            return [simulated_deal]
            
        except httpx.RequestError as e:
            logger.error(f"خطأ شبكة في {self.platform_name} ({self.country}): {e}")
        except Exception as e:
            logger.error(f"خطأ غير متوقع في {self.platform_name}: {e}")
            
        return []

async def main_background_loop():
    logger.info("🚀 تم إقلاع نظام صيد العروض والصفقات في الخلفية بنجاح (24/7).")
    
    # قائمة المنصات المستهدفة عبر دول الخليج
    platforms = [
        # السعودية
        PlatformFetcher("HungerStation", "Saudi Arabia", "https://api.hungerstation.com/v1/offers"),
        PlatformFetcher("Jahez", "Saudi Arabia", "https://api.jahez.net/v1/deals"),
        PlatformFetcher("Mrsool", "Saudi Arabia", "https://api.mrsool.co/v1/promos"),
        PlatformFetcher("Ninja", "Saudi Arabia", "https://api.ninjadirect.sa/offers"),
        # الإمارات
        PlatformFetcher("Talabat", "UAE", "https://api.talabat.com/uae/deals"),
        PlatformFetcher("Careem", "UAE", "https://api.careem.com/food/offers"),
        # الكويت
        PlatformFetcher("Talabat", "Kuwait", "https://api.talabat.com/kuwait/deals"),
        # قطر
        PlatformFetcher("Snoonu", "Qatar", "https://api.snoonu.com/v1/offers"),
    ]

    # دورة العمل المستمرة في الخفاء
    while True:
        async with httpx.AsyncClient(http2=True) as client:
            tasks = [p.fetch(client) for p in platforms]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, list):
                    for deal in result:
                        logger.success(f"🟢 [تم رصد صفقة]: {deal['country']} | {deal['platform']} | الكود: {deal['promo_code']}")
        
        logger.info("⏳ انتهاء دورة الفحص الحالية. الانتقال لوضع السكون المؤقت...")
        await asyncio.sleep(600)

if __name__ == "__main__":
    try:
        asyncio.run(main_background_loop())
    except KeyboardInterrupt:
        logger.warning("⚠️ تم إيقاف البوت يدوياً.")
