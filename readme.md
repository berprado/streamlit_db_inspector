
```markdown
# 🧪 Streamlit DB Inspector

Aplicación desarrollada con **Python + Streamlit** para explorar esquemas de bases de datos **MySQL** y generar reportes. Ideal para Devs, DBAs o cualquier persona que necesite documentar estructuras de bases de datos.

---

## ⚙️ Requisitos

- Python 3.8+
- MySQL Server local o remoto
- Git
- VS Code Insiders (opcional, pero recomendado)

---

## 🏁 Configuración inicial del entorno

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu_usuario/streamlit_db_inspector.git
cd streamlit_db_inspector
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

> También puedes usar el script:
> `install_deps.bat`

---

## 🔐 Variables de entorno

Crea un archivo `.env` con tus credenciales de MySQL:

```env
DB_HOST=localhost
DB_USER=usuario
DB_PASSWORD=contraseña
DB_NAME=nombre_de_base
```

---

## 🚀 Ejecutar la aplicación

Puedes lanzar la app de dos formas:

### ✅ Manual:

```bash
venv\Scripts\activate
streamlit run app.py
```

### 🖱 Con doble clic:

> Ejecuta `start_project.bat`  
> Este script activa el entorno, abre VS Code Insiders, actualiza `requirements.txt`, y lanza la app.

---

## 🧹 Scripts incluidos

| Script               | Descripción                                      |
|----------------------|--------------------------------------------------|
| `start_project.bat`  | Inicia todo el entorno y ejecuta la app         |
| `install_deps.bat`   | Instala dependencias desde `requirements.txt`   |

---

## 📁 Estructura del proyecto

```
streamlit_db_inspector/
│
├── app.py                  # Interfaz principal con Streamlit
├── db_utils.py             # Funciones de conexión y consulta
├── .env                    # Credenciales (NO subir a GitHub)
├── .gitignore
├── requirements.txt
├── start_project.bat
├── install_deps.bat
└── venv/                   # Entorno virtual
```

---

## 🤝 Contribuciones

¡Bienvenidas! Puedes abrir issues o enviar PRs.

---

## 📜 Licencia

MIT

---

Desarrollado por berprado 

```

---
