# Configuración de Facebook OAuth

Esta guía te ayudará a configurar la autenticación con Facebook OAuth en tu aplicación Django.

## 📋 Requisitos Previos

- Cuenta de Facebook
- Aplicación web desplegada (local o en producción)

## 🚀 Paso 1: Crear una Aplicación en Facebook

1. **Ve a Facebook Developers**
   - Accede a [https://developers.facebook.com/](https://developers.facebook.com/)
   - Inicia sesión con tu cuenta de Facebook

2. **Crea una Nueva Aplicación**
   - Haz clic en "Mis aplicaciones" en la esquina superior derecha
   - Selecciona "Crear aplicación"
   - Elige el tipo "Consumer" (para login de usuarios)
   - Haz clic en "Siguiente"

3. **Configura los Detalles de la Aplicación**
   - **Nombre de la aplicación:** Zultech (o el nombre que prefieras)
   - **Correo electrónico de contacto:** Tu correo electrónico
   - Haz clic en "Crear aplicación"

## 🔑 Paso 2: Obtener Credenciales OAuth

1. **Ve a la Configuración de la Aplicación**
   - En el panel izquierdo, haz clic en "Configuración" > "Básica"
   
2. **Obtén tus Credenciales**
   - **App ID (Client ID):** Copia este valor
   - **App Secret (Client Secret):** Haz clic en "Mostrar" y copia este valor
   
   ⚠️ **IMPORTANTE:** Mantén el App Secret en secreto y nunca lo compartas públicamente

## 🔧 Paso 3: Configurar el Producto "Inicio de Sesión con Facebook"

1. **Agrega el Producto**
   - En el panel izquierdo, busca "Productos" o "Agregar producto"
   - Encuentra "Inicio de sesión con Facebook" (Facebook Login)
   - Haz clic en "Configurar"

2. **Configura las URLs de Redirección**
   - Ve a "Inicio de sesión con Facebook" > "Configuración"
   - En "URI de redireccionamiento de OAuth válidos", agrega:
     ```
     # Para desarrollo local:
     http://localhost:8000/accounts/facebook/login/callback/
     http://127.0.0.1:8000/accounts/facebook/login/callback/
     
     # Para producción (reemplaza con tu dominio):
     https://tudominio.com/accounts/facebook/login/callback/
     https://mywebsite-tlxs.onrender.com/accounts/facebook/login/callback/
     ```
   - Haz clic en "Guardar cambios"

## 📝 Paso 4: Configurar las Variables de Entorno

Agrega las credenciales de Facebook en tu archivo `.env`:

```env
# OAuth Facebook
OAUTH_FACEBOOK_ID=tu_app_id_aqui
OAUTH_FACEBOOK_SECRET=tu_app_secret_aqui
```

**Ejemplo:**
```env
OAUTH_FACEBOOK_ID=123456789012345
OAUTH_FACEBOOK_SECRET=abcdef1234567890abcdef1234567890
```

## 🌐 Paso 5: Configurar Dominios de la Aplicación

1. **Ve a Configuración Básica**
   - En el panel izquierdo, "Configuración" > "Básica"

2. **Agrega los Dominios**
   - En "Dominios de la aplicación", agrega:
     ```
     localhost
     tudominio.com
     mywebsite-tlxs.onrender.com
     ```

3. **Configura la URL de Política de Privacidad**
   - URL de la política de privacidad: `https://tudominio.com/privacy-policy`
   - URL de los Términos de servicio: `https://tudominio.com/terms-of-service`

## 🎯 Paso 6: Cambiar a Modo Producción

Para que tu aplicación funcione para usuarios reales (no solo desarrolladores):

1. **Completa la Verificación de la Aplicación**
   - Ve a "Revisión de aplicaciones"
   - Completa todos los requisitos necesarios
   - Solicita los permisos necesarios (email, public_profile)

2. **Activa el Modo Producción**
   - En la parte superior, hay un switch que dice "Desarrollo" o "En producción"
   - Cambia a "En producción" cuando estés listo

## 🧪 Paso 7: Probar la Configuración

1. **Reinicia tu servidor Django**
   ```bash
   python manage.py runserver
   ```

2. **Prueba el Login**
   - Ve a tu página de login: `http://localhost:8000/accounts/login/`
   - Haz clic en el botón de "Iniciar sesión con Facebook"
   - Deberías ser redirigido a Facebook para autorizar
   - Después de autorizar, serás redirigido de vuelta a tu aplicación

## 🔍 Verificación de la Configuración

Verifica que tu configuración en `settings.py` incluya:

```python
INSTALLED_APPS = [
    # ...
    'allauth.socialaccount.providers.facebook',
    # ...
]

SOCIALACCOUNT_PROVIDERS = {
    # ...
    'facebook': {
        'APP': {
            'client_id': os.environ.get('OAUTH_FACEBOOK_ID', ''),
            'secret': os.environ.get('OAUTH_FACEBOOK_SECRET', ''),
            'key': ''
        },
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
        ],
        'EXCHANGE_TOKEN': True,
        'VERIFIED_EMAIL': False,
        'VERSION': 'v18.0',
    },
}
```

## 📌 URIs de Redirección Importantes

Las URIs de redirección siguen este formato:
```
http[s]://[tu-dominio]/accounts/facebook/login/callback/
```

**Ejemplos:**
- Local: `http://localhost:8000/accounts/facebook/login/callback/`
- Producción: `https://mywebsite-tlxs.onrender.com/accounts/facebook/login/callback/`

## ⚠️ Problemas Comunes

### Error: "URL Blocked: This redirect failed because the redirect URI is not whitelisted"
- **Solución:** Asegúrate de que la URI de redirección esté agregada en "URI de redireccionamiento de OAuth válidos"

### Error: "App Not Setup: This app is still in development mode"
- **Solución:** Agrega tu cuenta de Facebook como tester en "Roles" > "Testers" o activa el modo producción

### Error: "Invalid OAuth access token"
- **Solución:** Verifica que el App ID y App Secret sean correctos en tu archivo `.env`

### El botón no funciona
- **Solución:** Asegúrate de que django-allauth esté instalado y que hayas ejecutado las migraciones:
  ```bash
  pip install django-allauth
  python manage.py migrate
  ```

## 📚 Recursos Adicionales

- [Documentación de Facebook Login](https://developers.facebook.com/docs/facebook-login/)
- [Documentación de django-allauth](https://docs.allauth.org/en/latest/socialaccount/providers/facebook.html)
- [Graph API Explorer](https://developers.facebook.com/tools/explorer/) - Para probar las APIs de Facebook

## 🎓 Permisos de Facebook

La configuración actual solicita:
- **email:** Acceso al correo electrónico del usuario
- **public_profile:** Información pública del perfil (nombre, foto, etc.)

Si necesitas permisos adicionales, agrégalos en el array `SCOPE` en `settings.py` y solicita la aprobación de Facebook en la revisión de la aplicación.

## ✅ Checklist de Configuración

- [ ] Cuenta de Facebook Developers creada
- [ ] Aplicación de Facebook creada
- [ ] App ID y App Secret copiados
- [ ] Producto "Inicio de sesión con Facebook" agregado
- [ ] URIs de redirección configuradas
- [ ] Dominios de aplicación agregados
- [ ] Variables de entorno configuradas en `.env`
- [ ] Servidor reiniciado
- [ ] Login probado exitosamente

---

¡Tu autenticación con Facebook está lista! 🎉
