document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    const searchFilter = document.getElementById('searchFilter');
    const paintingCards = document.querySelectorAll('.painting-card');

    const filterPaintings = () => {
        const query = searchInput.value.toLowerCase().trim();
        const filterBy = searchFilter.value;

        paintingCards.forEach(card => {
            const artist = card.dataset.artist || '';
            const title = card.dataset.title || '';

            let matches = false;

            if (filterBy === 'artist') {
                matches = artist.startsWith(query);
            } else if (filterBy === 'title') {
                matches = title.startsWith(query);
            }

            card.classList.toggle('hidden', !matches);
        });
    };

    searchInput.addEventListener('input', filterPaintings);
    searchFilter.addEventListener('change', filterPaintings);
});