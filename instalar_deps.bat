@echo off
title 📦 Instalando dependencias desde requirements.txt
color 0B

echo ===============================================
echo    INSTALACIÓN DE DEPENDENCIAS DEL PROYECTO
echo ===============================================
echo.


REM Cambiar al directorio del proyecto
cd /d "C:\Users\Bernardo\Desktop\streamlit-db-inspector"

REM Activar entorno virtual
echo 🔄 Activando entorno virtual...
call venv\Scripts\activate

REM Instalar dependencias
echo 📦 Instalando paquetes desde requirements.txt...
pip install -r requirements.txt

echo.
echo ✅ ¡Instalación completada!
echo -----------------------------------------------
cmd /k
