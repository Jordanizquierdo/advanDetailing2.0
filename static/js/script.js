let cart = []; // Carrito inicial vacío

/**
 * Añade un servicio al carrito si pasa las validaciones.
 * @param {string} serviceName - Nombre del servicio.
 * @param {number} servicePrice - Precio del servicio.
 * @param {string} serviceType - Tipo de servicio (por ejemplo, 'lavado' o 'especial').
 */
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

/**
 * Muestra los detalles del servicio seleccionado.
 * @param {string} serviceName - Nombre del servicio.
 * @param {number} servicePrice - Precio del servicio.
 * @param {string} serviceId - ID del servicio.
 */
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

  // Insertar el HTML generado en el contenedor de detalles del servicio
  serviceDetailsContainer.innerHTML = serviceDetailsHTML;
}

/**
 * Actualiza el carrito en la barra lateral.
 */
function updateCartSidebar() {
  const cartSidebar = document.getElementById("cart-sidebar");
  const totalPrice = cart.reduce((total, item) => total + item.price, 0);

  // Limpiar el contenido actual del carrito
  cartSidebar.innerHTML = '';

  // Mostrar los servicios en el carrito
  cart.forEach(item => {
    const cartItem = document.createElement("div");
    cartItem.classList.add("cart-item");
    cartItem.innerHTML = `
      <span class="cart-item-title">${item.title}</span>
      <span class="cart-item-price">$${item.price.toLocaleString()}</span>
    `;
    cartSidebar.appendChild(cartItem);
  });

  // Mostrar el total del carrito
  const totalElement = document.createElement("div");
  totalElement.classList.add("cart-total");
  totalElement.innerHTML = `Total: $${totalPrice.toLocaleString()}`;
  cartSidebar.appendChild(totalElement);

  // Mostrar el botón de "Proceder al pago"
  const checkoutButton = document.createElement("button");
  checkoutButton.classList.add("checkout-button");
  checkoutButton.innerHTML = "Proceder al pago";
  checkoutButton.onclick = PayCart;
  cartSidebar.appendChild(checkoutButton);
}

/**
 * Verifica que el carrito no esté vacío y procede al pago.
 */
function PayCart() {
  const clienteId = sessionStorage.getItem('clienteId'); // Cliente autenticado
  if (!clienteId) {
    alert("Debes iniciar sesión para proceder al pago.");
    return;
  }

  // Si el carrito no está vacío, proceder a la página de pago
  if (cart.length === 0) {
    alert("El carrito está vacío.");
    return;
  }

  // Redirigir a la página de pago con los datos del carrito
  const checkoutUrl = `/checkout?cart=${JSON.stringify(cart)}`;
  window.location.href = checkoutUrl;
}

/**
 * Abre el modal con información del vehículo del cliente.
 */
function openModal() {
  const modal = document.getElementById("vehicle-modal");
  const clientId = sessionStorage.getItem("clienteId");

  if (!clientId) {
    alert("Debes iniciar sesión para ver los vehículos.");
    return;
  }

  fetch(`/api/clients/${clientId}/vehicles`)
    .then(response => response.json())
    .then(data => {
      let vehicleListHTML = "<ul>";
      data.vehicles.forEach(vehicle => {
        vehicleListHTML += `<li>${vehicle.model} (${vehicle.year})</li>`;
      });
      vehicleListHTML += "</ul>";
      document.getElementById("vehicle-list").innerHTML = vehicleListHTML;
      modal.style.display = "block"; // Mostrar el modal
    })
    .catch(error => {
      console.error("Error al cargar los vehículos:", error);
      alert("Hubo un error al cargar los vehículos.");
    });
}

/**
 * Cierra el modal.
 */
function closeModal() {
  const modal = document.getElementById("vehicle-modal");
  modal.style.display = "none"; // Ocultar el modal
}

/**
 * Muestra u oculta el menú lateral.
 */
function toggleMenu() {
  const menu = document.getElementById("sidebar");
  menu.classList.toggle("active");
}

/**
 * Animación de los elementos al cargarse la página.
 */
window.onload = () => {
  const containers = document.querySelectorAll(".animated-container");
  containers.forEach((container, index) => {
    container.style.animationDelay = `${index * 0.2}s`;
    container.classList.add("animated");
  });
};
