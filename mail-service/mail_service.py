from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from email.message import EmailMessage
from email.parser import BytesParser
from email.policy import default
from urllib.parse import parse_qs
import html
import json
import os
import smtplib
import ssl


HOST = os.getenv("SERVER_HOST", "127.0.0.1")
PORT = int(os.getenv("SERVER_PORT", "8787"))
ALLOWED_ORIGIN = os.getenv("ALLOWED_ORIGIN", "*")

SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)
LEAD_TO = os.getenv("LEAD_TO", SMTP_USER)
FROM_NAME = os.getenv("FROM_NAME", "Executive Reporting System")


FIELD_LABELS = {
    "name": "Nombre",
    "email": "Email",
    "phone": "Telefono o WhatsApp",
    "company": "Empresa o actividad",
    "role": "Area o rol",
    "pack_interest": "Pack de interes",
    "data_source": "Fuente de datos disponible",
    "message": "Que necesita resolver o presentar",
}


def required_config_missing():
    return [
        key
        for key, value in {
            "SMTP_HOST": SMTP_HOST,
            "SMTP_USER": SMTP_USER,
            "SMTP_PASS": SMTP_PASS,
            "FROM_EMAIL": FROM_EMAIL,
            "LEAD_TO": LEAD_TO,
        }.items()
        if not value
    ]


def clean(value):
    return " ".join(value.replace("\r", " ").split()).strip()


def read_form(body, content_type):
    if "application/json" in content_type:
        return json.loads(body.decode("utf-8") or "{}")

    if "multipart/form-data" in content_type:
        message = BytesParser(policy=default).parsebytes(
            f"Content-Type: {content_type}\r\n\r\n".encode("utf-8") + body
        )
        values = {}
        for part in message.iter_parts():
            name = part.get_param("name", header="content-disposition")
            if not name:
                continue
            payload = part.get_payload(decode=True) or b""
            charset = part.get_content_charset() or "utf-8"
            values[name] = payload.decode(charset, errors="replace")
        return values

    parsed = parse_qs(body.decode("utf-8"), keep_blank_values=True)
    return {key: values[0] for key, values in parsed.items()}


def lead_email_text(data):
    lines = ["Nuevo lead desde Executive Reporting System", ""]
    for key, label in FIELD_LABELS.items():
        lines.append(f"{label}: {clean(data.get(key, 'No indicado')) or 'No indicado'}")
    return "\n".join(lines)


def lead_email_html(data):
    rows = []
    for key, label in FIELD_LABELS.items():
        value = html.escape(clean(data.get(key, "No indicado")) or "No indicado")
        rows.append(f"<tr><th>{html.escape(label)}</th><td>{value}</td></tr>")

    return f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #18212b;">
        <h2>Nuevo lead desde Executive Reporting System</h2>
        <table cellpadding="8" cellspacing="0" style="border-collapse: collapse;">
          {''.join(rows)}
        </table>
      </body>
    </html>
    """


def autoresponse_text(name):
    greeting = f"Hola {name}," if name else "Hola,"
    return f"""{greeting}

Gracias por escribirnos. Recibimos tu solicitud para evaluar un reporte ejecutivo piloto.

En las proximas horas vas a recibir el contacto de nuestro equipo para revisar puntualmente tu caso y planificar una demo sobre que podemos construir con los datos que tenes hoy.

Para avanzar, probablemente vamos a pedirte una fuente de datos en Excel, CSV, Google Sheets o un export similar. No hace falta que este perfecto: puede ser una planilla operativa, un reporte actual, un listado de ventas, proyectos, clientes, costos, tickets, tareas o indicadores dispersos.

La idea de la primera revision es entender:

- Que informacion tenes disponible.
- Quien consume el reporte.
- Que necesitas lograr: decidir, vender valor, renovar, alinear, priorizar o mostrar avance.
- Que salida conviene construir: Executive Report, Client Business Review, Owner Brief o un pack por area.

Nuestro foco no es convertir datos en graficos. Es convertir informacion dispersa en una lectura clara para tomar mejores decisiones o presentar valor con mas autoridad.

Saludos,
Executive Reporting System
"""


def send_email(to_email, subject, text_body, html_body=None, reply_to=None):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"] = to_email
    if reply_to:
        msg["Reply-To"] = reply_to
    msg.set_content(text_body)
    if html_body:
        msg.add_alternative(html_body, subtype="html")

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as server:
        server.starttls(context=context)
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)


class Handler(BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", ALLOWED_ORIGIN)
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Accept")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_POST(self):
        if self.path != "/lead":
            self.respond(404, {"ok": False, "error": "Not found"})
            return

        missing = required_config_missing()
        if missing:
            self.respond(500, {"ok": False, "error": f"Missing config: {', '.join(missing)}"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length)
            data = read_form(body, self.headers.get("Content-Type", ""))

            name = clean(data.get("name", ""))
            email = clean(data.get("email", ""))
            if not name or not email or "@" not in email:
                self.respond(400, {"ok": False, "error": "Nombre y email son obligatorios."})
                return

            send_email(
                LEAD_TO,
                "Nuevo lead - Executive Reporting System",
                lead_email_text(data),
                lead_email_html(data),
                reply_to=email,
            )
            send_email(
                email,
                "Recibimos tu solicitud - Executive Reporting System",
                autoresponse_text(name),
            )

            self.respond(200, {"ok": True})
        except Exception as exc:
            print(f"Error processing lead: {exc}")
            self.respond(500, {"ok": False, "error": "Internal error"})

    def respond(self, status, payload):
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


if __name__ == "__main__":
    print(f"Mail service running at http://{HOST}:{PORT}/lead")
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    server.serve_forever()
