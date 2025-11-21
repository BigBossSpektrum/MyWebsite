# 🔐 OAuth - Configuración Interna (Sin Admin)

## 📋 Resumen

Tu aplicación ahora usa **configuración interna** para OAuth de Google y GitHub. Las credenciales se configuran directamente en el código usando variables de entorno, **sin necesidad de usar el admin de Django**.

## ✅ Estado Actual

```
✓ Configuración interna activada
✓ Credenciales en variables de entorno (.env)
✓ Sin necesidad de admin (/admin/socialaccount/socialapp/)
✓ django.contrib.sites removido
✓ SITE_ID removido
✓ Proveedores: Google ✓ | GitHub ✓
```

## 🎯 Ventajas

| Característica | Antes (Admin) | Ahora (Interna) |
|---------------|---------------|-----------------|
| **Configuración** | Admin de Django | settings.py |
| **Credenciales** | Base de datos | Variables de entorno |
| **Portabilidad** | ❌ Difícil | ✅ Fácil |
| **Control de versiones** | ❌ No | ✅ Sí (sin credenciales) |
| **Seguridad** | ⚠️ Media | ✅ Alta |
| **Simplicidad** | ❌ Compleja | ✅ Simple |

## 🔧 Archivos Modificados

### 1. `settings.py`

```python
# Configuración interna de proveedores OAuth
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.environ.get('OAUTH_GOOGLE_ID', ''),
            'secret': os.environ.get('OAUTH_GOOGLE_SECRET', ''),
            'key': ''
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    },
    'github': {
        'APP': {
            'client_id': os.environ.get('OAUTH_GITHUB_ID', ''),
            'secret': os.environ.get('OAUTH_GITHUB_SECRET', ''),
            'key': ''
        },
        'SCOPE': ['user', 'user:email'],
    },
}
```

### 2. `.env`

```env
OAUTH_GOOGLE_ID=tu-google-client-id
OAUTH_GOOGLE_SECRET=tu-google-secret
OAUTH_GITHUB_ID=tu-github-client-id
OAUTH_GITHUB_SECRET=tu-github-secret
```

### 3. `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    # ... otras apps
    # django.contrib.sites REMOVIDO ❌
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    # ... tus apps
]
```

## 🚀 Cómo Usar

### Desarrollo Local

1. **Asegúrate de que el servidor esté corriendo**:
   ```bash
   source env/Scripts/activate
   python manage.py runserver
   ```

2. **Accede a la página de login**:
   ```
   http://127.0.0.1:8000/accounts/login/
   ```

3. **Haz clic en "Login con Google" o "Login con GitHub"**

4. **Autoriza el acceso**

5. **Serás redirigido automáticamente al dashboard**

### Producción (Render)

1. **Configura las variables de entorno en Render**:
   - `OAUTH_GOOGLE_ID`
   - `OAUTH_GOOGLE_SECRET`
   - `OAUTH_GITHUB_ID`
   - `OAUTH_GITHUB_SECRET`

2. **Configura las URLs de callback en los proveedores**:
   - Google: `https://mywebsite-tlxs.onrender.com/accounts/google/login/callback/`
   - GitHub: `https://mywebsite-tlxs.onrender.com/accounts/github/login/callback/`

3. **Despliega tu aplicación**

## 🧪 Scripts de Verificación

### 1. Verificar Configuración

```bash
python verify_internal_oauth_config.py
```

**Muestra**:
- ✓ Proveedores configurados
- ✓ Credenciales completas
- ✓ Variables de entorno
- ✓ URLs de callback

### 2. Limpiar Configuración Antigua (Opcional)

```bash
python clean_old_oauth_config.py
```

**Elimina**:
- Registros de `SocialApp` en la base de datos
- Ya no son necesarios con configuración interna

## 📝 Checklist de Migración

- [x] Removido `django.contrib.sites` de `INSTALLED_APPS`
- [x] Removido `SITE_ID = 1`
- [x] Agregada configuración `APP` en `SOCIALACCOUNT_PROVIDERS`
- [x] Credenciales movidas a variables de entorno (`.env`)
- [x] Configuraciones deprecadas actualizadas
- [x] Verificación exitosa (`python manage.py check`)
- [ ] Prueba de login con Google
- [ ] Prueba de login con GitHub
- [ ] Configuración en producción (Render)

## 🔍 Troubleshooting

### Error: "SocialApp matching query does not exist"

**Causa**: Estás intentando usar la configuración de base de datos.

**Solución**: Ya no necesitas `SocialApp` en el admin. Usa configuración interna.

### Error: "Invalid client_id" o "Unauthorized"

**Causa**: Variables de entorno incorrectas.

**Solución**: 
1. Verifica que `.env` tenga las credenciales correctas
2. Ejecuta `python verify_internal_oauth_config.py`
3. Reinicia el servidor

### Error: "redirect_uri_mismatch"

**Causa**: URL de callback no configurada en el proveedor OAuth.

**Solución**:
- **Google**: Agrega `http://localhost:8000/accounts/google/login/callback/` en Google Cloud Console
- **GitHub**: Agrega `http://localhost:8000/accounts/github/login/callback/` en GitHub OAuth Apps

### Login no crea usuario automáticamente

**Causa**: Configuración de allauth incorrecta.

**Solución**: Verifica en `settings.py`:
```python
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
```

## 📚 Documentación

- [`CONFIGURACION_OAUTH_INTERNA.md`](CONFIGURACION_OAUTH_INTERNA.md) - Detalles técnicos completos
- [`GUIA_PRUEBA_OAUTH.md`](GUIA_PRUEBA_OAUTH.md) - Guía paso a paso para probar
- [`verify_internal_oauth_config.py`](verify_internal_oauth_config.py) - Script de verificación
- [`clean_old_oauth_config.py`](clean_old_oauth_config.py) - Script de limpieza

## 🔗 URLs de Callback

### Desarrollo Local

```
Google:  http://localhost:8000/accounts/google/login/callback/
         http://127.0.0.1:8000/accounts/google/login/callback/

GitHub:  http://localhost:8000/accounts/github/login/callback/
         http://127.0.0.1:8000/accounts/github/login/callback/
```

### Producción

```
Google:  https://mywebsite-tlxs.onrender.com/accounts/google/login/callback/
GitHub:  https://mywebsite-tlxs.onrender.com/accounts/github/login/callback/
```

## 🎉 Próximos Pasos

1. ✅ **Verificar que funcione localmente**
   ```bash
   python verify_internal_oauth_config.py
   ```

2. 🧪 **Probar el login**
   - Google
   - GitHub

3. 🚀 **Configurar en producción**
   - Variables de entorno en Render
   - URLs de callback en proveedores

4. 📊 **Monitorear logs**
   - Verificar que OAuth funciona
   - Comprobar creación de usuarios

## 💡 Tips

- **No necesitas el admin** para configurar OAuth
- **Las credenciales están en `.env`**, no en la base de datos
- **Fácil de versionar**: La configuración está en el código
- **Seguro**: Las credenciales no se exponen en la base de datos
- **Portable**: Fácil de mover entre entornos

## 🆘 Ayuda

Si tienes problemas:

1. Ejecuta `python verify_internal_oauth_config.py`
2. Revisa los logs del servidor
3. Verifica las URLs de callback en los proveedores
4. Comprueba las variables de entorno

---

**✨ ¡Tu configuración OAuth está lista para usar!**
