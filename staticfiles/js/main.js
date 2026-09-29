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