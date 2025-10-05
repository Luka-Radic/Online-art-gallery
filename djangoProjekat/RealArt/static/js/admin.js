document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('searchInput');
    const boxes = document.querySelectorAll('.request-box');

    const inputDelete = document.getElementById('paintingSearch');
    const pictures = document.querySelectorAll('.photo-box');

    const commentSearch = document.getElementById('commentSearchInput');
    const comms = document.querySelectorAll('.comment-box');

    input.addEventListener('input', function () {
        const query = this.value.toLowerCase();

        boxes.forEach(box => {
            const username = box.dataset.username || '';
            const match = username.startsWith(query);
            box.classList.toggle('hidden', !match);
        });
    });
    inputDelete.addEventListener('input', function () {
        const query = this.value.toLowerCase();

        pictures.forEach(pict => {
            const title = pict.dataset.title || '';
            const match = title.startsWith(query);
            console.log(query);
            console.log(title);
            pict.classList.toggle('hidden', !match);
        });
    });

    commentSearch.addEventListener('input', function () {
        const query = this.value.toLowerCase();
        comms.forEach(comment => {
            const content = comment.dataset.content || '';
            const username = comment.dataset.username || '';
            const match = username.startsWith(query) || content.startsWith(query);
            comment.classList.toggle('hidden', !match);
        });
    });

});

document.querySelectorAll('.photo-box form').forEach(form => {
    form.addEventListener('submit', e => {
        if (!confirm('Da li ste sigurni da želite da obrišete ovu fotografiju?')) {
            e.preventDefault();
        }
    });
});

