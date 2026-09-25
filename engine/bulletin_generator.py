import json, os, logging, base64, pathlib, glob
from datetime import datetime
from html2image import Html2Image
from PIL import Image

# استيراد حاسبة الخطر وطبقة التحقق الجديدة من الطقس
from engine.risk_calculator import RiskCalculator
from weather_validator import WeatherAccuracyJudge

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class BulletinGenerator:
    def __init__(self):
        # استخدام قاضي الطقس الجديد بدلاً من weather_client القديم
        self.weather_judge = WeatherAccuracyJudge()
        self.risk_calculator = RiskCalculator()
        
        self.base_project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.output_dir = os.path.join(self.base_project_dir, "output")
        if not os.path.exists(self.output_dir): os.makedirs(self.output_dir)
        
        self.hti = Html2Image(
            output_path=self.output_dir,
            custom_flags=['--disable-web-security', '--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
        )
        self.cities_file = os.path.join(self.base_project_dir, "config", "cities.json")

    def load_cities(self):
        try:
            with open(self.cities_file, 'r', encoding='utf-8') as f: return json.load(f)
        except Exception as e:
            logger.error(f"Error loading cities: {e}")
            return {}

    def get_optimized_background_b64(self, directory):
        if not os.path.exists(directory): return ""
        for f in os.listdir(directory):
            if "background" in f.lower() and f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                orig_path = os.path.join(directory, f)
                try:
                    img = Image.open(orig_path).convert("RGB")
                    img = img.resize((1080, 1080), Image.Resampling.LANCZOS)
                    opt_path = os.path.join(self.output_dir, "temp_opt.jpg")
                    img.save(opt_path, "JPEG", quality=85)
                    with open(opt_path, "rb") as img_file:
                        b64_data = base64.b64encode(img_file.read()).decode('utf-8')
                    try: os.remove(opt_path)
                    except: pass
                    return f"data:image/jpeg;base64,{b64_data}"
                except:
                    pass
        return ""

    def get_font_uri(self, directory):
        if not os.path.exists(directory): return ""
        for f in os.listdir(directory):
            if "font" in f.lower() and f.lower().endswith(".ttf"): 
                return pathlib.Path(os.path.abspath(os.path.join(directory, f))).as_uri()
        return ""

    def get_weather_icon(self, code):
        if code in [0, 1]: return "☀️"
        elif code == 2: return "⛅"
        elif code == 3: return "☁️"
        elif code in [45, 48]: return "🌫️"
        elif 51 <= code <= 67: return "🌧️"
        elif 71 <= code <= 77: return "❄️"
        elif 80 <= code <= 82: return "🌦️"
        elif 95 <= code <= 99: return "⛈️"
        else: return "☀️"

    def get_uv_word(self, uv_index):
        if uv_index <= 2: return "منخفض"
        elif uv_index <= 5: return "متوسط"
        elif uv_index <= 7: return "عالي"
        elif uv_index <= 10: return "عالي جداً"
        else: return "شديد"

    def clean_unwanted_files(self):
        for ext in ["*.csv", "*.txt", "*.html"]:
            for file_path in glob.glob(os.path.join(self.output_dir, ext)):
                try: os.remove(file_path)
                except: pass

    def generate_all_bulletins(self):
        cities = self.load_cities()
        if not cities: return
        for key, city in cities.items():
            try:
                logger.info(f"🔄 جاري معالجة مدينة: {city.get('name_ar', key)}...")
                self._generate_city_infographic(city)
            except Exception as e:
                logger.error(f"❌ حدث خطأ في {key}: {e}")
        self.clean_unwanted_files()
        
        # استدعاء دالة إنشاء الموقع بعد توليد الصور
        self.generate_website(cities)
        
        logger.info("🧹 تم إنشاء الصور والموقع بنجاح!")

    def _generate_city_infographic(self, city_data):
        # 1. الحصول على الأيام الخمسة الموثقة والمقارنة مباشرة من القاضي
        daily_data = self.weather_judge.get_validated_forecast(city_data['latitude'], city_data['longitude'], city_data['timezone'])
        
        if not daily_data:
            logger.error(f"❌ لم يتم جلب البيانات لمدينة {city_data['name_ar']}")
            return
            
        base_dir = os.path.join(self.base_project_dir, "assets")
        bg_b64 = self.get_optimized_background_b64(base_dir)
        font_uri = self.get_font_uri(base_dir)

        days_ar = ["الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
        cards_html = ""
        
        for day in daily_data:
            # يتم الاعتماد الآن على القيم اليومية النقية لحساب المخاطر
            risk = self.risk_calculator.calculate_daily_risk(day)
            nose = risk['nose']
            breath = risk['breath']
            icon = self.get_weather_icon(day.weather_code)
            uv_desc = self.get_uv_word(day.uv_index)
            try: day_name = days_ar[datetime.strptime(day.date, "%Y-%m-%d").weekday()]
            except: day_name = "اليوم"
            
            pollen_val = getattr(day, 'pollen', 0)

            is_alert = day.dust > 80 or day.wind_speed > 40
            alert_class = "alert-card" if is_alert else ""
            day_class = "alert-day" if is_alert else ""
            alert_badge = '<div class="alert-badge">⚠️ إنذار طقس</div>' if is_alert else ''

            cards_html += f"""
            <div class="card {alert_class}">
                <div class="day-name {day_class}">{day_name}<br><span style="font-size:11pt;">{day.date}</span></div>
                {alert_badge}
                <div class="weather-icon">{icon}</div>
                <div class="temp-box">{day.max_temp}° <span style="font-size:16pt; color:#444;">/ {day.min_temp}°</span></div>
                
                <div class="details-list">
                    <div class="d-item">💧 الرطوبة: <span class="val">{day.humidity}%</span></div>
                    <div class="d-item">💨 الرياح: <span class="val">{day.wind_speed} كم/س</span></div>
                    <div class="d-item">🌫️ الغبار: <span class="val">{day.dust} µg</span></div>
                    <div class="d-item">🌿 اللقاح: <span class="val">{pollen_val}</span></div>
                    <div class="d-item">☀️ الـ UV: <span class="val">{day.uv_index} ({uv_desc})</span></div>
                </div>
                
                <div class="med-indicators">
                    <div class="m-box" style="background: {nose['bg']}; border-color: {nose['border']};">
                        <div class="m-title">{nose['title']}</div>
                        <div class="m-val">{nose['emoji']} {nose['level']}</div>
                    </div>
                    <div class="m-box" style="background: {breath['bg']}; border-color: {breath['border']};">
                        <div class="m-title">{breath['title']}</div>
                        <div class="m-val">{breath['emoji']} {breath['level']}</div>
                    </div>
                </div>
            </div>
            """

        html_content = f"""
        <!DOCTYPE html>
        <html dir="rtl" lang="ar">
        <head>
        <meta charset="UTF-8">
        <style>
            @font-face {{ font-family: 'CustomCairo'; src: url('{font_uri}') format('truetype'); }}
            body {{ margin: 0; padding: 0; background: transparent; font-family: 'CustomCairo', sans-serif; }}
            .main-wrapper {{ width: 1080px; height: 1080px; padding: 15px 20px; box-sizing: border-box; background: url('{bg_b64}') center/100% 100% no-repeat; display: flex; flex-direction: column; overflow: hidden; }}
            .header-container {{ text-align: center; margin-top: 5px; margin-bottom: 10px; }}
            .city-title {{ display: inline-block; background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(10px); border: 2px solid rgba(255,255,255,0.4); border-radius: 25px; padding: 5px 50px; font-size: 38pt; color: #0d47a1; font-weight: 900; box-shadow: 0 10px 20px rgba(0,0,0,0.1); text-shadow: 1px 2px 5px rgba(0,0,0,0.3); }}
            .grid-container {{ display: flex; justify-content: space-between; gap: 10px; padding: 0 10px; }}
            
            .card {{ background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(8px); border-top: 2px solid rgba(255,255,255,0.6); border-left: 2px solid rgba(255,255,255,0.6); border-right: 1px solid rgba(255,255,255,0.2); border-bottom: 1px solid rgba(255,255,255,0.2); border-radius: 18px; padding: 10px 8px; width: 19%; height: fit-content; box-sizing: border-box; text-align: center; box-shadow: 5px 10px 20px rgba(0,0,0,0.15); display: flex; flex-direction: column; transition: 0.3s; }}
            
            .alert-card {{ background: rgba(231, 76, 60, 0.25) !important; border: 2px solid rgba(231, 76, 60, 0.9) !important; box-shadow: 0 0 20px rgba(231, 76, 60, 0.6) !important; }}
            .alert-day {{ background: linear-gradient(90deg, #900C3F, #C70039) !important; }}
            .alert-badge {{ background: #c0392b; color: white; font-size: 11pt; font-weight: bold; padding: 2px 5px; border-radius: 8px; margin-bottom: 6px; box-shadow: 0 2px 5px rgba(0,0,0,0.3); text-shadow: 1px 1px 2px rgba(0,0,0,0.5); }}

            .day-name {{ background: linear-gradient(90deg, #0d47a1, #1976d2); color: white; padding: 4px; border-radius: 10px; font-size: 13pt; font-weight: 900; margin-bottom: 6px; text-shadow: 1px 2px 4px rgba(0,0,0,0.5); }}
            .weather-icon {{ font-size: 34pt; margin: 0; filter: drop-shadow(0 5px 10px rgba(0,0,0,0.2)); }}
            .temp-box {{ font-size: 26pt; color: #c0392b; font-weight: 900; margin-bottom: 3px; text-shadow: 0 2px 4px rgba(255,255,255,0.9); border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 3px; }}
            .details-list {{ text-align: right; margin-bottom: 5px; border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 5px; }}
            .d-item {{ font-size: 13pt; color: #000; font-weight: 900; margin-bottom: 3px; text-shadow: 0 1px 4px rgba(255,255,255,0.9); }}
            .val {{ color: #111; font-weight: 900; }}
            .med-indicators {{ display: flex; flex-direction: column; gap: 6px; margin-top: auto; }}
            .m-box {{ padding: 6px; border-radius: 10px; border: 2px solid; box-shadow: inset 0 2px 5px rgba(255,255,255,0.3); background-blend-mode: overlay; }}
            .m-title {{ font-size: 12pt; color: #111; font-weight: 900; text-shadow: 0 1px 2px rgba(255,255,255,0.9); }}
            .m-val {{ font-size: 15pt; font-weight: 900; margin-top: 2px; color: #ffffff; text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000, 0px 4px 6px rgba(0,0,0,0.8); }}
        </style>
        </head>
        <body>
            <div class="main-wrapper">
                <div class="header-container"><div class="city-title">{city_data['name_ar']}</div></div>
                <div class="grid-container">{cards_html}</div>
            </div>
        </body>
        </html>
        """
        out_name = f"infographic_{city_data['id']}.png"
        self.hti.screenshot(html_str=html_content, save_as=out_name, size=(1080, 1080))
        logger.info(f"✅ تم حفظ الصورة: {out_name}")

    def generate_website(self, cities):
        html = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>النشرة الطبية - مجموعة الأمل</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Cairo', sans-serif; background: #eef2f3; margin: 0; padding: 20px; text-align: center; color: #333; }
        h1 { color: #0d47a1; margin-bottom: 5px; font-weight: 900; }
        p { font-size: 1.2rem; color: #555; margin-top: 0; margin-bottom: 30px; font-weight: 700; }
        .grid { display: flex; flex-wrap: wrap; justify-content: center; gap: 30px; }
        .city-card { width: 100%; max-width: 500px; }
        img { width: 100%; border-radius: 20px; box-shadow: 0 15px 30px rgba(0,0,0,0.15); transition: transform 0.3s; }
        img:hover { transform: scale(1.02); }
        .footer { margin-top: 40px; font-size: 0.9rem; color: #777; }
        
        /* تصميم واجهة مساعد الأمل الذكي */
        #ai-chat-container {
            max-width: 600px;
            margin: 40px auto 20px auto;
            background: #ffffff;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            overflow: hidden;
            border-right: 5px solid #0d47a1;
            text-align: right;
        }
        .chat-header {
            background: #0d47a1;
            color: white;
            padding: 15px 20px;
            font-weight: 900;
            font-size: 1.1rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .chat-body {
            padding: 20px;
            max-height: 300px;
            overflow-y: auto;
            background: #f9fbfd;
            font-size: 0.95rem;
            color: #444;
        }
        .chat-footer {
            padding: 15px;
            background: #fff;
            border-top: 1px solid #eee;
            display: flex;
            gap: 10px;
        }
        .chat-input {
            flex: 1;
            padding: 10px 15px;
            border: 1px solid #ccc;
            border-radius: 10px;
            font-family: 'Cairo', sans-serif;
            outline: none;
        }
        .chat-btn {
            background: #0d47a1;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 10px;
            font-weight: bold;
            cursor: pointer;
            font-family: 'Cairo', sans-serif;
        }
        .chat-btn:hover { background: #1565c0; }
        .message { margin-bottom: 12px; padding: 10px 14px; border-radius: 12px; line-height: 1.5; }
        .bot-msg { background: #eef2f3; color: #333; margin-left: 20px; }
        .user-msg { background: #0d47a1; color: white; margin-right: 20px; text-align: left; }
    </style>
</head>
<body>
    <h1>🌤️ النشرة الطبية لمرضى الحساسية والربو</h1>
    <p>برعاية مجموعة الأمل الطبية - Organon</p>
    <div class="grid">
"""
        for city in cities.values():
            html += f'\n        <div class="city-card"><img src="output/infographic_{city["id"]}.png" alt="نشرة {city["name_ar"]}"></div>'
            
        html += """
    </div>

    <!-- واجهة مساعد الأمل الذكي داخل الموقع -->
    <div id="ai-chat-container">
        <div class="chat-header">
            <span>🤖 مساعد الأمل الذكي (AI-powered Assistant)</span>
        </div>
        <div class="chat-body" id="chat-messages">
            <div class="message bot-msg">أهلاً بك زميلي العزيز. أنا مساعد الأمل الذكي، جاهز للإجابة على استفساراتك حول النشرة الطبية، معلومات الأدوية، والجرعات الموثقة. تفضل بطرح سؤالك.</div>
        </div>
        <div class="chat-footer">
            <input type="text" id="user-input" class="chat-input" placeholder="اكتب استفسارك هنا..." onkeypress="if(event.key === 'Enter') sendMessage();">
            <button class="chat-btn" onclick="sendMessage()">إرسال</button>
        </div>
    </div>

    <script>
        function sendMessage() {
            const input = document.getElementById('user-input');
            const messages = document.getElementById('chat-messages');
            const text = input.value.trim();
            if(!text) return;

            messages.innerHTML += `<div class="message user-msg">${text}</div>`;
            input.value = '';
            messages.scrollTop = messages.scrollHeight;

            setTimeout(() => {
                messages.innerHTML += `<div class="message bot-msg">شكراً لتواصلك. تم تسجيل استفسارك وسيتم توجيهه لقسم المعلومات الطبية بمجموعة الأمل. (ملاحظة: المساعد أداة توجيهية ولا يُغني عن استشارة الطبيب أو الصيدلي).</div>`;
                messages.scrollTop = messages.scrollHeight;
            }, 1000);
        }
    </script>

    <div class="footer">تم التحديث تلقائياً بواسطة Medical Weather Engine</div>
</body>
</html>"""
        
        index_path = os.path.join(self.base_project_dir, "index.html")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(html)
        logger.info("🌐 تم إنشاء صفحة الموقع مع مساعد الأمل الذكي بنجاح: index.html")

if __name__ == "__main__":
    BulletinGenerator().generate_all_bulletins()