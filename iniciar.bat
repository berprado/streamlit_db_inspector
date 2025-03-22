@echo off
title Iniciando Streamlit DB Inspector
color 0A

echo ===============================================
echo   INICIANDO PROYECTO: Streamlit DB Inspector
echo ===============================================
echo.

REM Ir al directorio del proyecto
cd /d "C:\Users\Bernardo\Desktop\streamlit-db-inspector"

REM Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate

REM Abrir VS Code Insiders
echo Abriendo VS Code Insiders...
start code-insiders .

REM Actualizar requirements.txt
echo Actualizando archivo de dependencias (requirements.txt)...
pip freeze > requirements.txt
echo Requerimientos actualizados correctamente.

REM Ejecutar la app de Streamlit
echo Ejecutando la app Streamlit...
streamlit run app.py

REM Mantener ventana abierta
echo.
echo Todo listo. Puedes comenzar a trabajar.
echo -----------------------------------------------
cmd /k