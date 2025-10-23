# models.py
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
import re

class ContactCreate(BaseModel):
    nombre: str
    empresa: Optional[str] = None
    telefono: str
    email: EmailStr
    servicio: str
    mensaje: Optional[str] = None

    @validator('nombre')
    def nombre_no_vacio(cls, v):
        if not v.strip():
            raise ValueError('El nombre es requerido')
        return v.strip()

    @validator('telefono')
    def telefono_mexicano(cls, v):
        v_limpio = re.sub(r'\D', '', v)
        if len(v_limpio) != 10:
            raise ValueError('El teléfono debe contener 10 dígitos')
        return v_limpio

    @validator('servicio')
    def servicio_valido(cls, v):
        servicios_validos = [
            'personal-limpieza', 'limpieza-profunda', 'pulido-encerado',
            'fumigacion-sanitizacion', 'jardineria', 'venta-productos'
        ]
        if v not in servicios_validos:
            raise ValueError('Servicio no válido')
        return v