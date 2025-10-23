# email_service.py
import httpx # Usaremos httpx para peticiones async
from models import ContactCreate
from settings import settings

def _build_email_body(contact: ContactCreate) -> str:
    """Construye el cuerpo del correo en texto plano."""
    return f"""
Nuevo mensaje desde el formulario de contacto de LINMSO:

--- INFORMACIÓN DEL CLIENTE ---
- Nombre: {contact.nombre}
- Empresa: {contact.empresa or 'No especificada'}
- Teléfono: {contact.telefono}
- Email: {contact.email}

--- DETALLES DE LA SOLICITUD ---
- Servicio Solicitado: {contact.servicio.replace('-', ' ').title()}
- Mensaje:
{contact.mensaje or 'El cliente no dejó un mensaje adicional.'}

---
Enviado desde el sitio web.
    """

async def send_contact_notification(contact: ContactCreate) -> bool:
    """Envía la notificación por correo usando la API de Mailgun."""
    api_key = settings.MAILGUN_API_KEY
    domain = settings.MAILGUN_DOMAIN
    
    if not api_key or not domain:
        print("ERROR: Faltan las variables de entorno de Mailgun (API_KEY, DOMAIN).")
        return False

    api_url = f"https://api.mailgun.net/v3/{domain}/messages"
    email_data = {
        "from": settings.FROM_EMAIL,
        "to": settings.TO_EMAIL,
        "subject": f"Nuevo Contacto Web: {contact.nombre}",
        "text": _build_email_body(contact)
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(api_url, auth=("api", api_key), data=email_data)
            response.raise_for_status() # Lanza un error si la petición falla (status code 4xx o 5xx)
            print("Correo enviado exitosamente a través de Mailgun.")
            return True
        except httpx.HTTPStatusError as e:
            print(f"Error al enviar el correo con Mailgun: {e.response.status_code} - {e.response.text}")
            return False
        except Exception as e:
            print(f"Un error inesperado ocurrió: {e}")
            return False