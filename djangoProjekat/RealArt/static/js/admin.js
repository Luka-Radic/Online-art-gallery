document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('searchInput');
    const boxes = document.querySelectorAll('.request-box');

    input.addEventListener('input', function () {
        const query = this.value.toLowerCase();

        boxes.forEach(box => {
            const username = box.dataset.username || '';
            const match = username.startsWith(query);
            box.classList.toggle('hidden', !match);
        });
    });
});