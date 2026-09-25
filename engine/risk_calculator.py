class RiskCalculator:
    def __init__(self):
        # تم ترك الإيموجي لحالة "مرتفع" فارغاً هنا ليتم تخصيصه برمجياً لكل مؤشر
        self.risk_styles = {
            "low": {
                "level": "منخفض",
                "emoji": "😊",
                "bg": "rgba(46, 204, 113, 0.25)",
                "border": "rgba(39, 174, 96, 0.6)"
            },
            "moderate": {
                "level": "متوسط",
                "emoji": "😐",
                "bg": "rgba(241, 196, 15, 0.25)",
                "border": "rgba(243, 156, 18, 0.6)"
            },
            "high": {
                "level": "مرتفع",
                "emoji": "",  # سيتم حقنه في الأسفل بناءً على نوع المؤشر
                "bg": "rgba(230, 126, 34, 0.25)",
                "border": "rgba(211, 84, 0, 0.6)"
            },
            "severe": {
                "level": "مرتفع جداً",
                "emoji": "🚨",
                "bg": "rgba(231, 76, 60, 0.3)",
                "border": "rgba(192, 57, 43, 0.7)"
            }
        }

    def calculate_daily_risk(self, day_data):
        dust = float(str(day_data.dust).split()[0]) if str(day_data.dust).split()[0].replace('.', '', 1).isdigit() else 0
        humidity = float(day_data.humidity)
        wind = float(day_data.wind_speed)
        
        # تمت إضافة الحرارة العظمى من التحديث الجديد لتعزيز دقة التقييم الطبي
        max_temp = float(getattr(day_data, 'max_temp', 25))

        # 1. منطق الحساسية (الأنف) - تم دمج تأثير الحرارة العالية التي تسبب الجفاف والتهيج
        if dust > 60 or wind > 35 or (wind > 25 and max_temp > 38):
            nose_key = "severe"
        elif dust > 40 or wind > 25 or (max_temp > 35 and humidity < 30):
            nose_key = "high"
        elif dust > 20 or wind > 15 or humidity > 75:
            nose_key = "moderate"
        else:
            nose_key = "low"

        # 2. منطق خطر الربو (التنفس) - مدمج معه الخطر الحراري
        if dust > 50 or (humidity > 80 and wind > 30) or max_temp > 40:
            breath_key = "severe"
        elif dust > 30 or (humidity > 75 and wind > 20) or max_temp > 35:
            breath_key = "high"
        elif dust > 15 or humidity > 65 or wind > 15:
            breath_key = "moderate"
        else:
            breath_key = "low"

        # تخصيص كارت الحساسية
        nose_style = self.risk_styles[nose_key].copy()
        nose_style["title"] = "مؤشر الحساسية"
        if nose_key == "high":
            nose_style["emoji"] = "🤧"

        # تخصيص كارت الربو
        breath_style = self.risk_styles[breath_key].copy()
        breath_style["title"] = "خطر الربو"
        if breath_key == "high":
            breath_style["emoji"] = "😨"

        return {
            "nose": nose_style,
            "breath": breath_style
        }