# 🛒 Zultech - E-commerce Platform

Plataforma de comercio electrónico desarrollada con Django para la venta de productos tecnológicos.

## 🚀 Características

- ✅ Sistema de autenticación personalizado (clientes y administradores)
- ✅ Gestión de productos con categorías
- ✅ Carrito de compras
- ✅ Sistema de pedidos
- ✅ Recuperación de contraseña por email
- ✅ Panel de administración con Jazzmin
- ✅ Responsive design
- ✅ Gestión de imágenes de productos

## 📋 Requisitos

- Python 3.13+
- SQLite (desarrollo) / PostgreSQL (producción)
- Pillow (manejo de imágenes)

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/BigBossSpektrum/MyWebsite.git
cd MyWebsite
```

### 2. Crear entorno virtual

```bash
python -m venv env
source env/bin/activate  # Linux/Mac
# o
env\Scripts\activate  # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia el archivo de ejemplo y configura tus credenciales:

```bash
cp .env.example .env
```

Edita `.env` con tus configuraciones. Para desarrollo local, puedes dejarlo como está (usa console backend para emails).

📧 **Para configurar el envío de emails reales, consulta [EMAIL_CONFIG.md](EMAIL_CONFIG.md)**

### 5. Aplicar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

Visita http://127.0.0.1:8000/

## 📧 Configuración de Email

El proyecto incluye un sistema completo de emails para:
- Recuperación de contraseñas
- Notificaciones de pedidos
- Soporte al cliente

Para configurar el envío de emails:

1. Lee la guía completa: [EMAIL_CONFIG.md](EMAIL_CONFIG.md)
2. Configura tu archivo `.env`
3. Prueba la configuración:

```bash
python test_email.py
```

## 🗂️ Estructura del Proyecto

```
MyWebsite/
├── app_login/          # Sistema de autenticación
├── app_products/       # Gestión de productos
├── app_cart/          # Carrito de compras
├── app_orders/        # Sistema de pedidos
├── app_website/       # Páginas principales
├── Zultech_main/      # Configuración principal
├── static/            # Archivos estáticos
├── media/             # Archivos multimedia
├── templates/         # Plantillas base
├── .env              # Variables de entorno (no en git)
├── .env.example      # Plantilla de variables de entorno
└── requirements.txt   # Dependencias
```

## 👥 Tipos de Usuario

### Cliente (Customer)
- Navegar productos
- Agregar al carrito
- Realizar pedidos
- Gestionar perfil

### Administrador (Admin)
- Todo lo del cliente +
- Gestionar productos
- Gestionar pedidos
- Gestionar usuarios
- Acceso al panel de administración

## 🔐 Seguridad

- Tokens CSRF habilitados
- Contraseñas hasheadas
- Variables de entorno para datos sensibles
- Validación de formularios
- Protección contra inyección SQL (ORM Django)

## 📦 Deployment en Render

El proyecto está configurado para deployment en Render con PostgreSQL.

1. Crea una cuenta en Render.com
2. Crea un nuevo Web Service
3. Conecta tu repositorio de GitHub
4. Render detectará automáticamente `build.sh` y `requirements.txt`
5. Configura las variables de entorno en el panel de Render

Variables requeridas en producción:
- `DATABASE_URL` (automática)
- `SECRET_KEY`
- `EMAIL_BACKEND=smtp` (si quieres envío real)
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`

## 🧪 Testing

```bash
python manage.py test
```

## 📝 Comandos Útiles

```bash
# Verificar instalación
python manage.py check

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Recolectar archivos estáticos
python manage.py collectstatic

# Crear superusuario
python manage.py createsuperuser

# Probar configuración de email
python test_email.py
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es privado y pertenece a Zultech.

## 👨‍💻 Autor

**BigBossSpektrum**
- GitHub: [@BigBossSpektrum](https://github.com/BigBossSpektrum)

## 📞 Soporte

Si tienes problemas:
1. Revisa [EMAIL_CONFIG.md](EMAIL_CONFIG.md) para problemas con emails
2. Abre un issue en GitHub
3. Contacta al equipo de desarrollo

---

⭐ Si te gusta este proyecto, no olvides darle una estrella!
