document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');
    const searchFilter = document.getElementById('searchFilter');
    const container = document.getElementById('paintingsContainer');
    const sortLinks = document.querySelectorAll('.dropdown-item');

    const getFilteredCards = () => {
        const query = searchInput.value.toLowerCase().trim();
        const filterBy = searchFilter.value;
        const cards = Array.from(container.querySelectorAll('.painting-card'));

        return cards.map(card => {
            const artist = card.dataset.artist || '';
            const title = card.dataset.title || '';
            let matches = false;

            if (filterBy === 'artist') {
                matches = artist.startsWith(query);
            } else if (filterBy === 'title') {
                matches = title.startsWith(query);
            }

            card.classList.toggle('hidden', !matches);
            return card;
        });
    };

    searchInput.addEventListener('input', getFilteredCards);
    searchFilter.addEventListener('change', getFilteredCards);

    sortLinks.forEach(link => {
        link.addEventListener('click', e => {
            e.preventDefault();
            const type = e.target.textContent.trim();

            let cards = Array.from(container.querySelectorAll('.painting-card'));

            // Remove hidden class before sorting
            cards.forEach(card => card.classList.remove('hidden'));

            if (type === 'Sortiraj po umetniku') {
                cards.sort((a, b) => a.dataset.artist.localeCompare(b.dataset.artist));
            } else if (type === 'Sortiraj po oceni') {
                cards.sort((a, b) => parseFloat(b.dataset.rating || 0) - parseFloat(a.dataset.rating || 0));
            } else if (type === 'Najnovije') {
                cards.sort((a, b) => parseInt(b.dataset.timestamp || 0) - parseInt(a.dataset.timestamp || 0));
            }

            // Re-render
            container.innerHTML = '';
            cards.forEach(card => container.appendChild(card));

            // Re-apply filter after sorting
            getFilteredCards();
        });
    });
});