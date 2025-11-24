# Guía de Despliegue en Render

Esta guía te ayudará a desplegar tu aplicación Django en Render.com.

## 🚀 Cambios Realizados

Se han realizado las siguientes modificaciones para hacer el proyecto compatible con Render:

### 1. **build.sh** - Script de construcción mejorado
- Instala dependencias
- Ejecuta collectstatic
- Ejecuta migraciones de base de datos
- **NUEVO**: Crea automáticamente el objeto Site requerido por django-allauth

### 2. **render.yaml** - Configuración de Render actualizada
- Base de datos PostgreSQL configurada
- Variables de entorno para OAuth (Google, GitHub, Facebook)
- Variables de entorno para email
- Configuración de SECRET_KEY automática

### 3. **settings.py** - Configuración de producción mejorada
- Detección automática de entorno Render
- Configuración de seguridad HTTPS para producción
- CSRF_TRUSTED_ORIGINS configurado
- Mejoras en ALLOWED_HOSTS

### 4. **Management Command** - `setup_site.py`
- Comando personalizado para crear/actualizar el Site de django.contrib.sites
- Se ejecuta automáticamente en cada despliegue

## 📋 Pre-requisitos

1. Cuenta en [Render.com](https://render.com)
2. Repositorio Git con tu código (GitHub, GitLab, o Bitbucket)
3. Credenciales OAuth configuradas (opcional)

## 🔧 Pasos para Desplegar

### Paso 1: Preparar el Repositorio

1. Asegúrate de que todos los cambios estén commiteados:
```bash
git add .
git commit -m "Configuración para despliegue en Render"
git push origin main
```

### Paso 2: Crear el Servicio en Render

1. Ve a [render.com](https://render.com) e inicia sesión
2. Click en "New +" y selecciona "Blueprint"
3. Conecta tu repositorio de GitHub
4. Render detectará automáticamente el archivo `render.yaml`
5. Click en "Apply"

### Paso 3: Configurar Variables de Entorno

Render creará automáticamente las siguientes variables (las puedes modificar en el Dashboard):

#### Variables Obligatorias (auto-generadas)
- `DATABASE_URL` - ✅ Auto-configurada por Render
- `SECRET_KEY` - ✅ Auto-generada por Render
- `DEBUG` - ✅ Configurada como `False`

#### Variables OAuth (Configurar manualmente)

Ve a tu servicio en Render Dashboard → Environment y añade:

**Google OAuth:**
```
OAUTH_GOOGLE_ID=tu-google-client-id.apps.googleusercontent.com
OAUTH_GOOGLE_SECRET=tu-google-secret
```

**GitHub OAuth:**
```
OAUTH_GITHUB_ID=tu-github-client-id
OAUTH_GITHUB_SECRET=tu-github-secret
```

**Facebook OAuth:**
```
OAUTH_FACEBOOK_ID=tu-facebook-app-id
OAUTH_FACEBOOK_SECRET=tu-facebook-app-secret
```

#### Configuración de Email (Opcional)
```
EMAIL_BACKEND=smtp  # o 'console' para desarrollo
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@outlook.com
EMAIL_HOST_PASSWORD=tu-password
DEFAULT_FROM_EMAIL=noreply@zultech.com
```

### Paso 4: Configurar OAuth Providers

Para que OAuth funcione en producción, necesitas actualizar las URLs de callback:

#### Google OAuth
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Selecciona tu proyecto
3. Ve a "Credentials" → Edita tu OAuth Client ID
4. Añade a "Authorized redirect URIs":
   ```
   https://mywebsite-tlxs.onrender.com/accounts/google/login/callback/
   ```

#### GitHub OAuth
1. Ve a [GitHub Developer Settings](https://github.com/settings/developers)
2. Edita tu OAuth App
3. Actualiza "Authorization callback URL":
   ```
   https://mywebsite-tlxs.onrender.com/accounts/github/login/callback/
   ```

#### Facebook OAuth
1. Ve a [Facebook Developers](https://developers.facebook.com/)
2. Edita tu app
3. Ve a "Facebook Login" → Settings
4. Añade a "Valid OAuth Redirect URIs":
   ```
   https://mywebsite-tlxs.onrender.com/accounts/facebook/login/callback/
   ```

### Paso 5: Verificar el Despliegue

1. Espera a que el build termine (5-10 minutos)
2. Render te dará una URL: `https://mywebsite-tlxs.onrender.com`
3. Visita tu sitio y verifica que funcione

## 🐛 Solución de Problemas

### Error: "no such table: django_site"
✅ **Solucionado** - El comando `setup_site` ahora se ejecuta automáticamente

### Error: "CSRF verification failed"
- Verifica que `CSRF_TRUSTED_ORIGINS` incluya tu dominio de Render
- Asegúrate de usar HTTPS en producción

### Error: OAuth "redirect_uri_mismatch"
- Verifica que las URLs de callback coincidan exactamente
- Deben incluir el protocolo HTTPS
- No deben tener espacios o caracteres adicionales

### La base de datos no tiene datos
Esto es normal en el primer despliegue. Puedes:
1. Crear un superusuario via Render Shell:
```bash
python manage.py createsuperuser
```
2. Importar datos existentes si los tienes

### Error de conexión a la base de datos
- Verifica que el servicio de base de datos esté activo
- Comprueba que `DATABASE_URL` esté configurado correctamente

## 🔄 Re-despliegues

Render re-desplegará automáticamente cuando:
- Hagas push a tu rama principal
- Cambies variables de entorno
- Actualices el archivo `render.yaml`

## 📊 Monitoreo

En el Dashboard de Render puedes:
- Ver logs en tiempo real
- Monitorear uso de recursos
- Configurar alertas
- Ver métricas de rendimiento

## 🔐 Seguridad en Producción

Las siguientes configuraciones de seguridad están activas cuando `DEBUG=False`:

- ✅ HTTPS obligatorio (`SECURE_SSL_REDIRECT`)
- ✅ Cookies seguras (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`)
- ✅ Protección XSS (`SECURE_BROWSER_XSS_FILTER`)
- ✅ Protección MIME (`SECURE_CONTENT_TYPE_NOSNIFF`)
- ✅ X-Frame-Options configurado

## 📝 Comandos Útiles

### Acceder a Shell de Render
```bash
# Via Render Dashboard → Shell tab
python manage.py shell
```

### Ver logs
```bash
# Via Render Dashboard → Logs tab
# O usando Render CLI
render logs
```

### Ejecutar migraciones manualmente
```bash
# Via Render Dashboard → Shell tab
python manage.py migrate
```

### Crear superusuario
```bash
# Via Render Dashboard → Shell tab
python manage.py createsuperuser
```

## 🆘 Soporte

Si encuentras problemas:
1. Revisa los logs en Render Dashboard
2. Verifica las variables de entorno
3. Consulta la [documentación de Render](https://render.com/docs)
4. Revisa este archivo para soluciones comunes

## ✅ Checklist de Despliegue

- [ ] Código pusheado a GitHub
- [ ] Servicio creado en Render desde Blueprint
- [ ] Variables de entorno OAuth configuradas
- [ ] URLs de callback OAuth actualizadas en providers
- [ ] Build completado sin errores
- [ ] Sitio accesible via HTTPS
- [ ] Login manual funciona
- [ ] OAuth providers funcionan (si configurados)
- [ ] Archivos estáticos se cargan correctamente
- [ ] Base de datos con migraciones aplicadas

---

**¡Felicidades!** 🎉 Tu aplicación Django ahora está desplegada en Render.
