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
            const titleText = titleEl ? titleEl.textContent.toLowerCase() : '';

            // Čitanje statusa direktno iz baze
            const cardStatus = card.dataset.status; // "active", "closed" ili drugo

            const matchesQuery = titleText.includes(query);

            const matchesStatus =
                status === 'sve' ||
                (status === 'active' && cardStatus === 'active') ||
                (status === 'closed' && cardStatus === 'closed');

            card.style.display = (matchesQuery && matchesStatus) ? '' : 'none';
        });
    }

    searchInput.addEventListener('input', filterIzlozbe);
    statusFilter.addEventListener('change', filterIzlozbe);
});