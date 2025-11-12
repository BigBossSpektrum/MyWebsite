# Configuración de Email para Zultech

## 📧 Configuración Inicial

Este proyecto usa variables de entorno para configurar el envío de emails. Hay dos modos:

### 1. Modo Desarrollo (Console Backend)
Los emails se muestran en la terminal, no se envían realmente.

```env
EMAIL_BACKEND=console
```

### 2. Modo Producción (SMTP Backend)
Los emails se envían por SMTP usando un servidor de correo real.

```env
EMAIL_BACKEND=smtp
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-contraseña-de-aplicacion
DEFAULT_FROM_EMAIL=noreply@zultech.com
```

---

## 🔧 Configuración por Proveedor

### Gmail (Recomendado para desarrollo)

1. **Habilita la verificación en dos pasos:**
   - Ve a https://myaccount.google.com/
   - Seguridad → Verificación en dos pasos
   - Sigue los pasos para activarla

2. **Crea una contraseña de aplicación:**
   - Ve a https://myaccount.google.com/apppasswords
   - Selecciona "Correo" y "Otro dispositivo personalizado"
   - Escribe "Zultech Django"
   - Copia la contraseña de 16 caracteres

3. **Configura tu `.env`:**
   ```env
   EMAIL_BACKEND=smtp
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=tu-correo@gmail.com
   EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
   DEFAULT_FROM_EMAIL=noreply@zultech.com
   ```

### Outlook / Hotmail

```env
EMAIL_BACKEND=smtp
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-correo@outlook.com
EMAIL_HOST_PASSWORD=tu-contraseña
DEFAULT_FROM_EMAIL=noreply@zultech.com
```

### Yahoo Mail

```env
EMAIL_BACKEND=smtp
EMAIL_HOST=smtp.mail.yahoo.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-correo@yahoo.com
EMAIL_HOST_PASSWORD=tu-contraseña-de-aplicacion
DEFAULT_FROM_EMAIL=noreply@zultech.com
```

**Nota:** Yahoo también requiere contraseñas de aplicación.

### SendGrid (Recomendado para producción)

1. Crea una cuenta en https://sendgrid.com/
2. Crea una API Key
3. Configura:

```env
EMAIL_BACKEND=smtp
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=tu-api-key-aqui
DEFAULT_FROM_EMAIL=noreply@tudominio.com
```

### Mailgun

1. Crea una cuenta en https://www.mailgun.com/
2. Verifica tu dominio
3. Obtén tus credenciales SMTP

```env
EMAIL_BACKEND=smtp
EMAIL_HOST=smtp.mailgun.org
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=postmaster@tu-dominio.mailgun.org
EMAIL_HOST_PASSWORD=tu-contraseña-mailgun
DEFAULT_FROM_EMAIL=noreply@tudominio.com
```

---

## 📝 Uso en el Código

El sistema de email ya está configurado para:

- ✅ Recuperación de contraseñas
- ✅ Emails de confirmación
- ✅ Notificaciones de pedidos (próximamente)
- ✅ Soporte al cliente (próximamente)

No necesitas cambiar nada en el código, solo configura el archivo `.env`.

---

## 🧪 Probar la Configuración

### En desarrollo (console):
Los emails aparecerán en la terminal donde ejecutas `python manage.py runserver`.

### En producción (smtp):
Para probar que funciona:

1. Ve a http://localhost:8000/accounts/password-reset/
2. Ingresa un email registrado
3. Revisa la bandeja de entrada (o spam)

---

## ⚠️ Solución de Problemas

### Error: "SMTPAuthenticationError"
- Verifica que el email y contraseña sean correctos
- Para Gmail: asegúrate de usar una contraseña de aplicación, no tu contraseña normal
- Verifica que la verificación en dos pasos esté activa (Gmail)

### Error: "SMTPServerDisconnected"
- Verifica el EMAIL_HOST y EMAIL_PORT
- Asegúrate de que EMAIL_USE_TLS=True

### Los emails no llegan
- Revisa la carpeta de spam
- Verifica que DEFAULT_FROM_EMAIL sea válido
- Para Gmail: asegúrate de que "Acceso de aplicaciones menos seguras" NO esté bloqueado

### Error: "SMTPRecipientsRefused"
- Verifica que el email del destinatario sea válido
- Algunos proveedores limitan a quién puedes enviar emails (ej: SendGrid en modo sandbox)

---

## 🔐 Seguridad

**IMPORTANTE:**
- ⛔ **NUNCA** subas el archivo `.env` a GitHub
- ⛔ **NUNCA** compartas tus contraseñas de aplicación
- ✅ Usa `.env.example` como plantilla
- ✅ El archivo `.env` ya está en `.gitignore`

---

## 📦 Instalación de Dependencias

El proyecto ya incluye `python-dotenv` en `requirements.txt`. Para instalar:

```bash
source env/bin/activate
pip install -r requirements.txt
```

---

## 🚀 Configuración en Render/Heroku

En producción, configura las variables de entorno en el panel de control:

**Render:**
- Ve a tu servicio → Environment
- Agrega cada variable (EMAIL_HOST, EMAIL_PORT, etc.)

**Heroku:**
```bash
heroku config:set EMAIL_BACKEND=smtp
heroku config:set EMAIL_HOST=smtp.sendgrid.net
heroku config:set EMAIL_HOST_USER=apikey
heroku config:set EMAIL_HOST_PASSWORD=tu-api-key
# ... etc
```

---

## 📚 Referencias

- [Django Email Documentation](https://docs.djangoproject.com/en/5.2/topics/email/)
- [Gmail App Passwords](https://support.google.com/accounts/answer/185833)
- [SendGrid Django Integration](https://docs.sendgrid.com/for-developers/sending-email/django)
- [Mailgun Documentation](https://documentation.mailgun.com/en/latest/)
