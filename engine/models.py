from pydantic import BaseModel
from typing import Optional

class DailyEnvironmentData(BaseModel):
    date: str
    max_temp: float
    min_temp: float
    wind_speed: float
    precipitation: float
    dust: Optional[float] = None
    pm10: Optional[float] = None
    pm25: Optional[float] = None
    aqi: Optional[float] = None
    pollen: Optional[float] = None
    
    # إضافة الحقول الجديدة لاتجاه الرياح والرطوبة لمنع ظهور أخطاء
    wind_direction: Optional[float] = 180
    humidity: Optional[float] = 45