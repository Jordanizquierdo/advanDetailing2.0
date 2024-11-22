// Obtener los datos del carrito de la URL
const urlParams = new URLSearchParams(window.location.search);
const cartData = JSON.parse(decodeURIComponent(urlParams.get("cartList") || "[]"));
const clienteId = urlParams.get("clienteId");  // Obtener clienteId de la URL

// Selecciona el contenedor donde se mostrarán los artículos del carrito
const cartItemsContainer = document.getElementById("cart-items");
const cartTotalContainer = document.getElementById("cart-total");

let total = 0;

/**
 * Muestra los artículos del carrito y calcula el total.
 * Para cada artículo en el carrito, se crea un elemento <p> y se agrega al contenedor del carrito.
 * Luego, se calcula el total sumando los precios de todos los artículos.
 */
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

/**
 * Redirige al usuario de vuelta a la página de servicios.
 */
function goBackToServices() {
    window.location.href = "./";
}

/**
 * Reserva un servicio seleccionando la fecha, hora y método de pago.
 * Verifica que se hayan ingresado todos los campos necesarios.
 * Si todo es correcto, crea un objeto de datos de reserva y muestra una alerta con la confirmación.
 */
function reserveService() {
    const selectedDate = document.getElementById("selectedDate").value;
    const selectedTime = document.getElementById("selectedTime").value;
    const paymentMethod = document.getElementById("paymentMethod").value;

    // Validaciones
    if (!selectedDate || !selectedTime) {
        alert("Por favor, selecciona una fecha y hora para la reserva.");
        return;
    }

    if (!paymentMethod) {
        alert("Por favor, selecciona un método de pago.");
        return;
    }

    if (!clienteId) {
        alert("Error: No se pudo obtener el ID del cliente.");
        return;
    }

    // Crear el objeto de datos de la reserva
    const reservationData = {
        clienteId: clienteId,
        fechaReserva: selectedDate,
        horaReserva: selectedTime,
        paymentMethod: paymentMethod,
        estado: "pendiente",  // Estado predeterminado
        administrador: null   // Administrador en null
    };

    alert(`Reserva realizada con éxito:\nFecha: ${selectedDate}\nHora: ${selectedTime}\nMétodo de pago: ${paymentMethod}\nCliente: ${clienteId}`);

}
