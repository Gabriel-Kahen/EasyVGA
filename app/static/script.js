function updateImageWidth(value) {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/set_width", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 204) {
            console.log("Image Width updated to: " + value);
        }
    };
    xhr.send("image_width=" + value);
}