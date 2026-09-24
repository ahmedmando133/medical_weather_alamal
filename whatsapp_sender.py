import pywhatkit
import os
import time

# قائمة الأطباء (تأكد من كتابة الأرقام بمفتاح ليبيا +218 بدون أصفار في البداية)
doctors = [
    {"name": "Ahmed Abdelmawgood", "phone": "+218931571358", "city_id": "tripoli"},
    # يمكنك إضافة المزيد بنسخ السطر وتغيير البيانات
    # {"name": "د. أحمد", "phone": "+218911111111", "city_id": "benghazi"},
]

def send_whatsapp_bulletins():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "output")
    
    print("🚀 جاري بدء حملة الواتساب... (برجاء عدم استخدام الماوس أو الكيبورد أثناء الإرسال)")
    
    for doc in doctors:
        img_path = os.path.join(output_dir, f"infographic_{doc['city_id']}.png")
        
        if not os.path.exists(img_path):
            print(f"⚠️ صورة مدينة {doc['city_id']} غير موجودة، سيتم تخطي {doc['name']}.")
            continue
            
        # الرسالة المرفقة مع الصورة
        caption = f"صباح الخير {doc['name']}،\nمرفق لسيادتكم النشرة الطبية لمرضى الحساسية والربو لهذا الأسبوع.\nمع تحيات مجموعة الأمل الطبية."
        
        print(f"📲 جاري التحضير للإرسال إلى {doc['name']}...")
        
        try:
            # فتح واتساب ويب، انتظار 20 ثانية للتحميل، إرسال الصورة، ثم إغلاق التاب
            pywhatkit.sendwhats_image(
                receiver=doc['phone'],
                img_path=img_path,
                caption=caption,
                wait_time=20,
                tab_close=True,
                close_time=5
            )
            print(f"✅ تم الإرسال بنجاح إلى {doc['name']}!")
            time.sleep(7)  # فاصل زمني أمان لتجنب حظر الواتساب
            
        except Exception as e:
            print(f"❌ فشل الإرسال إلى {doc['name']}: {e}")

if __name__ == "__main__":
    send_whatsapp_bulletins()