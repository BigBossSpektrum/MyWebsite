# Configuración de URI de Redirección para Google OAuth

## ⚠️ Error actual
```
Error 400: redirect_uri_mismatch
```

Este error ocurre porque la URI de redirección de tu aplicación no está registrada en Google Cloud Console.

## 🔧 Solución

### Paso 1: Accede a Google Cloud Console
1. Ve a: https://console.cloud.google.com/
2. Selecciona tu proyecto
3. Ve a **APIs & Services** > **Credentials**
4. Encuentra tu OAuth 2.0 Client ID y haz clic en el ícono de editar (lápiz)

### Paso 2: Agrega las URIs de Redirección Autorizadas

En la sección **"Authorized redirect URIs"**, agrega las siguientes URIs:

#### Para desarrollo local (localhost):
```
http://localhost:8000/accounts/google/login/callback/
http://127.0.0.1:8000/accounts/google/login/callback/
```

#### Para producción (Render.com):
```
https://mywebsite-tlxs.onrender.com/accounts/google/login/callback/
```

### Paso 3: Guarda los cambios
- Haz clic en **"Save"** o **"Guardar"**
- Espera unos segundos para que los cambios se propaguen

## 📋 Configuración actual en tu proyecto

### Domain del Site (Django):
- **Domain**: `localhost:8000`
- **Site ID**: `1`

### Client ID de Google:
- **Client ID**: `514806161353-b063a8iu612rijnkfrqinlepja666f35.apps.googleusercontent.com`

### Ruta de callback en Django:
```
/accounts/google/login/callback/
```

## ✅ Verificación

Después de configurar las URIs en Google Cloud Console:

1. Limpia la caché del navegador o usa una ventana de incógnito
2. Intenta iniciar sesión con Google nuevamente
3. El flujo OAuth debería funcionar correctamente

## 🔍 URIs que debes verificar

**Formato completo de las URIs de redirección:**
```
{SCHEME}://{DOMAIN}/accounts/google/login/callback/
```

Ejemplos:
- Local: `http://localhost:8000/accounts/google/login/callback/`
- Producción: `https://mywebsite-tlxs.onrender.com/accounts/google/login/callback/`

## 📝 Notas importantes

1. **No olvides el slash final (/)**: `/callback/` no `/callback`
2. **Protocolo correcto**: `http://` para localhost, `https://` para producción
3. **Dominio exacto**: Debe coincidir exactamente con el que estás usando
4. **Puerto incluido**: Para localhost, incluye `:8000`

## 🆘 Si el problema persiste

Si después de agregar las URIs el error continúa:

1. Verifica que guardaste los cambios en Google Cloud Console
2. Espera 1-2 minutos para la propagación
3. Limpia las cookies y caché del navegador
4. Intenta en una ventana de incógnito
5. Verifica que estás usando el Client ID correcto en `settings.py`
