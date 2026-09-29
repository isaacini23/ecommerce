
document.addEventListener("DOMContentLoaded", function () {

    // ==============================
    // Mobile Navigation
    // ==============================

    const menuToggle = document.querySelector(".menu-toggle");
    const navLinks = document.querySelector(".nav-links");

    if (menuToggle && navLinks) {
        menuToggle.addEventListener("click", function () {
            navLinks.classList.toggle("active");
        });
    }


    // ==============================
    // Cart Update Forms
    // ==============================

    const cartUpdateForms = document.querySelectorAll(".cart-update-form");

    cartUpdateForms.forEach(function (form) {
        form.addEventListener("submit", function (event) {
            event.preventDefault();

            updateCartItem(form);
        });
    });


    // ==============================
    // Cart Quantity Buttons
    // ==============================

    const quantityButtons = document.querySelectorAll(".quantity-btn");

    quantityButtons.forEach(function (button) {
        button.addEventListener("click", function () {

            const form = button.closest(".cart-update-form");

            if (!form) {
                return;
            }

            const quantityInput = form.querySelector(".cart-quantity");

            if (!quantityInput) {
                return;
            }

            let quantity = parseInt(quantityInput.value);

            if (isNaN(quantity) || quantity < 1) {
                quantity = 1;
            }

            if (button.classList.contains("quantity-minus")) {

                if (quantity > 1) {
                    quantity -= 1;
                }

            }

            if (button.classList.contains("quantity-plus")) {
                quantity += 1;
            }

            quantityInput.value = quantity;

            updateCartItem(form);
        });
    });


    // ==============================
    // Remove Cart Items
    // ==============================

    const cartRemoveForms = document.querySelectorAll(".cart-remove-form");

    cartRemoveForms.forEach(function (form) {
        form.addEventListener("submit", function (event) {
            event.preventDefault();

            const cartItem = form.closest(".cart-item");

            if (!cartItem) {
                return;
            }

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

                    // Update cart total
                    const cartTotal = document.querySelector(
                        ".cart-summary h2"
                    );

                    if (cartTotal) {
                        cartTotal.textContent =
                            "Total: ₦" + data.cart_total;
                    }


                    // Update navbar cart count
                    updateCartCount(
                        data.cart_total_items
                    );


                    // If cart is empty, reload page
                    if (data.total_items === 0) {
                        window.location.reload();
                    }

                } else {
                    alert(
                        data.message ||
                        "Unable to remove this item."
                    );
                }

            })

            .catch(function (error) {

                console.error(
                    "Remove cart item error:",
                    error
                );

                alert(
                    "Something went wrong. Please try again."
                );
            });
        });
    });


    // ==============================
    // Add To Cart
    // ==============================

    const addToCartForms = document.querySelectorAll(
        ".add-to-cart-form"
    );

    addToCartForms.forEach(function (form) {

        form.addEventListener("submit", function (event) {

            event.preventDefault();

            const button = form.querySelector(
                "button[type='submit']"
            );

            const quantityInput = form.querySelector(
                "[name='quantity']"
            );

            const csrfToken = form.querySelector(
                "[name='csrfmiddlewaretoken']"
            ).value;

            const quantity = quantityInput.value;


            // Disable button while request is processing
            button.disabled = true;
            button.textContent = "Adding...";


            fetch(form.action, {

                method: "POST",

                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": csrfToken,
                    "Content-Type":
                        "application/x-www-form-urlencoded",
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

                    // Change button text
                    button.textContent = "Added ✓";


                    // Update navbar cart count
                    updateCartCount(
                        data.cart_total_items
                    );


                    // Change button back
                    setTimeout(function () {

                        button.textContent =
                            "Add to Cart";

                    }, 1500);

                } else {

                    alert(data.message);

                    button.textContent =
                        "Add to Cart";
                }

            })

            .catch(function (error) {

                console.error(
                    "Add to cart error:",
                    error
                );

                alert(
                    "Something went wrong. Please try again."
                );

                button.textContent =
                    "Add to Cart";

            })

            .finally(function () {

                button.disabled = false;

            });

        });

    });

});


// ==========================================
// Update Cart Item
// ==========================================

function updateCartItem(form) {

    const cartItem = form.closest(".cart-item");

    if (!cartItem) {
        return;
    }

    const quantityInput = form.querySelector(
        ".cart-quantity"
    );

    const itemTotal = cartItem.querySelector(
        ".cart-item-total"
    );

    const quantity = quantityInput.value;

    const csrfToken = form.querySelector(
        "[name=csrfmiddlewaretoken]"
    ).value;


    fetch(form.action, {

        method: "POST",

        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrfToken,
            "Content-Type":
                "application/x-www-form-urlencoded",
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

            // Update individual item total
            if (itemTotal) {
                itemTotal.textContent =
                    "₦" + data.item_total;
            }


            // Update cart total
            const cartTotal = document.querySelector(
                ".cart-summary h2"
            );

            if (cartTotal) {
                cartTotal.textContent =
                    "Total: ₦" + data.cart_total;
            }


            // Update navbar cart count
            updateCartCount(
                data.quantity
            );

        } else {

            alert(data.message);

        }

    })

    .catch(function (error) {

        console.error(
            "Cart update error:",
            error
        );

        alert(
            "Something went wrong. Please try again."
        );

    });
}


// ==========================================
// Update Navbar Cart Count
// ==========================================

function updateCartCount(totalItems) {

    let cartCount = document.getElementById(
        "cart-count"
    );


    // If there is no cart-count element yet,
    // do nothing for now.
    if (!cartCount) {
        return;
    }


    cartCount.textContent = totalItems;
}


// ==========================================
// Product Gallery
// ==========================================

function changeMainImage(image) {

    const mainImage = document.getElementById(
        "main-product-image"
    );

    if (mainImage) {

        mainImage.src = image.src;

        mainImage.alt = image.alt;

    }
}


// ==========================================
// Debug
// ==========================================

console.log("MAIN.JS LOADED");

