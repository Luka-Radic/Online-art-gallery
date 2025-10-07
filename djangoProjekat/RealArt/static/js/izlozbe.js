function toggleFormu() {
    const forma = document.getElementById("forma-izlozba");
    if (forma.style.display === "none" || forma.style.display === "") {
        forma.style.display = "block";
        forma.scrollIntoView({behavior: "smooth"});
    } else {
        forma.style.display = "none";
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchIzlozbe');
    const statusFilter = document.getElementById('statusFilter');
    const izlozbeCards = document.querySelectorAll('.row.g-4 > .col-md-6');

    function filterIzlozbe() {
        const query = searchInput.value.toLowerCase();
        const status = statusFilter.value;

        izlozbeCards.forEach(card => {
            const titleEl = card.querySelector('.card-title');
            const statusEl = card.querySelector('p.text-muted');

            const titleText = titleEl ? titleEl.textContent.toLowerCase() : '';
            const statusText = statusEl ? statusEl.textContent.toLowerCase() : '';

            const matchesQuery = titleText.includes(query);
            const matchesStatus =
                status === 'sve' ||
                (status === 'active' && statusText.includes('aktivna')) ||
                (status === 'closed' && statusText.includes('zatvorena'));

            if (matchesQuery && matchesStatus) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });
    }

    searchInput.addEventListener('input', filterIzlozbe);
    statusFilter.addEventListener('change', filterIzlozbe);
});