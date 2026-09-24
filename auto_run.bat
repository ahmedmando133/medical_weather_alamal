@echo off
echo Starting Daily Medical Weather Update...

:: الانتقال لمسار المشروع الثابت
cd /d "C:\Allergy weather project"

:: تفعيل بيئة بايثون الافتراضية عشان المكتبات تشتغل صح
call venv\Scripts\activate

:: تشغيل كود توليد الصور والموقع
python -m engine.bulletin_generator

:: إرسال النشرة بالإيميل
python email_sender.py

:: رفع التحديثات أوتوماتيكياً على جيتهاب
git add .
git commit -m "Auto-update: Daily Medical Weather Bulletin"
git push

echo Update Completed Successfully!
exit