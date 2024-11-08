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
  } else if (serviceName === "Servicios Especiales") {
    // Detalles de servicios especiales
    serviceDetailsHTML = `
      <div class="service-details-container">
        <div class="service-details-center">
          <h3>${serviceName}</h3>
        </div>

        <!-- Servicio Especial 1 -->
        <div class="special-service">
          <h4>Grabado de patente</h4>
          <p>Valor: $15,000</p>
          <button class="add-to-cart-button" onclick="addToCart('Grabado de patente', 15000)">
            Añadir al carrito
            <i class="fa fa-plus add-to-cart-icon"></i>
          </button>
        </div>

        <!-- Servicio Especial 2 -->
        <div class="special-service">
          <h4>Cueros (Limpieza a vapor y humectación)</h4>
          <p>Valor: $25,000</p>
          <button class="add-to-cart-button" onclick="addToCart('Cueros (Limpieza a vapor y humectación)', 25000)">
            Añadir al carrito
            <i class="fa fa-plus add-to-cart-icon"></i>
          </button>
        </div>

        <!-- Servicio Especial 3 -->
        <div class="special-service">
          <h4>Sanitización con retiro de malos olores</h4>
          <p>Valor: $20,000</p>
          <button class="add-to-cart-button" onclick="addToCart('Sanitización con retiro de malos olores', 20000)">
            Añadir al carrito
            <i class="fa fa-plus add-to-cart-icon"></i>
          </button>
        </div>

        <!-- Servicio Especial 4 -->
        <div class="special-service">
          <h4>Pulido de carrocería</h4>
          <p>Valor: $45,000</p>
          <button class="add-to-cart-button" onclick="addToCart('Pulido de carrocería', 45000)">
            Añadir al carrito
            <i class="fa fa-plus add-to-cart-icon"></i>
          </button>
        </div>

        <!-- Servicio Especial 5 -->
        <div class="special-service">
          <h4>Limpieza de tableros a vapor</h4>
          <p>Valor: $15,000</p>
          <button class="add-to-cart-button" onclick="addToCart('Limpieza de tableros a vapor', 15000)">
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

// Función para añadir al carrito
function addToCart(serviceName, servicePrice) {
  cart.push({ title: serviceName, price: servicePrice });
  updateCartSidebar();
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

// Función para redirigir a la página de pago con los datos del carrito
function PayCart() {
  if (cart.length === 0) {
    alert("El carrito está vacío. Añade servicios antes de proceder al pago.");
    return;
  }

  const cartData = encodeURIComponent(JSON.stringify(cart));
  window.location.href = `/carrito/?cartList=${cartData}`;
}

// Función para limpiar el carrito
function clearCart() {
  cart = [];
  updateCartSidebar();
}

