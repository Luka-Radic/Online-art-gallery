document.addEventListener('DOMContentLoaded', () => {
    const stars = document.querySelectorAll('.star-rating .star');

    function removeHover() {
        stars.forEach(s => s.classList.remove('hovered'));
    }

    stars.forEach((star, index) => {
        star.addEventListener('mouseenter', () => {
            removeHover();
            for (let i = 0; i <= index; i++) {
                if (!stars[i].classList.contains('filled')) {
                    stars[i].classList.add('hovered');
                }
            }
        });

        star.addEventListener('mouseleave', () => {
            removeHover();
        });

        star.addEventListener('click', () => {
            const score = index + 1;
            stars.forEach((s, i) => {
                if (i < score) {
                    s.classList.add('filled');
                    s.classList.remove('hovered');
                } else {
                    s.classList.remove('filled');
                }
            });
        });
    });
});