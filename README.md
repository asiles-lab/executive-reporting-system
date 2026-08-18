# Executive Reporting System

Landing page comercial para presentar servicios de reporting ejecutivo por area, rol y caso de uso: IT, operaciones, ventas, RRHH, proyectos, autonomos y business owners.

## Estructura

- `index.html`: landing principal.
- `styles.css`: estilos de la landing.
- `script.js`: envio del formulario al endpoint configurado.
- `gracias.html`: pagina de confirmacion.
- `assets/hero-services.webp`: imagen principal optimizada.
- `mail-service/`: servicio local para recibir leads por email y enviar autorespuesta.

## Publicar con GitHub Pages

1. Entrar al repo en GitHub.
2. Ir a `Settings` > `Pages`.
3. En `Build and deployment`, elegir `Deploy from a branch`.
4. En `Branch`, seleccionar `main` y carpeta `/root`.
5. Guardar.

La URL esperada es:

```text
https://asiles-lab.github.io/executive-reporting-system/
```

Puede tardar unos minutos en estar disponible.

## Formulario y mails

La landing envia el formulario al endpoint configurado en `index.html`, atributo `data-endpoint` del formulario.

Para prueba local, el endpoint actual puede ser:

```text
http://127.0.0.1:8787/lead
```

Para que funcione desde una web publica, ese endpoint debe ser una URL publica que apunte al servicio local, por ejemplo mediante un tunel seguro.

## Ejecutar el servicio de mails local

Dentro de `mail-service/`:

1. Copiar `.env.example` como `.env`.
2. Completar `SMTP_USER`, `SMTP_PASS`, `FROM_EMAIL` y `LEAD_TO`.
3. Ejecutar en PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\start-mail-service.ps1
```

El archivo `.env` real no debe subirse al repo.
