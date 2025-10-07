document.addEventListener('DOMContentLoaded', () => {
    const stars = document.querySelectorAll('#starRating .star');
    const ratingValue = document.getElementById('ratingValue');
    let currentRating = 0;

    stars.forEach(star => {
        star.addEventListener('click', () => {
            const value = parseInt(star.dataset.value);
            currentRating = (currentRating === value) ? 0 : value;
            updateStars();
            ratingValue.textContent = currentRating > 0 ? `${currentRating}/5` : "0/5";
        });

        star.addEventListener('mouseover', () => {
            const value = parseInt(star.dataset.value);
            highlightStars(value);
        });

        star.addEventListener('mouseout', () => {
            updateStars();
        });
    });

    function updateStars() {
        stars.forEach(star => {
            const value = parseInt(star.dataset.value);
            star.style.color = value <= currentRating ? 'gold' : '#ccc';
        });
    }

    function highlightStars(value) {
        stars.forEach(star => {
            const val = parseInt(star.dataset.value);
            star.style.color = (val <= value) ? 'gold' : '#ccc';
        });
    }
});