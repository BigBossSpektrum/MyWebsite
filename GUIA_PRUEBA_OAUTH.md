# Guía de Prueba - OAuth Configuración Interna

## ✅ Configuración Completada

Tu aplicación ahora usa **configuración interna** de OAuth. Ya no necesitas configurar nada en el admin de Django.

## 🧪 Cómo Probar

### 1. **Accede a la página de login**
```
http://127.0.0.1:8000/accounts/login/
```

### 2. **Verás los botones de login social**
- 🔵 "Login con Google"
- 🟣 "Login con GitHub"

### 3. **Haz clic en cualquiera de los botones**
- Se abrirá una ventana de autorización del proveedor
- Autoriza el acceso
- Serás redirigido automáticamente a tu dashboard

## 🔍 Verificar que Funciona

### ✓ Creación Automática de Usuarios
Los usuarios se crean automáticamente sin necesidad de registro previo:
- **Username**: Se genera desde el email o login del proveedor
- **Email**: Se obtiene del proveedor OAuth
- **Foto de perfil**: Se descarga automáticamente (Google)
- **Rol**: Se asigna `CUSTOMER` por defecto

### ✓ Sin Configuración en Admin
Ya NO necesitas:
- Ir a `/admin/socialaccount/socialapp/`
- Crear entradas en la base de datos
- Configurar `Site` o `SocialApp`

Todo está en el código (`settings.py`) y las credenciales en `.env`.

## 📋 Checklist de Verificación

- [ ] El servidor está corriendo en `http://127.0.0.1:8000`
- [ ] Puedes ver la página de login
- [ ] Los botones de OAuth aparecen
- [ ] Al hacer clic en Google/GitHub, se abre la ventana de autorización
- [ ] Después de autorizar, vuelves a la aplicación
- [ ] Se crea un nuevo usuario automáticamente
- [ ] Eres redirigido al dashboard

## 🐛 Troubleshooting

### Error: "redirect_uri_mismatch" (Google)
**Causa**: La URL de callback no está configurada en Google Cloud Console

**Solución**:
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Selecciona tu proyecto
3. Ve a "Credenciales" > "OAuth 2.0 Client IDs"
4. Edita tu Client ID
5. En "URIs de redireccionamiento autorizados", agrega:
   ```
   http://localhost:8000/accounts/google/login/callback/
   http://127.0.0.1:8000/accounts/google/login/callback/
   ```

### Error: "Authorization callback error" (GitHub)
**Causa**: La URL de callback no está configurada en GitHub

**Solución**:
1. Ve a [GitHub Developer Settings](https://github.com/settings/developers)
2. Selecciona tu OAuth App
3. En "Authorization callback URL", configura:
   ```
   http://localhost:8000/accounts/github/login/callback/
   ```

### Error: "SocialApp matching query does not exist"
**Causa**: Estás intentando usar la configuración de base de datos

**Solución**: Ya no necesitas `SocialApp` en el admin. La configuración es interna.

### Login no redirige correctamente
**Causa**: Configuración de redirección incorrecta

**Solución**: Verifica en `settings.py`:
```python
LOGIN_REDIRECT_URL = 'website:Dashboard'
```

## 📸 Captura de Pantalla de Ejemplo

Cuando hagas login con OAuth, verás algo como:

```
✓ Usuario creado: john_doe
✓ Email: john.doe@gmail.com
✓ Proveedor: Google
✓ Foto de perfil descargada
✓ Redirigiendo al dashboard...
```

## 🔄 Flujo Completo

```
Usuario → Click "Login con Google"
         ↓
Google OAuth → Usuario autoriza
         ↓
Callback → /accounts/google/login/callback/
         ↓
Django-allauth → Lee config de settings.py
         ↓
CustomSocialAccountAdapter → Crea usuario automáticamente
         ↓
Dashboard → Usuario logueado
```

## 📝 Logs de Depuración

Si quieres ver los logs detallados, verifica la consola del servidor:
```bash
source env/Scripts/activate
python manage.py runserver
```

Verás algo como:
```
=== IS_AUTO_SIGNUP_ALLOWED ===
Provider: google
Extra data: {'email': 'john@gmail.com', ...}
Result from super: True
Forcing True

=== POPULATE_USER ===
Data recibida: {'email': 'john@gmail.com', ...}
Email procesado: john@gmail.com
Base username: john
Username final: john

✓ Usuario base creado: john
```

## 🎯 Próximos Pasos

1. ✅ **Desarrollo Local**: Ya funciona con `http://localhost:8000`
2. 🚀 **Producción**: Configura las URLs de callback en producción:
   ```
   https://mywebsite-tlxs.onrender.com/accounts/google/login/callback/
   https://mywebsite-tlxs.onrender.com/accounts/github/login/callback/
   ```
3. 🔒 **Seguridad**: Asegúrate de que las variables de entorno estén configuradas en Render
4. 📊 **Monitoreo**: Revisa los logs de producción para verificar que OAuth funciona

## ✨ Ventajas de Esta Configuración

1. **Sin Admin**: No necesitas tocar el admin de Django
2. **Portable**: Fácil de mover entre entornos (dev, staging, prod)
3. **Control de Versiones**: La configuración está en el código
4. **Seguridad**: Las credenciales están en `.env`, no en la base de datos
5. **Simple**: Una sola fuente de verdad

## 📚 Archivos Importantes

- `settings.py`: Configuración de OAuth
- `.env`: Credenciales (no versionar)
- `app_login/adapters.py`: Lógica de creación de usuarios
- `verify_internal_oauth_config.py`: Script de verificación

## 🎉 ¡Listo!

Tu aplicación ahora usa configuración interna de OAuth. Ya puedes probar el login con Google y GitHub sin necesidad de configurar nada en el admin.

**¿Necesitas ayuda?** Ejecuta:
```bash
python verify_internal_oauth_config.py
```
