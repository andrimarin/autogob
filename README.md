# AutoGob - Plataforma de Colas para Requerimientos Sociales

Este proyecto implementa una aplicación web para el registro y gestión de requerimientos sociales de ciudadanos, proporcionando un sistema de colas organizado para el gobierno.

## Características

- **Registro de Requerimientos**: Los ciudadanos pueden registrar sus necesidades sociales
- **Sistema de Colas**: Gestión organizada de requerimientos por prioridad
- **Tipos de Requerimientos**: Salud, Educación, Vivienda, Empleo, Alimentación, Transporte
- **Estados de Seguimiento**: Pendiente, En Proceso, Completado, Cancelado
- **Niveles de Prioridad**: Baja, Normal, Alta, Urgente
- **API REST**: Endpoints para integración con otros sistemas
- **Interfaz Web**: Panel de control para gestión y seguimiento

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/andrimarin/autogob.git
cd autogob
```

2. Crear y activar un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. Ejecutar la aplicación:
```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

## Uso

### Registro de Requerimientos

1. Navegar a "Registrar Requerimiento"
2. Completar el formulario con:
   - Información del ciudadano (nombre, email, teléfono)
   - Tipo de requerimiento
   - Descripción detallada
   - Prioridad
3. Enviar el formulario

### Gestión de Cola

1. Acceder a "Estado de Cola"
2. Ver todos los requerimientos registrados
3. Actualizar estados según el progreso
4. Ver detalles completos de cada requerimiento

## API REST

### Endpoints Disponibles

- `GET /api/requirements` - Obtener todos los requerimientos
- `POST /api/requirements` - Crear nuevo requerimiento
- `PUT /api/requirements/{id}/status` - Actualizar estado de requerimiento

### Ejemplo de Uso de API

```bash
# Crear nuevo requerimiento
curl -X POST http://localhost:5000/api/requirements \
  -H "Content-Type: application/json" \
  -d '{
    "citizen_name": "Juan Pérez",
    "citizen_email": "juan@email.com",
    "requirement_type": "salud",
    "description": "Necesito atención médica urgente",
    "priority": "alta"
  }'

# Actualizar estado
curl -X PUT http://localhost:5000/api/requirements/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'
```

## Estructura del Proyecto

```
autogob/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias Python
├── .env.example          # Variables de entorno ejemplo
├── templates/            # Plantillas HTML
│   ├── base.html
│   ├── index.html
│   ├── register.html
│   └── queue.html
├── static/              # Archivos estáticos
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── social_requirements.db # Base de datos SQLite
```

## Modelo de Datos

### SocialRequirement

- `id`: Identificador único
- `citizen_name`: Nombre del ciudadano
- `citizen_email`: Email del ciudadano
- `citizen_phone`: Teléfono (opcional)
- `requirement_type`: Tipo de requerimiento
- `description`: Descripción detallada
- `status`: Estado actual (pending, in_progress, completed, cancelled)
- `priority`: Prioridad (baja, normal, alta, urgente)
- `created_at`: Fecha de creación
- `updated_at`: Fecha de última actualización

## Tecnologías

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Base de Datos**: SQLite (configurable para PostgreSQL/MySQL)
- **Formularios**: Flask-WTF, WTForms

## Contribuir

1. Fork del repositorio
2. Crear rama para feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para detalles.

## Soporte

Para soporte técnico o consultas, por favor crear un issue en el repositorio de GitHub.
