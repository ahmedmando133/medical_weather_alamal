import requests
import logging

logger = logging.getLogger(__name__)

class OpenMeteoClient:
    def __init__(self):
        self.weather_url = "https://api.open-meteo.com/v1/forecast"
        self.air_quality_url = "https://air-quality-api.open-meteo.com/v1/air-quality"

    def fetch_data(self, lat, lon, timezone="Auto"):
        try:
            weather_params = {
                "latitude": lat,
                "longitude": lon,
                "daily": "weathercode,temperature_2m_max,temperature_2m_min,wind_speed_10m_max,wind_direction_10m_dominant,uv_index_max",
                "hourly": "relative_humidity_2m",
                "timezone": timezone
            }
            w_resp = requests.get(self.weather_url, params=weather_params)
            w_resp.raise_for_status()
            
            aq_params = {
                "latitude": lat,
                "longitude": lon,
                # تمت إضافة grass_pollen و olive_pollen لسحب بيانات اللقاح
                "hourly": "pm10,pm2_5,dust,ozone,nitrogen_dioxide,sulphur_dioxide,grass_pollen,olive_pollen",
                "timezone": timezone
            }
            aq_resp = requests.get(self.air_quality_url, params=aq_params)
            aq_resp.raise_for_status()
            
            return {"weather": w_resp.json(), "air_quality": aq_resp.json()}
        except Exception as e:
            logger.error(f"❌ خطأ API: {e}")
            return None