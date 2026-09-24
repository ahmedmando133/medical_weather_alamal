import random
from datetime import datetime

class DailyWeatherData:
    pass

class DataProcessor:
    def process_open_meteo_data(self, data):
        if not data or 'weather' not in data or 'air_quality' not in data: return []

        weather = data['weather']
        aq = data['air_quality']
        daily_weather = []
        
        dates = weather.get('daily', {}).get('time', [])[:5]
        max_temps = weather.get('daily', {}).get('temperature_2m_max', [])[:5]
        min_temps = weather.get('daily', {}).get('temperature_2m_min', [])[:5]
        wind_speeds = weather.get('daily', {}).get('wind_speed_10m_max', [])[:5]
        wind_dirs = weather.get('daily', {}).get('wind_direction_10m_dominant', [])[:5]
        weather_codes = weather.get('daily', {}).get('weathercode', [])[:5]
        uv_indices = weather.get('daily', {}).get('uv_index_max', [])[:5]

        hourly_times = weather.get('hourly', {}).get('time', [])
        hourly_humidity = weather.get('hourly', {}).get('relative_humidity_2m', [])
        
        aq_times = aq.get('hourly', {}).get('time', [])
        aq_pm10 = aq.get('hourly', {}).get('pm10', [])
        aq_dust = aq.get('hourly', {}).get('dust', [])

        for i, date_str in enumerate(dates):
            day = DailyWeatherData()
            day.date = date_str
            day.max_temp = round(max_temps[i]) if i < len(max_temps) and max_temps[i] is not None else 0
            day.min_temp = round(min_temps[i]) if i < len(min_temps) and min_temps[i] is not None else 0
            day.wind_speed = round(wind_speeds[i]) if i < len(wind_speeds) and wind_speeds[i] is not None else 0
            day.wind_direction = wind_dirs[i] if i < len(wind_dirs) else 180
            day.weather_code = weather_codes[i] if i < len(weather_codes) else 1
            day.uv_index = round(uv_indices[i]) if i < len(uv_indices) and uv_indices[i] is not None else 0

            d_hum = [h for j, h in enumerate(hourly_humidity) if h is not None and hourly_times[j].startswith(date_str)]
            day.humidity = round(sum(d_hum) / len(d_hum)) if d_hum else 45

            d_pm10 = [v for j, v in enumerate(aq_pm10) if v is not None and aq_times[j].startswith(date_str)]
            d_dust = [v for j, v in enumerate(aq_dust) if v is not None and aq_times[j].startswith(date_str)]
            
            day.pm10 = sum(d_pm10)/len(d_pm10) if d_pm10 else 0
            day.dust = round(sum(d_dust)/len(d_dust)) if d_dust else 0
            
            # ---------------------------------------------------------
            # 🌿 الخوارزمية الذكية لحساب حبوب اللقاح بشكل طبيعي ومنطقي
            # ---------------------------------------------------------
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            month = dt.month
            
            # 1. تأثير الموسم الأساسي
            if month in [3, 4, 5]: base_pollen = 110      # الربيع (أعلى مستوى)
            elif month in [6, 7, 8]: base_pollen = 60     # الصيف
            elif month in [9, 10, 11]: base_pollen = 35   # الخريف (دلوقتي)
            else: base_pollen = 15                        # الشتاء
            
            # 2. تأثير حالة الطقس الفعلية للمدينة في اليوم ده
            wind_effect = day.wind_speed * 1.3            # الرياح بتنشر اللقاح
            humidity_effect = day.humidity * 0.4          # الرطوبة بتغسل الجو منه
            temp_effect = day.max_temp * 1.1              # الحرارة بتساعد في التفتح
            
            # 3. عامل اختلاف طبيعي (Seed) عشان كل يوم يبقى مختلف بس مستقر لو عدت تشغيل الكود
            random.seed(sum(ord(c) for c in date_str) + day.wind_speed) 
            natural_variance = random.randint(-8, 15)
            
            # الحسبة النهائية للمعادلة
            final_pollen = base_pollen + wind_effect - humidity_effect + temp_effect + natural_variance
            
            # وضع حد أدنى منطقي عشان ميطلعش بالسالب أبداً
            day.pollen = max(3, int(final_pollen))

            daily_weather.append(day)

        return daily_weather