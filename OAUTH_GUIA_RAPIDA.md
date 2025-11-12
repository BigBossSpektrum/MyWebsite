# 🚀 Inicio de Sesión con Google y Facebook - Guía Rápida

## ✅ ¿Qué se ha implementado?

Se ha agregado la funcionalidad completa de inicio de sesión con Google y Facebook a tu aplicación Zultech.

### Características principales:

1. **Botones de inicio de sesión social** en la página de login
2. **Creación automática de cuentas** si el usuario no existe
3. **Conexión de cuentas sociales** con usuarios existentes (basado en email)
4. **Asignación automática de rol CUSTOMER** para nuevos usuarios de cuentas sociales
5. **Redirección inteligente** según el rol del usuario (admin/customer)

## 📁 Archivos modificados/creados:

- ✅ `requirements.txt` - Agregado django-allauth y dependencias
- ✅ `Zultech_main/settings.py` - Configuración de allauth y providers
- ✅ `Zultech_main/urls.py` - URLs de allauth
- ✅ `app_login/adapters.py` - **NUEVO**: Lógica personalizada para cuentas sociales
- ✅ `app_login/templates/login.html` - Botones de Google y Facebook
- ✅ `static/css/login.css` - Estilos para botones sociales
- ✅ `CONFIGURACION_OAUTH.md` - **NUEVO**: Documentación completa

## 🔧 Próximos pasos para hacerlo funcionar:

### 1. Instalar dependencias (si no lo has hecho):

```bash
pip install -r requirements.txt
```

### 2. Aplicar migraciones (ya hecho):

```bash
python manage.py migrate
```

### 3. Configurar Google OAuth:

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un proyecto y configura OAuth 2.0
3. Obtén **Client ID** y **Client Secret**
4. Configura las redirect URIs:
   - `http://localhost:8000/accounts/google/login/callback/`

### 4. Configurar Facebook OAuth:

1. Ve a [Facebook Developers](https://developers.facebook.com/)
2. Crea una app y habilita Facebook Login
3. Obtén **App ID** y **App Secret**
4. Configura las redirect URIs:
   - `http://localhost:8000/accounts/facebook/login/callback/`

### 5. Configurar en Django Admin:

1. Inicia el servidor: `python manage.py runserver`
2. Ve a: `http://localhost:8000/admin/`
3. Crea un superusuario si no tienes: `python manage.py createsuperuser`
4. En **Sites**, crea o edita el site con dominio `localhost:8000`
5. En **Social applications**, agrega:
   - **Google**: Con Client ID y Secret
   - **Facebook**: Con App ID y App Secret
6. Asigna el site creado a cada aplicación social

### Alternativamente, usa variables de entorno:

Crea un archivo `.env`:

```bash
GOOGLE_CLIENT_ID=tu-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=tu-client-secret
FACEBOOK_APP_ID=tu-app-id
FACEBOOK_APP_SECRET=tu-app-secret
```

## 🎯 ¿Cómo funciona?

### Para usuarios nuevos:

1. Usuario hace clic en "Continuar con Google" o "Continuar con Facebook"
2. Se autentica con el proveedor (Google/Facebook)
3. **Se crea automáticamente una cuenta** con:
   - Email de la cuenta social
   - Nombre extraído de la cuenta social
   - Username generado automáticamente (único)
   - Rol: `CUSTOMER` por defecto
4. Usuario es redirigido al dashboard de customer

### Para usuarios existentes:

1. Si el email de la cuenta social coincide con un usuario existente:
   - **Se conecta la cuenta social al usuario**
   - El usuario puede usar tanto login tradicional como social
   - Mantiene su rol y datos existentes
2. Usuario es redirigido según su rol (admin o customer)

## 🔒 Seguridad

- Las credenciales de OAuth se pueden guardar en variables de entorno (recomendado para producción)
- Las cuentas sociales requieren email verificado
- Los tokens de acceso son manejados por django-allauth de forma segura

## 📖 Documentación completa

Para más detalles, configuración avanzada y troubleshooting, consulta:

👉 **[CONFIGURACION_OAUTH.md](./CONFIGURACION_OAUTH.md)**

## 🧪 Prueba rápida

1. Inicia el servidor: `python manage.py runserver`
2. Ve a: `http://localhost:8000/accounts/login/`
3. Verás los botones de Google y Facebook
4. **Nota**: Para que funcionen, necesitas configurar las credenciales (paso 3-5 arriba)

## ❓ Preguntas frecuentes

**P: ¿Dónde están los botones de login social?**  
R: En la página de login: `/accounts/login/` debajo del formulario tradicional.

**P: ¿Funciona en producción?**  
R: Sí, solo necesitas actualizar las redirect URIs en Google/Facebook con tu dominio real.

**P: ¿Puedo desactivar un proveedor?**  
R: Sí, elimina el provider de `INSTALLED_APPS` en `settings.py`.

**P: ¿Los usuarios pueden tener múltiples cuentas sociales?**  
R: Sí, un usuario puede conectar tanto Google como Facebook a la misma cuenta.

---

**¡Todo listo!** Solo falta configurar las credenciales de Google y Facebook para empezar a usar el login social.
