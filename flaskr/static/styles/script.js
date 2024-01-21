//TODO: Sanitize here

//Slider
document.addEventListener('DOMContentLoaded', function () {
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
});