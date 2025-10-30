# settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Email configuration (usaremos variables de entorno en Render)
    MAILGUN_API_KEY: str
    MAILGUN_DOMAIN: str

    # Email Addresses
    FROM_EMAIL: str # ej: "Formulario Web <mailgun@tu-dominio.com>"
    TO_EMAIL: str   # ej: "ventas@tu-dominio.com"

    # CORS
    FRONTEND_URL: str # ej: "https://tu-usuario.github.io"

    class Config:
        env_file = ".env" # Carga las variables desde el archivo .env

# Exportar la instancia para usarla en la aplicación

settings = Settings()