// Access webcam and display video feed
navigator.mediaDevices.getUserMedia({ video: true })
    .then(function(stream) {
        var video = document.getElementById('video');
        video.srcObject = stream;
        video.play();
    })
    .catch(function(err) {
        console.error('Error accessing webcam: ', err);
    });

// Capture picture from webcam and display the captured image
document.getElementById('captureButton').addEventListener('click', function() {
    var video = document.getElementById('video');
    var canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    var context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    var imageData = canvas.toDataURL('image/jpeg');

    // Display the captured image
    var capturedImage = document.createElement('img');
    capturedImage.src = imageData;
    capturedImage.width = 400; // Set width for display
    capturedImage.height = 300; // Set height for display
    document.getElementById('capturedImageContainer').innerHTML = ''; // Clear previous image
    document.getElementById('capturedImageContainer').appendChild(capturedImage);

    // Update hidden input with captured image data
    document.getElementById('photo').value = imageData;
});
