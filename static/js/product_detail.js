document.getElementById("add-to-cart-btn").addEventListener("click", function(e) {
    e.preventDefault();  // prevent redirect

    let variantId = document.getElementById("selected_variant").value;

    if (!variantId) {
        alert("Please select both color and size before adding to cart.");
        return;
    }

    // send user to backend
    window.location.href = `/cart/add/${variantId}/`;
});

// BUY NOW BTN — optional
document.getElementById("buy-now-btn")?.addEventListener("click", function(e) {
    e.preventDefault();

    let variantId = document.getElementById("selected_variant").value;

    if (!variantId) {
        alert("Please select both color and size before buying.");
        return;
    }

    window.location.href = `/checkout/${variantId}/`;
});
