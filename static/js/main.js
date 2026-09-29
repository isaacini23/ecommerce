document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.querySelector(".menu-toggle");
    const navLinks = document.querySelector(".nav-links");

    if (menuToggle && navLinks) {
        menuToggle.addEventListener("click", function () {
            navLinks.classList.toggle("active");
        });
    }
});


function changeMainImage(image) {
    const mainImage = document.getElementById("main-product-image");

    if (mainImage) {
        mainImage.src = image.src;
        mainImage.alt = image.alt;
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const cartUpdateForms = document.querySelectorAll(".cart-update-form");

    cartUpdateForms.forEach(function (form) {
        form.addEventListener("submit", function (event) {
            event.preventDefault();

            const cartItem = form.closest(".cart-item");
            const quantityInput = form.querySelector(".cart-quantity");
            const itemTotal = cartItem.querySelector(".cart-item-total");

            const quantity = quantityInput.value;
            const csrfToken = form.querySelector(
                "[name=csrfmiddlewaretoken]"
            ).value;

            fetch(form.action, {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({
                    quantity: quantity,
                    csrfmiddlewaretoken: csrfToken,
                }),
            })
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                if (data.success) {
                    itemTotal.textContent = "₦" + data.item_total;

                    const cartTotal = document.querySelector(
                        ".cart-summary h2"
                    );

                    if (cartTotal) {
                        cartTotal.textContent =
                            "Total: ₦" + data.cart_total;
                    }
                } else {
                    alert(data.message);
                }
            })
            .catch(function (error) {
                console.error("Cart update error:", error);
                alert("Something went wrong. Please try again.");
            });
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const cartRemoveForms = document.querySelectorAll(".cart-remove-form");

    cartRemoveForms.forEach(function (form) {
        form.addEventListener("submit", function (event) {
            event.preventDefault();

            const cartItem = form.closest(".cart-item");

            const csrfToken = form.querySelector(
                "[name=csrfmiddlewaretoken]"
            ).value;

            fetch(form.action, {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": csrfToken,
                },
                body: new URLSearchParams({
                    csrfmiddlewaretoken: csrfToken,
                }),
            })
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                if (data.success) {
                    cartItem.remove();

                    const cartTotal = document.querySelector(
                        ".cart-summary h2"
                    );

                    if (cartTotal) {
                        cartTotal.textContent =
                            "Total: ₦" + data.cart_total;
                    }

                    if (data.total_items === 0) {
                        window.location.reload();
                    }
                } else {
                    alert("Unable to remove this item.");
                }
            })
            .catch(function (error) {
                console.error("Remove cart item error:", error);
                alert("Something went wrong. Please try again.");
            });
        });
    });
});