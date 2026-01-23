document.getElementById("imageInput").addEventListener("change", function (event) {
    const [file] = event.target.files;
    if (file) {
      const preview = document.getElementById("imagePreview");
      preview.src = URL.createObjectURL(file);
      preview.style.display = "block";
    }
  });