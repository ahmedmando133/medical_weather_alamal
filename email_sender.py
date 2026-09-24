import os
import smtplib
from email.message import EmailMessage

def send_infographics_email():
    # 1. إعدادات الإيميل المرسل (إيميلك والباسورد الخاص بالتطبيقات)
    SENDER_EMAIL = "ahmed.mohamed.abdelmawgoud@gmail.com"
    APP_PASSWORD = "ueojstnpoisbvzww"
    
    # 2. قائمة المستلمين (بالإيميلات اللي إنت ضفتها)
    RECEIVER_EMAILS = [
        "ahmed.abdelmawgood@amalgrp.com",
        "exampel2@gmail.com",
        "exaple3@gmail.com"
    ]
    
    msg = EmailMessage()
    msg['Subject'] = '📊 النشرة الطبية ومؤشرات الحساسية الأسبوعية | مجموعة الأمل الطبية'
    msg['From'] = SENDER_EMAIL
    
    # دمج كل الإيميلات عشان تتبعتلهم كلهم في نفس اللحظة
    msg['To'] = ", ".join(RECEIVER_EMAILS)
    
    # 3. محتوى الرسالة (صياغة طبية احترافية)
    email_body = """السادة الأطباء والزملاء الكرام،

مرفق طيه النشرة الجوية الطبية المحدثة لمدن ليبيا لهذا الأسبوع.

تم احتساب (مؤشر الحساسية) و (خطر الربو) بدقة استناداً إلى المعايير الطبية العالمية لمنظمة الصحة العالمية (WHO Guidelines) لجودة الهواء. حيث يقيس (مؤشر الحساسية) مستويات الغبار والجسيمات الدقيقة، بينما يعكس (خطر الربو) تأثير الرطوبة والغازات المهيجة على الجهاز التنفسي.

⚠️ نوصي بالالتزام التام بالخطط العلاجية وجرعات بخاخات الأنف ومضادات الحساسية الموصوفة من قِبل طبيبك المختص.

مع خالص التحيات،
مجموعة الأمل الطبية
Organon | Al Amal Medicine Group"""
    
    msg.set_content(email_body)

    # 4. سحب الصور من فولدر output
    output_dir = 'output'
    attachments_added = False
    
    if os.path.exists(output_dir):
        for filename in os.listdir(output_dir):
            if filename.endswith('.png'):
                filepath = os.path.join(output_dir, filename)
                with open(filepath, 'rb') as f:
                    img_data = f.read()
                
                msg.add_attachment(img_data, maintype='image', subtype='png', filename=filename)
                attachments_added = True
                print(f"📎 تم إرفاق الصورة: {filename}")

    if not attachments_added:
        print("⚠️ لم يتم العثور على أي صور PNG في مجلد output لإرسالها.")
        return

    # 5. الاتصال بسيرفر جوجل وإرسال الإيميل
    try:
        print("\n🚀 جاري الاتصال بخوادم جوجل وإرسال الإيميل...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
        print("✅ تم إرسال الإيميل بنجاح لجميع المستلمين!")
    except Exception as e:
        print(f"❌ حدث خطأ أثناء الإرسال: {e}")

if __name__ == "__main__":
    send_infographics_email()