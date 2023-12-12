document.addEventListener('DOMContentLoaded', function() {
    const videoFileInput = document.getElementById('videoFile');
    const selectedVideo = document.getElementById('selectedVideo');
    let selectedFile = null;

    videoFileInput.addEventListener('change', function() {
        const file = videoFileInput.files[0];

        if (file) {
            // Check if the selected file is a video (you can add more video formats if needed)
            if (file.type.startsWith('video/')) {
                selectedFile = file;
                const fileName = selectedFile.name;
                selectedVideo.textContent = `Selected Video: ${fileName}`;
            } else {
                selectedVideo.textContent = 'Please select a valid video file.';
                selectedFile = null;
                videoFileInput.value = ''; // Clear the input field
            }
        } else {
            selectedVideo.textContent = 'No video selected';
        }
    });

    // Handle the storage of the selected video file (you can replace this with your storage logic)
    const uploadButton = document.getElementById('uploadButton');
    uploadButton.addEventListener('click', function() {
        if (selectedFile) {
            // Here, you can upload/store the 'selectedFile'
            // Replace this with your actual storage logic (e.g., sending the file to a server).
            console.log('Uploading the selected video file:', selectedFile);
            // Reset the selection after storage (if needed)
            selectedFile = null;
            videoFileInput.value = '';
            selectedVideo.textContent = 'No video selected';
        } else {
            selectedVideo.textContent = 'Please select a valid video file.';
        }
    });
});
