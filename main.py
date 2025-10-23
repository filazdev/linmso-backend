# main.py
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

# Importar lógica y modelos de otros archivos
from models import ContactCreate
from email_service import send_contact_notification
from settings import settings

app = FastAPI(title="LINMSO Contact API", version="1.0.0")

# Configurar CORS para permitir peticiones desde GitHub Pages
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Endpoint de salud para verificar que el servicio está activo."""
    return {"status": "ok"}

@app.post("/api/v1/contact", response_class=HTMLResponse)
async def create_contact(
    nombre: str = Form(...),
    empresa: str = Form(None),
    telefono: str = Form(...),
    email: str = Form(...),
    servicio: str = Form(...),
    mensaje: str = Form(None),
):
    try:
        # Validación de los datos del formulario usando el modelo Pydantic
        contact_data = ContactCreate(
            nombre=nombre, empresa=empresa, telefono=telefono,
            email=email, servicio=servicio, mensaje=mensaje
        )

        # Enviar la notificación por correo
        success = await send_contact_notification(contact_data)

        if success:
            success_headers = {"HX-Trigger": "form-sent-successfully"}
            success_html = '<div id="form-response" class="success"><strong>¡Mensaje enviado!</strong> Te contactaremos pronto.</div>'
            return HTMLResponse(content=success_html, headers=success_headers)
        else:
            # Mensaje de error si la API de Mailgun falla
            return '<div id="form-response" class="error"><strong>Error en el sistema.</strong> No pudimos enviar tu mensaje. Por favor, contáctanos por WhatsApp.</div>'

    except ValidationError as e:
        # Si la validación de Pydantic falla, devuelve el primer error
        error_msg = e.errors()[0]['msg']
        return f'<div id="form-response" class="error"><strong>Error de validación:</strong> {error_msg}.</div>'
    
    except Exception as e:
        # Captura cualquier otro error inesperado
        print(f"Error inesperado en el endpoint: {e}")
        return '<div id="form-response" class="error"><strong>Error interno.</strong> No se pudo procesar tu solicitud.</div>'