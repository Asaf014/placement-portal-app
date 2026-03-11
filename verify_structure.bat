@echo off
setlocal enabledelayedexpansion

echo.
echo ============================================
echo  Project Structure Verification
echo ============================================
echo.

cd /d "%~dp0"

echo Checking backend files...
if exist backend\app.py echo [OK] app.py else echo [MISSING] app.py
if exist backend\config.py echo [OK] config.py else echo [MISSING] config.py
if exist backend\requirements.txt echo [OK] requirements.txt else echo [MISSING] requirements.txt
if exist backend\models\__init__.py echo [OK] models/__init__.py else echo [MISSING] models/__init__.py
if exist backend\routes\auth.py echo [OK] routes/auth.py else echo [MISSING] routes/auth.py
if exist backend\routes\admin.py echo [OK] routes/admin.py else echo [MISSING] routes/admin.py
if exist backend\routes\company.py echo [OK] routes/company.py else echo [MISSING] routes/company.py
if exist backend\routes\student.py echo [OK] routes/student.py else echo [MISSING] routes/student.py
if exist backend\services\user_service.py echo [OK] services/user_service.py else echo [MISSING] services/user_service.py
if exist backend\utils\auth.py echo [OK] utils/auth.py else echo [MISSING] utils/auth.py
if exist backend\utils\cache.py echo [OK] utils/cache.py else echo [MISSING] utils/cache.py
if exist backend\utils\email.py echo [OK] utils/email.py else echo [MISSING] utils/email.py
if exist backend\tasks\celery_tasks.py echo [OK] tasks/celery_tasks.py else echo [MISSING] tasks/celery_tasks.py

echo.
echo Checking frontend files...
if exist frontend\package.json echo [OK] package.json else echo [MISSING] package.json
if exist frontend\vue.config.js echo [OK] vue.config.js else echo [MISSING] vue.config.js
if exist frontend\public\index.html echo [OK] public/index.html else echo [MISSING] public/index.html
if exist frontend\src\main.js echo [OK] src/main.js else echo [MISSING] src/main.js
if exist frontend\src\App.vue echo [OK] src/App.vue else echo [MISSING] src/App.vue
if exist frontend\src\router\index.js echo [OK] src/router/index.js else echo [MISSING] src/router/index.js
if exist frontend\src\services\api.js echo [OK] src/services/api.js else echo [MISSING] src/services/api.js
if exist frontend\src\views\Home.vue echo [OK] src/views/Home.vue else echo [MISSING] src/views/Home.vue
if exist frontend\src\views\auth\Login.vue echo [OK] src/views/auth/Login.vue else echo [MISSING] src/views/auth/Login.vue
if exist frontend\src\views\auth\Register.vue echo [OK] src/views/auth/Register.vue else echo [MISSING] src/views/auth/Register.vue

echo.
echo Checking configuration and documentation files...
if exist setup.bat echo [OK] setup.bat else echo [MISSING] setup.bat
if exist setup.ps1 echo [OK] setup.ps1 else echo [MISSING] setup.ps1
if exist run.bat echo [OK] run.bat else echo [MISSING] run.bat
if exist README.md echo [OK] README.md else echo [MISSING] README.md
if exist QUICK_START.txt echo [OK] QUICK_START.txt else echo [MISSING] QUICK_START.txt
if exist IMPLEMENTATION_GUIDE.txt echo [OK] IMPLEMENTATION_GUIDE.txt else echo [MISSING] IMPLEMENTATION_GUIDE.txt
if exist .gitignore echo [OK] .gitignore else echo [MISSING] .gitignore

echo.
echo ============================================
echo  Verification Complete!
echo ============================================
echo.
echo If all files are marked [OK], your project structure is correct.
echo Run setup.bat to install dependencies and initialize the database.
echo.

pause
