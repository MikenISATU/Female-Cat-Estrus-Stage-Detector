document.addEventListener('DOMContentLoaded', function() {
    const videoFileInput = document.getElementById('videoFile');
    const uploadButton = document.getElementById('uploadButton');
    const selectedVideo = document.getElementById('selectedVideo');

    uploadButton.addEventListener('click', function() {
        videoFileInput.click(); // Trigger the file input field when the button is clicked
    });

    videoFileInput.addEventListener('change', function() {
        const fileName = videoFileInput.files[0].name;
        selectedVideo.textContent = `Selected Video: ${fileName}`;
    });
});
