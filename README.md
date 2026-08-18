# Executive Reporting System

Landing page comercial para presentar servicios de reporting ejecutivo por area, rol y caso de uso: IT, operaciones, ventas, RRHH, proyectos, autonomos y business owners.

## Estructura

- `index.html`: landing principal.
- `styles.css`: estilos de la landing.
- `script.js`: comportamiento del formulario.
- `gracias.html`: pagina de confirmacion.
- `assets/hero-services.webp`: imagen principal optimizada.
- `mail-service/`: servicio local opcional para recibir leads por email y enviar autorespuesta desde Gmail.

## Web publica

La landing esta publicada con GitHub Pages en:

```text
https://asiles-lab.github.io/executive-reporting-system/
```

## Formulario publico

El formulario de `index.html` esta configurado para enviar consultas desde GitHub Pages mediante FormSubmit:

```html
<form class="contact-form" id="contactForm" action="https://formsubmit.co/gestiaexecutivereporting@gmail.com" method="POST">
```

Incluye:

- Email interno con todos los datos del lead.
- Redireccion a `gracias.html` despues del envio.
- Autorespuesta al contacto.
- Campo honeypot antispam.

La primera vez que se envie el formulario, FormSubmit puede mandar un email de activacion a `gestiaexecutivereporting@gmail.com`. Hay que abrir ese email y confirmar el formulario para que los proximos envios entren normalmente.

## Servicio de mails local opcional

El directorio `mail-service/` queda como alternativa propia si mas adelante se quiere tener control total del envio desde Gmail o exponer un endpoint propio por HTTPS.

Dentro de `mail-service/`:

1. Copiar `.env.example` como `.env`.
2. Completar `SMTP_USER`, `SMTP_PASS`, `FROM_EMAIL` y `LEAD_TO`.
3. Ejecutar en PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\start-mail-service.ps1
```

El archivo `.env` real no debe subirse al repo.
