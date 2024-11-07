let cart = []; // Carrito inicial vacío

// Función para mostrar los detalles del servicio
function showServiceDetails(serviceName, servicePrice, serviceId) {
  const serviceDetailsContainer = document.getElementById("service-details-container");

  let serviceDetailsHTML = "";

  if (serviceId === "lavado-basico") {
    serviceDetailsHTML = `
      <div class="service-details-container">
        <div class="service-details-column">
          <p>Lavado exterior</p>
          <p>Limpieza interior</p>
          <p>Aspirado</p>
          <p>Limpieza de tableros</p>
        </div>
        <div class="service-details-center">
          <h3>${serviceName}</h3>
          <p class="service-details-price">Valor: $${servicePrice.toLocaleString()}</p>
          <button class="add-to-cart-button" onclick="addToCart('${serviceName}', ${servicePrice})">
            Añadir al carrito
            <i class="fa fa-plus add-to-cart-icon"></i>
          </button>
        </div>
        <div class="service-details-column">
          <p>Limpieza de llantas</p>
          <p>Limpieza Maletero + Marcos</p>
          <p>Lavado de vidrios y espejos</p>
        </div>
      </div>
    `;
  } else if (serviceId === "lavado-intermedio") {
    serviceDetailsHTML = `
      <div class="service-details-container">
        <div class="service-details-column">
          <p>Lavado exterior completo</p>
          <p>Limpieza profunda de asientos</p>
          <p>Aspirado y lavado de alfombras</p>
          <p>Desinfección interior</p>
        </div>
        <div class="service-details-center">
          <h3>${serviceName}</h3>
          <p class="service-details-price">Valor: $${servicePrice.toLocaleString()}</p>
          <button class="add-to-cart-button" onclick="addToCart('${serviceName}', ${servicePrice})">
            Añadir al carrito
            <i class="fa fa-plus add-to-cart-icon"></i>
          </button>
        </div>
        <div class="service-details-column">
          <p>Limpieza de llantas y rines</p>
          <p>Protección de tableros</p>
          <p>Limpieza de espejos</p>
        </div>
      </div>
    `;
  } else if (serviceId === "lavado-avanzado") {
    serviceDetailsHTML = `
      <div class="service-details-container">
        <div class="service-details-column">
          <p>Lavado exterior</p>
          <p>Limpieza interior</p>
          <p>Aspirado</p>
          <p>Limpieza de tableros</p>
          <p>Encerado / Brillo</p>
          <p>Lavado de Asientos</p>
        </div>
        <div class="service-details-center">
          <h3>${serviceName}</h3>
          <p class="service-details-price">Valor: $${servicePrice.toLocaleString()}</p>
          <button class="add-to-cart-button" onclick="addToCart('${serviceName}', ${servicePrice})">
            Añadir al carrito
            <i class="fa fa-plus add-to-cart-icon"></i>
          </button>
        </div>
        <div class="service-details-column">
          <p>Limpieza de llantas</p>
          <p>Limpieza Maletero + marcos</p>
          <p>Lavado de vidrios y espejos</p>
          <p>Silicona + renovador</p>
          <p>Lavado de Alfombras</p>
        </div>
      </div>
    `;
  }

  serviceDetailsContainer.innerHTML = serviceDetailsHTML;
  serviceDetailsContainer.style.display = "block"; // Mostrar el contenedor de detalles
}

// Función para añadir al carrito (permitiendo solo un servicio a la vez)
function addToCart(serviceName, servicePrice) {
  cart = []; // Limpiar el carrito antes de añadir un nuevo servicio

  cart.push({ title: serviceName, price: servicePrice }); // Añadir el nuevo servicio

  // Actualizar la barra lateral del carrito
  updateCartSidebar();
}

// Función para actualizar el contenido de la barra lateral
function updateCartSidebar() {
  const sidebar = document.getElementById("sidebar");
  const cartList = sidebar.querySelector("ul");
  const totalPrice = sidebar.querySelector(".total");

  // Limpiar contenido previo
  cartList.innerHTML = "";
  let total = 0;

  cart.forEach((item) => {
    const listItem = document.createElement("li");
    listItem.textContent = `${item.title} - $${item.price.toLocaleString()}`;
    cartList.appendChild(listItem);
    total += item.price;
  });

  // Mostrar el total
  totalPrice.textContent = `Total: $${total.toLocaleString()}`;

  // Mostrar el botón de limpiar carrito si hay un elemento
  document.getElementById("btn").style.display = cart.length ? "block" : "none";
  document.getElementById("btn-secondary").style.display = cart.length ? "block" : "none";
}

// Función para limpiar el carrito
function clearCart() {
  cart = [];
  updateCartSidebar();
}

