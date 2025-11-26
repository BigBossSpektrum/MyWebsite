# 📸 Configuración de Cloudinary para Almacenamiento de Archivos

## 🎯 Problema

Render no mantiene archivos persistentes en el disco. Cuando el servicio se reinicia, todos los archivos subidos (imágenes de perfil, productos, etc.) se pierden.

## ✅ Solución: Cloudinary

Cloudinary es un servicio gratuito (hasta 25GB) para almacenamiento de imágenes y videos en la nube.

---

## 📋 Paso 1: Crear Cuenta en Cloudinary

1. Ve a [https://cloudinary.com/users/register/free](https://cloudinary.com/users/register/free)
2. Regístrate con tu email o cuenta de Google
3. Verifica tu email
4. Accede al Dashboard

---

## 🔑 Paso 2: Obtener Credenciales

En tu Dashboard de Cloudinary verás:

```
Cloud Name: tu_cloud_name
API Key: 123456789012345
API Secret: abcdefghijklmnopqrstuvwxyz123
```

**Guarda estas credenciales, las necesitarás en el siguiente paso.**

---

## ⚙️ Paso 3: Configurar Variables de Entorno en Render

1. Ve a tu servicio en [Render Dashboard](https://dashboard.render.com/)
2. Selecciona tu servicio web
3. Ve a **Environment** → **Environment Variables**
4. Agrega estas 3 nuevas variables:

```bash
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret
```

5. Haz clic en **Save Changes**

---

## 🚀 Paso 4: Desplegar los Cambios

1. Asegúrate de hacer commit y push de los cambios:

```bash
git add .
git commit -m "Agregar configuración de Cloudinary para almacenamiento persistente"
git push origin Development---Check
```

2. Render automáticamente detectará los cambios y volverá a desplegar

---

## 🧪 Paso 5: Probar la Configuración

Una vez desplegado, ejecuta este comando desde tu terminal local (conectado a Render):

```bash
python manage.py update_social_profile_pics --provider google
```

O para un usuario específico:

```bash
python manage.py update_social_profile_pics --username admin
```

---

## 📊 Verificar que Funciona

1. Inicia sesión con Google en tu sitio
2. Ve a tu perfil
3. La imagen de perfil debería aparecer
4. Ve al Dashboard de Cloudinary → Media Library
5. Deberías ver la imagen de perfil allí

---

## 🔍 Comandos Útiles

### Diagnosticar cuenta social:
```bash
python manage.py diagnose_social_account <username>
```

### Actualizar todas las fotos de Google:
```bash
python manage.py update_social_profile_pics --provider google
```

### Actualizar todas las fotos (incluir usuarios que ya tienen foto):
```bash
python manage.py update_social_profile_pics --force
```

### Actualizar solo un usuario:
```bash
python manage.py update_social_profile_pics --username admin
```

---

## 📝 Notas Importantes

1. **Cloudinary Gratis**: Incluye 25GB de almacenamiento y 25GB de ancho de banda mensual
2. **Automático**: Las nuevas fotos de perfil se subirán automáticamente a Cloudinary
3. **URLs**: Las URLs de las imágenes ahora serán `https://res.cloudinary.com/...`
4. **Rendimiento**: Cloudinary incluye CDN global, las imágenes cargarán más rápido

---

## 🛠️ Cambios Realizados en el Código

### 1. `requirements.txt`
- ✅ Agregado `cloudinary==1.41.0`
- ✅ Agregado `django-cloudinary-storage==0.3.0`

### 2. `settings.py`
- ✅ Agregado `cloudinary_storage` y `cloudinary` a `INSTALLED_APPS`
- ✅ Configuración de Cloudinary con variables de entorno
- ✅ Uso de `DEFAULT_FILE_STORAGE` en producción

### 3. Comandos de Gestión Creados
- ✅ `diagnose_social_account.py` - Diagnosticar cuentas sociales
- ✅ `update_social_profile_pics.py` - Actualizar fotos de perfil

### 4. `adapters.py`
- ✅ Mejorado logging para debugging
- ✅ Soporte para actualizar fotos en usuarios existentes
- ✅ Scope `openid` agregado para Google OAuth

---

## ⚠️ Troubleshooting

### Error: "No module named 'cloudinary'"
```bash
pip install -r requirements.txt
```

### Error: "Configuration Error"
Verifica que las variables de entorno estén configuradas correctamente en Render.

### La foto no aparece
1. Verifica que las credenciales de Cloudinary sean correctas
2. Ejecuta `python manage.py diagnose_social_account <username>`
3. Verifica que el scope `openid` esté en Google Cloud Console
4. Ejecuta `python manage.py update_social_profile_pics --username <username>`

---

## 📞 Soporte

Si tienes problemas, revisa los logs en Render:
```
Dashboard → Tu Servicio → Logs
```

O contacta a silvekerhernandez@proton.me
