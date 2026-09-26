import os
import smtplib
from email.message import EmailMessage

def send_infographics_email():
    # 1. إعدادات الإيميل المرسل (إيميلك والباسورد الخاص بالتطبيقات)
    SENDER_EMAIL = "ahmed.mohamed.abdelmawgoud@gmail.com"
    APP_PASSWORD = "ueojstnpoisbvzww"
    
    # 2. قائمة المستلمين
    RECEIVER_EMAILS = [
        "ahmed.abdelmawgood@amalgrp.com",, 
    "Faisal.marghni@amalgrp.com"]
    
    msg = EmailMessage()
    msg['Subject'] = '📊 النشرة الطبية ومؤشرات الحساسية الأسبوعية | مجموعة الأمل الطبية'
    msg['From'] = SENDER_EMAIL
    
    # دمج كل الإيميلات عشان تتبعتلهم كلهم في نفس اللحظة
    msg['To'] = ", ".join(RECEIVER_EMAILS)
    
    # 3. محتوى الرسالة (النسخة النصية العادية)
    text_body = """السادة الأطباء والزملاء الكرام،

مرفق طيه النشرة الجوية الطبية المحدثة لمدن ليبيا.

تم احتساب (مؤشر الحساسية) و (خطر الربو) بدقة استناداً إلى المعايير الطبية العالمية لمنظمة الصحة العالمية (WHO Guidelines) لجودة الهواء.

🌐 جديد: يمكنكم الآن متابعة النشرة التفاعلية المحدثة يومياً لجميع المدن عبر الرابط التالي:
https://ahmedmando133.github.io/medical_weather_alamal/

🤖 مساعد الأمل الذكي داخل الموقع:
يتضمن الموقع مساعداً ذكياً (AI-powered assistant) لمساعدتكم في الوصول السريع لمعلومات الأدوية، تفاصيل النشرة الطبية، جرعاتها الموثقة، والإجابة عن الاستفسارات المرتبطة بخدمات مجموعة الأمل الطبية. يمكنكم التحدث معه مباشرة داخل الموقع لأي استفسار توجيهي (ملاحظة: المساعد أداة معلوماتية وتوجيهية ولا يُغني عن وصفة الطبيب أو استشارة الصيدلي).

⚠️ نوصي بتوجيه المرضى للالتزام التام بالخطط العلاجية وجرعات بخاخات الأنف ومضادات الحساسية الموصوفة من قِبل سيادتكم.

مع خالص التحيات،
أحمد عبد الموجود
Senior Medical Representative - Organon
Al Amal Medicine Group
"""

    # محتوى الرسالة (نسخة الـ HTML الاحترافية للزر التفاعلي والـ AI Assistant)
    html_body = """
    <div dir="rtl" style="font-family: Arial, sans-serif; font-size: 16px; color: #333; line-height: 1.6;">
        <p>السادة الأطباء والزملاء الكرام،</p>
        <p>مرفق طيه النشرة الجوية الطبية المحدثة لمدن ليبيا.</p>
        <p>تم احتساب <b>(مؤشر الحساسية)</b> و <b>(خطر الربو)</b> بدقة استناداً إلى المعايير الطبية العالمية لمنظمة الصحة العالمية (WHO Guidelines) لجودة الهواء.</p>

        <div style="background-color: #f4f6f9; border-right: 4px solid #0d47a1; padding: 15px; margin: 20px 0;">
            <h3 style="margin-top: 0; margin-bottom: 10px; color: #0d47a1;">🌐 لوحة الطقس الطبي التفاعلية</h3>
            <p style="margin-top: 0; margin-bottom: 15px;">يمكنكم الآن متابعة النشرة المحدثة يومياً لجميع المدن بضغطة واحدة من أي جهاز عبر الرابط التالي:</p>
            <a href="https://ahmedmando133.github.io/medical_weather_alamal/" style="background-color: #0d47a1; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">عرض النشرة الطبية المباشرة</a>
        </div>

        <div style="background-color: #eef2f3; border-right: 4px solid #1976d2; padding: 15px; margin: 20px 0;">
            <h4 style="margin-top: 0; margin-bottom: 8px; color: #0d47a1;">🤖 مساعد الأمل الذكي (AI-powered Assistant)</h4>
            <p style="margin-top: 0; margin-bottom: 0; font-size: 15px;">
                يحتوي الموقع على مساعد ذكي متكامل لمساعدتكم في استعراض معلومات الأدوية، تفاصيل النشرة الطبية، جرعاتها الموثقة، والإجابة عن أي استفسار متعلق بخدمات ومحتوى مجموعة الأمل الطبية. يمكنكم التحدث معه مباشرة داخل الموقع للحصول على التوجيه والمعلومات بكل سهولة. 
                <br><small style="color: #666;">(ملاحظة: المساعد أداة توجيهية ومعلوماتية ولا يُغني عن التقييم السريري ووصفة الطبيب أو الصيدلي).</small>
            </p>
        </div>

        <p>⚠️ نوصي بتوجيه المرضى للالتزام التام بالخطط العلاجية وجرعات بخاخات الأنف ومضادات الحساسية الموصوفة من قِبل سيادتكم.</p>
        <br>
        <p>مع خالص التحيات،<br>
        <b>أحمد عبد الموجود</b><br>
        Senior Medical Representative - Organon<br>
        Al Amal Medicine Group</p>
    </div>
    """
    
    # دمج النسختين في الإيميل
    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype='html')

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