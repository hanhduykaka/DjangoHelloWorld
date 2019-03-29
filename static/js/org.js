function readURL(input) {

    var files = event.target.files; // FileList object
    // Loop through the FileList and render image files as thumbnails
    for (var i = 0, f; f = files[i]; i++) {
        // Only process image files
        if (!f.type.match('image.*')) continue;
        // Init FileReader()
        // See: https://developer.mozilla.org/en-US/docs/Web/API/FileReader
        var reader = new FileReader();
        // Closure to capture the file information
        reader.onload = (function() {
            return function(e) {
                // Render background image
                document.getElementById('preview_image').style.background = 'url(' + e.target.result + ') no-repeat center center';
                document.getElementById('preview_image').style.backgroundSize = 'cover';
                // Set `display: block` to preview image container
                document.getElementById('preview_image').style.display = 'block';
            };
        })(f);
        // Read in the image file as a data URL
        reader.readAsDataURL(f);
    }
}
(function() {
    document.getElementById("id_Image").addEventListener('change', readURL);
})();