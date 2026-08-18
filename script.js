const form = document.querySelector("#contactForm");
const note = document.querySelector("#formNote");

form?.addEventListener("submit", (event) => {
  const endpoint = form.dataset.endpoint?.trim();

  if (!endpoint && form.getAttribute("action")) {
    note.textContent = "Enviando solicitud...";
    return;
  }

  event.preventDefault();

  const data = new FormData(form);
  const name = data.get("name")?.toString().trim() || "";
  const email = data.get("email")?.toString().trim() || "";
  const phone = data.get("phone")?.toString().trim() || "No indicado";
  const company = data.get("company")?.toString().trim() || "No indicado";
  const role = data.get("role")?.toString().trim() || "No indicado";
  const pack = data.get("pack_interest")?.toString().trim() || "No definido";
  const dataSource = data.get("data_source")?.toString().trim() || "No indicado";
  const message =
    data.get("message")?.toString().trim() ||
    "Quiero evaluar un reporte ejecutivo piloto para ordenar informacion, decidir mejor o presentar valor.";

  if (endpoint) {
    note.textContent = "Enviando solicitud...";

    fetch(endpoint, {
      method: "POST",
      body: data,
      headers: {
        Accept: "application/json",
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("No se pudo enviar el formulario.");
        }

        window.location.href = "./gracias.html";
      })
      .catch(() => {
        note.textContent =
          "No pudimos enviar el formulario. Proba nuevamente o escribinos por email.";
      });

    return;
  }

  const subject = "Consulta - Executive Reporting System";
  const body = [
    "Hola, quiero evaluar un reporte ejecutivo piloto.",
    "",
    `Nombre: ${name}`,
    `Email: ${email}`,
    `Telefono o WhatsApp: ${phone}`,
    `Empresa o actividad: ${company}`,
    `Area o rol: ${role}`,
    `Pack de interes: ${pack}`,
    `Fuente de datos disponible: ${dataSource}`,
    "",
    "Que necesito resolver o presentar:",
    message,
  ].join("\n");

  window.location.href = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;

  note.textContent = "Listo. Se preparo el email con tu consulta.";
});
