import os
import time
from openai import OpenAI
from dotenv import load_dotenv
import logging

load_dotenv(override=True)
logger = logging.getLogger(__name__)

class ContentGenerator:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("لم يتم العثور على مفتاح GEMINI_API_KEY في ملف .env")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        self.model_name = "gemini-3.8-flash"

    def generate_weekly_advice_batch(self, city_ar: str, days_data: list) -> list:
        """
        يولد 5 نصائح مختلفة ومتنوعة تماماً للأيام الخمسة دفعة واحدة لتجنب أي تكرار.
        """
        prompt = f"""
        أنت مسؤول التوعية الطبية والتسويق في "مجموعة الأمل الطبية" في ليبيا.
        المطلوب كتابة 5 نصائح طبية توعوية مختلفة ومتنوعة تماماً (يوم بعد يوم) لمرضى حساسية الأنف والربو في مدينة {city_ar} للتوقعات خلال 5 أيام القادمة.
        
        ايقاع التنوع المطلوب للأيام الخمسة:
        - اليوم الأول: التركيز على إغلاق النوافذ وقت حركة الرياح والغبار الخفيف.
        - اليوم الثاني: التركيز على شرب السوائل وترطيب الأنف والوقاية المنزلية.
        - اليوم الثالث: التركيز على الالتزام بالعلاج الوقائي الموصوف (مثل الاستمرار على الأدوية الأصلية مثل Nasonex أو Aerius والتأكد من وجود استيكر مجموعة الأمل الطبية).
        - اليوم الرابع: التركيز على ارتداء الكمامة أو النظارة عند الخروج لتجنب المهيجات.
        - اليوم الخامس: التركيز على تقليل الأنشطة الخارجية والتعامل بحذر مع أوقات الذروة.

        قواعد صارمة جداً:
        1. اجعل كل نصيحة قصيرة (سطرين إلى 3 أسطر) وبصيغة عربية فصحى بأسلوب تسويقي راقٍ وموجه للمريض.
        2. لا تكرر نفس الجمل في الأيام الخمسة أبداً.
        3. لا تدعي قياس كل مسببات الحساسية، واربط العلاج باستشارة الطبيب أو الصيدلي مع التنويه بالاستيكر الأصلي للمجموعة عند الحاجة.
        4. أرجع النتيجة على شكل قائمة مفصولة برقم اليوم (مثلاً: 1. النصيحة... \n 2. النصيحة...).
        """

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}]
                )
                text_result = response.choices[0].message.content.strip()
                
                lines = [line.strip() for line in text_result.split('\n') if line.strip()]
                advice_list = []
                for line in lines:
                    cleaned = line.lstrip('123456789.-* )')
                    if len(cleaned) > 10:
                        advice_list.append(cleaned)
                
                if len(advice_list) >= 5:
                    return advice_list[:5]
                elif advice_list:
                    while len(advice_list) < 5:
                        advice_list.append(advice_list[-1])
                    return advice_list

            except Exception as e:
                logger.warning(f"محاولة الدفعة {attempt + 1} فشلت، جاري المحاولة...")
                time.sleep(2)

        return [
            "احرص على إغلاق النوافذ جيداً وتجنب التعرض المباشر للتيارات الهوائية المحملة بالأتربة.",
            "حافظ على ترطيب جسمك بشرب السوائل بكثرة واستخدام المحاليل الملحية لتنظيف مجرى التنفس.",
            "التزم بخطتك العلاجية الوقائية الموصوفة (مثل Nasonex أو Aerius)، وتأكد من وجود استيكر مجموعة الأمل الطبية الأصلي.",
            "ارتدِ كمامة خفيفة أو نظارة واقية عند الاضطرار للخروج في الأوقات التي تقل فيها جودة الهواء.",
            "قلل من الأنشطة الخارجية المباشرة وتابع النشرة اليومية لحماية صحتك وصحة أفراد عائلتك."
        ]