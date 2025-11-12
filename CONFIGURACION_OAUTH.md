# Configuración de OAuth con Google y Facebook

Este documento explica cómo configurar el inicio de sesión con Google y Facebook en Zultech.

## 🚀 Características Implementadas

- ✅ Inicio de sesión con Google
- ✅ Inicio de sesión con Facebook
- ✅ Creación automática de cuentas si no existen
- ✅ Conexión de cuentas sociales con usuarios existentes (por email)
- ✅ Asignación automática de rol CUSTOMER a usuarios de cuentas sociales

## 📋 Requisitos Previos

1. **Cuenta de Google Developer Console** (para Google OAuth)
2. **Cuenta de Facebook Developer** (para Facebook OAuth)
3. **Django-allauth instalado** (ya incluido en requirements.txt)

## 🔧 Configuración de Google OAuth

### 1. Crear un Proyecto en Google Cloud Console

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Navega a **APIs & Services** > **Credentials**

### 2. Configurar Pantalla de Consentimiento OAuth

1. Ve a **OAuth consent screen**
2. Selecciona **External** (para usuarios fuera de tu organización)
3. Completa los campos obligatorios:
   - **App name**: Zultech
   - **User support email**: tu email
   - **Developer contact information**: tu email
4. Guarda y continúa

### 3. Crear Credenciales OAuth 2.0

1. Ve a **Credentials** > **Create Credentials** > **OAuth 2.0 Client ID**
2. Selecciona **Web application**
3. Configura:
   - **Name**: Zultech Web Client
   - **Authorized JavaScript origins**:
     - `http://localhost:8000` (desarrollo)
     - `https://tu-dominio.com` (producción)
   - **Authorized redirect URIs**:
     - `http://localhost:8000/accounts/google/login/callback/` (desarrollo)
     - `https://tu-dominio.com/accounts/google/login/callback/` (producción)
4. Guarda y copia el **Client ID** y **Client Secret**

### 4. Configurar en Django

#### Opción A: Variables de Entorno (Recomendado)

Crea un archivo `.env` en la raíz del proyecto:

```bash
GOOGLE_CLIENT_ID=tu-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=tu-client-secret
```

#### Opción B: Django Admin

1. Accede al admin de Django: `http://localhost:8000/admin/`
2. Ve a **Sites** > **Sites**
3. Edita el sitio existente o crea uno nuevo:
   - **Domain name**: `localhost:8000` (desarrollo) o `tu-dominio.com` (producción)
   - **Display name**: Zultech
4. Ve a **Social applications** (bajo SOCIAL ACCOUNTS)
5. Haz clic en **Add Social application**
6. Completa:
   - **Provider**: Google
   - **Name**: Google OAuth
   - **Client id**: pega tu Client ID
   - **Secret key**: pega tu Client Secret
   - **Sites**: selecciona el sitio que creaste
7. Guarda

## 🔧 Configuración de Facebook OAuth

### 1. Crear una App en Facebook Developers

1. Ve a [Facebook Developers](https://developers.facebook.com/)
2. Haz clic en **My Apps** > **Create App**
3. Selecciona **Consumer** como tipo de app
4. Completa:
   - **App name**: Zultech
   - **App contact email**: tu email
5. Crea la app

### 2. Configurar Facebook Login

1. En el dashboard de tu app, ve a **Products** > **Facebook Login** > **Settings**
2. Configura:
   - **Valid OAuth Redirect URIs**:
     - `http://localhost:8000/accounts/facebook/login/callback/` (desarrollo)
     - `https://tu-dominio.com/accounts/facebook/login/callback/` (producción)
3. Guarda los cambios

### 3. Obtener Credenciales

1. Ve a **Settings** > **Basic**
2. Copia:
   - **App ID** (Client ID)
   - **App Secret** (Client Secret) - haz clic en "Show"

### 4. Configurar en Django

#### Opción A: Variables de Entorno (Recomendado)

Agrega al archivo `.env`:

```bash
FACEBOOK_APP_ID=tu-app-id
FACEBOOK_APP_SECRET=tu-app-secret
```

#### Opción B: Django Admin

1. Accede al admin: `http://localhost:8000/admin/`
2. Ve a **Social applications**
3. Haz clic en **Add Social application**
4. Completa:
   - **Provider**: Facebook
   - **Name**: Facebook OAuth
   - **Client id**: pega tu App ID
   - **Secret key**: pega tu App Secret
   - **Sites**: selecciona el sitio configurado
5. Guarda

## 🔒 Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con:

```bash
# Google OAuth
GOOGLE_CLIENT_ID=tu-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=tu-google-client-secret

# Facebook OAuth
FACEBOOK_APP_ID=tu-facebook-app-id
FACEBOOK_APP_SECRET=tu-facebook-app-secret

# Django Settings
SECRET_KEY=tu-secret-key-de-django
DEBUG=True
```

**Importante**: Agrega `.env` a tu `.gitignore` para no subir las credenciales al repositorio.

## 🧪 Probar la Configuración

1. Inicia el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

2. Ve a: `http://localhost:8000/accounts/login/`

3. Haz clic en **Continuar con Google** o **Continuar con Facebook**

4. Completa el flujo de autenticación

5. Deberías ser redirigido al dashboard según tu rol

## 📝 Comportamiento del Sistema

### Creación Automática de Cuentas

Cuando un usuario inicia sesión con Google o Facebook:

1. **Si el usuario NO existe**:
   - Se crea automáticamente una nueva cuenta
   - Se asigna el rol `CUSTOMER` por defecto
   - Se extraen datos de la cuenta social (nombre, email, etc.)
   - Se genera un username único basado en el email

2. **Si el usuario YA existe** (mismo email):
   - Se conecta la cuenta social al usuario existente
   - El usuario puede usar tanto login tradicional como social
   - Se mantiene el rol y datos existentes

### Redirección Según Rol

- **ADMIN**: `/accounts/admin/dashboard/`
- **CUSTOMER**: `/accounts/customer/dashboard/`

## 🔧 Configuración Avanzada

### Personalizar Campos Extraídos

Edita `app_login/adapters.py` en el método `save_user()` para personalizar qué datos se guardan de las cuentas sociales.

### Cambiar Redirección Post-Login

Edita `app_login/adapters.py` en el método `get_login_redirect_url()` para cambiar a dónde se redirige después del login social.

## ⚠️ Troubleshooting

### Error: "redirect_uri_mismatch"

**Solución**: Verifica que las URIs de redirección en Google/Facebook coincidan EXACTAMENTE con:
- `http://localhost:8000/accounts/google/login/callback/`
- `http://localhost:8000/accounts/facebook/login/callback/`

### Error: "Site matching query does not exist"

**Solución**: 
1. Ve al admin de Django
2. Crea o edita un Site con el dominio correcto
3. Asigna ese Site a la Social Application

### Error: "No module named 'allauth'"

**Solución**: Instala las dependencias:
```bash
pip install -r requirements.txt
```

### Los botones no aparecen

**Solución**: Verifica que el template cargue el tag:
```html
{% load socialaccount %}
```

## 📚 Referencias

- [Django-allauth Documentation](https://django-allauth.readthedocs.io/)
- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Facebook Login Documentation](https://developers.facebook.com/docs/facebook-login)

## 🚀 Deploy a Producción

### 1. Actualizar URLs Permitidas

En `settings.py`, agrega tu dominio de producción a:
```python
ALLOWED_HOSTS = ['mywebsite-tlxs.onrender.com', 'tu-dominio.com']
```

### 2. Actualizar Redirect URIs

En Google y Facebook, actualiza las redirect URIs con tu dominio de producción:
- `https://tu-dominio.com/accounts/google/login/callback/`
- `https://tu-dominio.com/accounts/facebook/login/callback/`

### 3. Variables de Entorno en Producción

Configura las variables de entorno en tu plataforma de hosting (Render, Heroku, etc.):
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `FACEBOOK_APP_ID`
- `FACEBOOK_APP_SECRET`

### 4. Actualizar Site en Django Admin

En producción, actualiza el Site con tu dominio real en el admin de Django.

---

**¡Listo!** Ahora tu aplicación soporta login con Google y Facebook con creación automática de cuentas.
