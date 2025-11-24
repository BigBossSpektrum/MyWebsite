# 🔧 Fix: Database SQLite en vez de PostgreSQL

## ❌ Problema
El error muestra que Render está usando **SQLite** en lugar de **PostgreSQL**:
```
Exception Location: /opt/render/project/src/.venv/lib/python3.13/site-packages/django/db/backends/sqlite3/base.py
```

Esto significa que `DATABASE_URL` no está configurado correctamente.

## ✅ Solución

### Opción 1: Usar el Dashboard de Render (Recomendado)

1. **Ve a Render Dashboard** → https://dashboard.render.com

2. **Si NO tienes una base de datos creada:**
   - Click en "New +"
   - Selecciona "PostgreSQL"
   - Nombre: `zultech-main-db`
   - Plan: Free
   - Click "Create Database"

3. **Conecta la base de datos a tu servicio web:**
   - Ve a tu servicio web (`mywebsite-tlxs`)
   - Ve a la pestaña "Environment"
   - Click "Add Environment Variable"
   - Key: `DATABASE_URL`
   - Value: Ve a tu base de datos y copia la "Internal Database URL"
   - Click "Save Changes"

4. **Fuerza un nuevo despliegue:**
   - Ve a "Manual Deploy"
   - Click "Clear build cache & deploy"

### Opción 2: Usar render.yaml (Automático)

Si prefieres que Render maneje todo automáticamente:

1. **Elimina el servicio existente en Render** (si existe)
2. **Elimina la base de datos existente** (si existe)
3. **Crea un nuevo servicio desde Blueprint:**
   - Click "New +" → "Blueprint"
   - Conecta tu repositorio
   - Render leerá `render.yaml` y creará TODO automáticamente
   - Esto incluye la base de datos Y el servicio web conectados

### Opción 3: Diagnóstico Manual

Ejecuta este comando en Render Shell para ver qué está pasando:

```bash
python manage.py diagnose_db
```

Esto te dirá:
- ✅ Si `DATABASE_URL` está configurado
- ✅ Qué motor de base de datos está usando
- ✅ Si la conexión funciona
- ✅ Si la tabla `django_site` existe

## 🔍 Verificación

### En Render Dashboard:

1. **Ve a Environment Variables:**
   - Debe existir `DATABASE_URL`
   - Debe empezar con: `postgresql://` o `postgres://`
   - NO debe estar vacío

2. **Ve a la base de datos:**
   - Debe estar en estado "Available"
   - Debe tener una "Internal Database URL"

3. **Revisa los logs del build:**
   - Busca: "Running database diagnostics"
   - Debe decir: "Using PostgreSQL (Production)"
   - NO debe decir: "Using SQLite (Development)"

## 📝 Archivos Actualizados

### `render.yaml`
```yaml
databases:
  - name: zultech-main-db
    databaseName: zultech_main_db
    user: zultech_main_db

services:
  - type: web
    name: mywebsite-tlxs
    env: python
    plan: free
    buildCommand: './build.sh'
    startCommand: 'gunicorn Zultech_main.asgi:application -k uvicorn.workers.UvicornWorker'
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: zultech-main-db  # ⚠️ Debe coincidir con el nombre de la BD
          property: connectionString
```

### `settings.py`
```python
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
```

## 🚨 Errores Comunes

### 1. "DATABASE_URL" no existe
**Causa:** La base de datos no está vinculada al servicio  
**Solución:** Sigue "Opción 1" arriba

### 2. render.yaml no se aplica
**Causa:** El servicio se creó manualmente, no desde Blueprint  
**Solución:** Sigue "Opción 2" arriba

### 3. Sigue usando SQLite después de configurar
**Causa:** El build no se ejecutó después de añadir `DATABASE_URL`  
**Solución:** Manual Deploy → "Clear build cache & deploy"

## 📋 Checklist

Antes de continuar, verifica:
- [ ] Base de datos PostgreSQL creada en Render
- [ ] Base de datos en estado "Available"
- [ ] Variable `DATABASE_URL` configurada en el servicio web
- [ ] `DATABASE_URL` comienza con `postgresql://` o `postgres://`
- [ ] Servicio web re-desplegado después de configurar
- [ ] Logs muestran "Using PostgreSQL (Production)"

## 🔄 Próximos Pasos

Después de arreglar la base de datos:

1. **Push estos cambios:**
```bash
git add .
git commit -m "Fix: Configuración de base de datos PostgreSQL"
git push origin Development---Check
```

2. **Render re-desplegará automáticamente**

3. **Verifica en los logs:**
   - Debe mostrar "Database connection successful!"
   - Debe mostrar "Using PostgreSQL (Production)"
   - Debe mostrar "django_site table exists"

4. **Prueba tu sitio:**
   - https://mywebsite-tlxs.onrender.com/accounts/login/
   - NO debe mostrar "no such table: django_site"

---

**¿Aún tienes problemas?** Ejecuta `python manage.py diagnose_db` en Render Shell y comparte el output.
