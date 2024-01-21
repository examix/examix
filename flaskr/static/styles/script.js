//TODO: Sanitize here

//Slider
document.addEventListener('DOMContentLoaded', function () {
    if (document.getElementById('customRange')) { 
        const rangeInput = document.getElementById('customRange');
        const difficultyValue = document.getElementById('difficultyValue');

        rangeInput.addEventListener('input', function () {
            const value = this.value;
            let message = '';

            if (value == 0) {
                message = 'Easy';
            } else if (value == 1) {
                message = 'Somewhat easy'
            } else if (value == 2) {
                message = 'Medium'
            } else if (value == 3) {
                message = 'Somewhat hard'
            } else {
                message = 'Hard'
            }

            difficultyValue.innerHTML = message;
        });
    }
});

//***Animation slide in
// JavaScript to add 'loaded' class to body when the page is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    document.body.classList.add('loaded');
});
