document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('searchInput').addEventListener('input', function () {
        const input = this.value.toLowerCase();
        const cards = document.querySelectorAll('.painting-card');

        cards.forEach(card => {
            const title = card.dataset.title;
            const artist = card.dataset.artist;
            console.log(title);
            console.log(artist);
            console.log(input);
            const match = title.startsWith(input) || artist.startsWith(input);
            card.classList.toggle('hidden', !match);
        });
    });

    const sortLinks = document.querySelectorAll('.dropdown-item');
    const container = document.getElementById('paintingsContainer');

    sortLinks.forEach(link => {
        link.addEventListener('click', e => {
            e.preventDefault();
            const type = e.target.textContent.trim();

            const cards = Array.from(container.querySelectorAll('.painting-card'));

            let sorted = [];

            if (type === 'Sortiraj po umetniku') {
                sorted = cards.sort((a, b) => {
                    return a.dataset.artist.localeCompare(b.dataset.artist);
                });
            } else if (type === 'Sortira po oceni') {
                sorted = cards.sort((a, b) => {
                    return parseFloat(b.dataset.rating || 0) - parseFloat(a.dataset.rating || 0);
                });
            } else if (type === 'Najnovije') {
                sorted = cards.sort((a, b) => {
                    return parseInt(b.dataset.timestamp || 0) - parseInt(a.dataset.timestamp || 0);
                });
            }

            // Re-render
            container.innerHTML = '';
            sorted.forEach(card => container.appendChild(card));
        });
    });
});

