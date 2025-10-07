document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('gallerySearchInput');
    const searchFilter = document.getElementById('searchFilter');
    const galleryItems = document.querySelectorAll('.gallery-item');

    const filterGallery = () => {
        const query = searchInput.value.toLowerCase().trim();
        const filterBy = searchFilter.value;

        galleryItems.forEach(item => {
            const artist = item.dataset.artist || '';
            const title = item.dataset.title || '';
            const themeRaw = item.dataset.theme || '';
            const themes = themeRaw.split(',').map(t => t.trim());

            let matches = false;

            if (filterBy === 'artist') {
                matches = artist.startsWith(query);
            } else if (filterBy === 'title') {
                matches = title.startsWith(query);
            } else if (filterBy === 'theme') {
                matches = themes.some(t => t.startsWith(query));
            }

            item.classList.toggle('hidden', !matches);
        });
    };

    searchInput.addEventListener('input', filterGallery);

    searchFilter.addEventListener('change', filterGallery);
});