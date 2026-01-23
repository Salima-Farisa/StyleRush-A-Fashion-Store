document.addEventListener("DOMContentLoaded", function () {
  const plusButtons = document.querySelectorAll(".btn-qty.plus");
  const minusButtons = document.querySelectorAll(".btn-qty.minus");

  plusButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      const input = btn.parentElement.querySelector(".qty-input");
      input.value = parseInt(input.value) + 1;
      // Optionally: send AJAX to update cart
    });
  });

  minusButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      const input = btn.parentElement.querySelector(".qty-input");
      if (parseInt(input.value) > 1) {
        input.value = parseInt(input.value) - 1;
        // Optionally: send AJAX to update cart
      }
    });
  });
});

