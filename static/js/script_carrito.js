// Obtener los datos del carrito de la URL
const urlParams = new URLSearchParams(window.location.search);
const cartData = JSON.parse(decodeURIComponent(urlParams.get("cartList") || "[]"));

// Selecciona el contenedor donde se mostrarán los artículos del carrito
const cartItemsContainer = document.getElementById("cart-items");
const cartTotalContainer = document.getElementById("cart-total");

let total = 0;

// Mostrar los elementos del carrito y calcular el total
cartData.forEach(item => {
    const itemElement = document.createElement("p");
    itemElement.textContent = `${item.title} - $${item.price.toLocaleString()}`;
    cartItemsContainer.appendChild(itemElement);
    total += item.price;
});

// Mostrar el total del carrito
const totalElement = document.createElement("p");
totalElement.textContent = `Total: $${total.toLocaleString()}`;
cartTotalContainer.appendChild(totalElement);

// Función para regresar a la página de servicios
function goBackToServices() {
    window.location.href = "./";
}

function reserveService() {
    const selectedDate = document.getElementById("selectedDate").value;
    const paymentMethod = document.getElementById("paymentMethod").value;

    if (!selectedDate) {
        alert("Por favor, selecciona una fecha para la reserva.");
        return;
    }

    if (!paymentMethod) {
        alert("Por favor, selecciona un método de pago.");
        return;
    }

    // Puedes reemplazar esta alerta por una llamada para enviar los datos al servidor
    alert(`Reserva realizada con éxito para el ${selectedDate}. Método de pago: ${paymentMethod}`);
}
