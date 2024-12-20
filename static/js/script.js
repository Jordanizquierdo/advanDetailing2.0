let cart = []; // Carrito inicial vacío

// Función para añadir al carrito
function addToCart(serviceName, servicePrice, serviceType) {
  const serviceIds = {
    "Lavado Básico": 1,
    "Lavado Intermedio": 2,
    "Lavado Avanzado": 3,
    // Servicios Especiales
    "Grabado de patente": 4,
    "Cueros (Limpieza a vapor y humectación)": 5,
    "Sanitización con retiro de malos olores": 6,
    "Pulido de carrocería": 7,
    "Limpieza de tableros a vapor": 8,
  };

  const serviceId = serviceIds[serviceName] || 0; // 0 para servicios no definidos

  // Verifica si el servicio es un tipo de lavado
  const isLavado = ["Lavado Básico", "Lavado Intermedio", "Lavado Avanzado"].includes(serviceName);

  // Comprueba si ya hay un tipo de lavado en el carrito
  if (isLavado && cart.some(item => ["Lavado Básico", "Lavado Intermedio", "Lavado Avanzado"].includes(item.title))) {
    alert("Solo puedes añadir un tipo de lavado al carrito.");
    return;
  }

  // Comprueba si el servicio especial ya está en el carrito
  if (cart.some(item => item.title === serviceName)) {
    alert(`El servicio "${serviceName}" ya está en el carrito.`);
    return;
  }

  // Añade el servicio al carrito si pasa las validaciones
  cart.push({ title: serviceName, price: servicePrice, type: serviceType, id: serviceId });
  updateCartSidebar();
}

// Función para mostrar los detalles del servicio
function showServiceDetails(serviceName, servicePrice, serviceId) {
  const serviceDetailsContainer = document.getElementById("service-details-container");
  let serviceDetailsHTML = "";

  // Detalles de servicios básicos
  if (serviceId === "lavado-basico") {
    serviceDetailsHTML = `
      <div class="service-details-container">
        <div class="service-details-column">
          <p>Este servicio contiene:</p>
          <p>- Lavado exterior</p>
          <p>- Limpieza interior</p>
          <p>- Aspirado</p>
          <p>- Limpieza de tableros</p>
        </div>
        <div class="service-details-column">
          <p>- Limpieza de llantas</p>
          <p>- Limpieza Maletero + Marcos</p>
          <p>- Lavado de vidrios y espejos</p>
        </div>
        <div class="service-details-center">
          <h3>${serviceName}</h3>
          <p class="service-details-price">Valor: $${servicePrice.toLocaleString()}</p>
          <button class="add-to-cart-button" onclick="addToCart('${serviceName}', ${servicePrice}, 'lavado')">
            Añadir al carrito
            <i class="fa fa-plus add-to-cart-icon"></i>
          </button>
        </div>
      </div>
    `;
  } else if (serviceId === "lavado-intermedio") {
    serviceDetailsHTML = `
      <div class="service-details-container">
        <div class="service-details-column">
          <p>Este servicio contiene:</p>
          <p>- Lavado exterior completo</p>
          <p>- Limpieza profunda de asientos</p>
          <p>- Aspirado y lavado de alfombras</p>
          <p>- Desinfección interior</p>
        </div>
        <div class="service-details-column">
          <p>- Limpieza de llantas y rines</p>
          <p>- Protección de tableros</p>
          <p>- Limpieza de espejos</p>
        </div>
        <div class="service-details-center">
          <h3>${serviceName}</h3>
          <p class="service-details-price">Valor: $${servicePrice.toLocaleString()}</p>
          <button class="add-to-cart-button" onclick="addToCart('${serviceName}', ${servicePrice}, 'lavado')">
            Añadir al carrito
            <i class="fa fa-plus add-to-cart-icon"></i>
          </button>
        </div>
      </div>
    `;
  } else if (serviceId === "lavado-avanzado") {
    serviceDetailsHTML = `
      <div class="service-details-container">
        <div class="service-details-column">
          <p>Este servicio contiene:</p>
          <p>- Lavado exterior</p>
          <p>- Limpieza interior</p>
          <p>- Aspirado</p>
          <p>- Limpieza de tableros</p>
          <p>- Encerado / Brillo</p>
          <p>- Lavado de Asientos</p>
        </div>
        <div class="service-details-column">
          <p>- Limpieza de llantas</p>
          <p>- Limpieza Maletero + marcos</p>
          <p>- Lavado de vidrios y espejos</p>
          <p>- Silicona + renovador</p>
          <p>- Lavado de Alfombras</p>
        </div>
        <div class="service-details-center">
          <h3>${serviceName}</h3>
          <p class="service-details-price">Valor: $${servicePrice.toLocaleString()}</p>
          <button class="add-to-cart-button" onclick="addToCart('${serviceName}', ${servicePrice}, 'lavado')">
            Añadir al carrito
            <i class="fa fa-plus add-to-cart-icon"></i>
          </button>
        </div>
      </div>
    `;
  } else if (serviceName === "Servicios Especiales") {
    serviceDetailsHTML = `
      <div class="service-details-container">
        <div class="service-details-center">
          <h3>${serviceName}</h3>
        </div>
        <div class="special-service">
          <h4>Grabado de patente</h4>
          <p>Grabado láser de patente en vidrios</p>
          <p class="service-details-price">Valor: $15,000</p>
          <button class="add-to-cart-button" onclick="addToCart('Grabado de patente', 15000, 'especial')">
            Añadir al carrito
            <i class="fa fa-plus add-to-cart-icon"></i>
          </button>
        </div>
        <div class="special-service">
          <h4>Cueros (Limpieza a vapor y humectación)</h4>
          <p>Limpieza a vapor</p>
          <p>Humectación de cueros</p>
          <p class="service-details-price">Valor: $25,000</p>
          <button class="add-to-cart-button" onclick="addToCart('Cueros (Limpieza a vapor y humectación)', 25000, 'especial')">
            Añadir al carrito
            <i class="fa fa-plus add-to-cart-icon"></i>
          </button>
        </div>
        <div class="special-service">
          <h4>Sanitización con retiro de malos olores</h4>
          <p>Desinfección profunda</p>
          <p>Eliminación de olores</p>
          <p class="service-details-price">Valor: $20,000</p>
          <button class="add-to-cart-button" onclick="addToCart('Sanitización con retiro de malos olores', 20000, 'especial')">
            Añadir al carrito
            <i class="fa fa-plus add-to-cart-icon"></i>
          </button>
        </div>
        <div class="special-service">
          <h4>Pulido de carrocería</h4>
          <p>Pulido y abrillantado profesional</p>
          <p>Eliminación de rayones menores</p>
          <p class="service-details-price">Valor: $45,000</p>
          <button class="add-to-cart-button" onclick="addToCart('Pulido de carrocería', 45000, 'especial')">
            Añadir al carrito
            <i class="fa fa-plus add-to-cart-icon"></i>
          </button>
        </div>
        <div class="special-service">
          <h4>Limpieza de tableros a vapor</h4>
          <p>Limpieza profunda con vapor</p>
          <p>Restauración de superficies</p>
          <p class="service-details-price">Valor: $15,000</p>
          <button class="add-to-cart-button" onclick="addToCart('Limpieza de tableros a vapor', 15000, 'especial')">
            Añadir al carrito
            <i class="fa fa-plus add-to-cart-icon"></i>
          </button>
        </div>
      </div>
    `;
  }

  serviceDetailsContainer.innerHTML = serviceDetailsHTML;
  serviceDetailsContainer.style.display = "block";
}


// Función para actualizar el carrito en la barra lateral
function updateCartSidebar() {
  const sidebar = document.getElementById("sidebar");
  const cartList = sidebar.querySelector("ul");
  const totalPrice = sidebar.querySelector(".total");

  cartList.innerHTML = "";
  let total = 0;

  cart.forEach((item) => {
    const listItem = document.createElement("li");
    listItem.textContent = `${item.title} - $${item.price.toLocaleString()}`;
    cartList.appendChild(listItem);
    total += item.price;
  });

  totalPrice.textContent = `Total: $${total.toLocaleString()}`;
  document.getElementById("btn").style.display = cart.length ? "block" : "none";
  document.getElementById("btn-secondary").style.display = cart.length ? "block" : "none";
}

function clearCart() {
  cart = [];
  updateCartSidebar();
}


function PayCart() {
  // Verifica si el cliente está autenticado
  if (!clienteId || clienteId === "") {
    alert("Debes iniciar sesión para pagar el carrito.");
    window.location.href = "/login/"; // Redirige al login si no está autenticado
    return; 
  }

  // Verifica si el carrito está vacío
  if (cart.length === 0) {
    alert("El carrito está vacío. Añade servicios antes de proceder al pago.");
    return; 
  }

  // Si el carrito tiene elementos y el usuario está autenticado, realiza el pago
  const clienteIdParam = encodeURIComponent(clienteId);
  const cartData = encodeURIComponent(JSON.stringify(cart));

  // Redirige a la página del carrito con los parámetros necesarios (clienteId y cartData)
  window.location.href = `/carrito/?clienteId=${clienteIdParam}&cartList=${cartData}`;
}

// menu desplegable
function toggleMenu() {
  const sidebar = document.getElementById('sidebar');
  sidebar.classList.toggle('slicebar-open');
}

// funcion de la ventana emergente del clientes 

function openModal(clienteId) {
  console.log("Abriendo modal para cliente:", clienteId); // Depuración
  const modal = document.getElementById('modal');
  const modalBody = document.getElementById('modal-body');

  // Limpia el contenido previo
  modalBody.innerHTML = 'Cargando información...';

  // Realiza una solicitud al servidor para obtener los datos del cliente
  fetch(`/clientes/${clienteId}/vehiculos/`)
      .then(response => response.json())
      .then(data => {
          if (data.vehiculos.length > 0) {
              const vehicleInfo = data.vehiculos.map(v => `
                  <p>
                      <strong>Modelo:</strong> ${v.modelo}<br>
                      <strong>Año:</strong> ${v.year}<br>
                      <strong>Patente:</strong> ${v.patente}
                  </p>
              `).join('');
              modalBody.innerHTML = vehicleInfo;
          } else {
              modalBody.innerHTML = '<p>Este cliente no tiene vehículos asociados.</p>';
          }
      })
      .catch(error => {
          console.error('Error al cargar los datos:', error);
          modalBody.innerHTML = '<p>Hubo un error al cargar los datos. Inténtalo nuevamente.</p>';
      });

  // Muestra el modal
  modal.style.display = 'block';
}

function closeModal() {
  const modal = document.getElementById('modal');
  modal.style.display = 'none';
}

document.addEventListener("DOMContentLoaded", () => {
  const elementsToAnimate = document.querySelectorAll(".main-container, .slicebar, .services, .service, .service-details-container, .special-service, h1");

  elementsToAnimate.forEach((element) => {
    element.classList.add("animated");
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const animatedElements = document.querySelectorAll(".animated");
  animatedElements.forEach((element, index) => {
      element.style.animationDelay = `${index * 0.2}s`;
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  if (form) {
      form.style.animationDelay = "0.2s";
  }
});

document.addEventListener("DOMContentLoaded", () => {
  // Animar el título de la tabla
  const tableTitle = document.querySelector(".table-title");
  if (tableTitle) {
      tableTitle.classList.add("table-header");
      tableTitle.style.animationDelay = "0.1s";
  }

  // Selecciona las cabeceras de la tabla
  const tableHeaders = document.querySelectorAll("table thead tr th");
  tableHeaders.forEach((header, index) => {
      header.classList.add("table-header");
      header.style.animationDelay = `${index * 0.1 + 0.2}s`; // Inicia después del título
  });

  // Selecciona las filas de la tabla
  const tableRows = document.querySelectorAll("table tbody tr");
  tableRows.forEach((row, index) => {
      row.classList.add("table-row");
      row.style.animationDelay = `${index * 0.2 + 0.5}s`; // Inicia después de las cabeceras
  });
});
