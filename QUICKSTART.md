# 🚀 Quick Start - Despliegue a Render

## ¿Qué se arregló?

El error `OperationalError: no such table: django_site` ha sido **completamente solucionado**.

### Solución Implementada:
✅ Comando `setup_site` que crea automáticamente el objeto Site  
✅ Script `build.sh` actualizado para ejecutar el comando  
✅ Configuración de producción mejorada  
✅ Variables de entorno OAuth preparadas  

## 🎯 Despliegue en 3 Pasos

### Opción A: Script Automático (Recomendado)

```bash
# Windows:
deploy_to_render.bat

# Linux/Mac:
bash deploy_to_render.sh
```

### Opción B: Manual

```bash
# 1. Verificar configuración
python verify_render_config.py

# 2. Arreglar build.sh
python fix_build_script.py

# 3. Commit y push
git add .
git commit -m "Fix: Configuración para despliegue en Render"
git push origin Development---Check
```

## 🔐 Configurar OAuth en Render Dashboard

Una vez desplegado, añade estas variables de entorno:

```env
# Google OAuth
OAUTH_GOOGLE_ID=tu-google-client-id
OAUTH_GOOGLE_SECRET=tu-google-secret

# GitHub OAuth
OAUTH_GITHUB_ID=tu-github-client-id
OAUTH_GITHUB_SECRET=tu-github-secret

# Facebook OAuth
OAUTH_FACEBOOK_ID=tu-facebook-app-id
OAUTH_FACEBOOK_SECRET=tu-facebook-app-secret
```

## 🔗 Actualizar URLs de Callback

### Google
https://console.cloud.google.com/
→ Tu proyecto → Credentials → OAuth Client ID → Authorized redirect URIs:
```
https://mywebsite-tlxs.onrender.com/accounts/google/login/callback/
```

### GitHub
https://github.com/settings/developers
→ Tu OAuth App → Authorization callback URL:
```
https://mywebsite-tlxs.onrender.com/accounts/github/login/callback/
```

### Facebook
https://developers.facebook.com/
→ Tu app → Facebook Login → Settings → Valid OAuth Redirect URIs:
```
https://mywebsite-tlxs.onrender.com/accounts/facebook/login/callback/
```

## ✅ Verificar Funcionamiento

Después del despliegue:
1. Visita: `https://mywebsite-tlxs.onrender.com`
2. Prueba el login manual
3. Prueba OAuth (si configurado)
4. Verifica que los archivos estáticos cargan

## 📚 Más Información

- **Guía Completa**: Ver `DEPLOY_RENDER.md`
- **Resumen Técnico**: Ver `RENDER_FIX.md`
- **Cambios Realizados**: Ver `CAMBIOS_RENDER.md`

## 🆘 ¿Problemas?

### Build falla
- Revisa logs en Render Dashboard
- Verifica que `build.sh` tenga permisos correctos

### "no such table: django_site" (aún)
- El comando `setup_site` no se ejecutó
- Verifica que `build.sh` incluya: `python manage.py setup_site`
- Ejecuta manualmente en Render Shell: `python manage.py setup_site`

### OAuth no funciona
- Verifica que las variables de entorno estén configuradas
- Verifica que las URLs de callback coincidan exactamente
- Deben usar HTTPS, no HTTP

---

**¿Listo para desplegar?** Ejecuta `deploy_to_render.bat` (Windows) o `bash deploy_to_render.sh` (Linux/Mac)
