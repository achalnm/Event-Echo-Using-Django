var currentFilter = 'all';
var searchTimer = null;

function safeText(str) {
    var d = document.createElement('div');
    d.appendChild(document.createTextNode(String(str)));
    return d.innerHTML;
}

function buildCard(ev) {
    var img = ev.image_url
        ? '<img src="' + safeText(ev.image_url) + '" class="event-card-img" alt="' + safeText(ev.name) + '">'
        : '<div class="event-card-placeholder"><i class="bi bi-calendar-event"></i></div>';

    var price = ev.price === 0
        ? '<span class="badge-free">Free</span>'
        : '<span class="badge-price">$' + ev.price.toFixed(2) + '</span>';

    var avail = ev.is_full
        ? '<span class="badge-full">Full</span>'
        : '<span class="badge-spots">' + ev.spots_remaining + ' left</span>';

    return '<div class="col-md-4 mb-4">' +
        '<div class="event-card hover-rise"' +
        ' data-id="' + safeText(ev.id) + '"' +
        ' data-name="' + safeText(ev.name) + '"' +
        ' data-date="' + safeText(ev.date) + '"' +
        ' data-time=""' +
        ' data-location="' + safeText(ev.location) + '"' +
        ' data-description="' + safeText(ev.description) + '"' +
        ' data-price="' + ev.price + '"' +
        ' data-price-zero="' + (ev.price === 0 ? '1' : '0') + '"' +
        ' data-spots="' + ev.spots_remaining + '"' +
        ' data-full="' + (ev.is_full ? '1' : '0') + '"' +
        ' data-image="' + safeText(ev.image_url) + '"' +
        ' data-register-url="' + safeText(ev.register_url) + '"' +
        ' data-registered="' + (ev.is_registered ? '1' : '0') + '"' +
        ' style="opacity:0;transform:translateY(20px) scale(0.97);transition:opacity 0.45s ease,transform 0.45s cubic-bezier(0.34,1.56,0.64,1);">' +
        img +
        '<div class="event-card-body">' +
        '<div class="event-card-title">' + safeText(ev.name) + '</div>' +
        '<div class="event-meta"><i class="bi bi-calendar3"></i>' + safeText(ev.date) + '</div>' +
        '<div class="event-meta"><i class="bi bi-geo-alt"></i>' + safeText(ev.location) + '</div>' +
        '<div class="badges" style="margin-top:8px;">' + price + avail + '</div>' +
        '<p class="event-desc">' + safeText(ev.description) + '</p>' +
        '<div class="card-hint"><i class="bi bi-arrow-up-right-circle"></i>Click to view details</div>' +
        '</div></div></div>';
}

function animateNewCards() {
    document.querySelectorAll('#events-container .event-card').forEach(function (card, i) {
        setTimeout(function () {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0) scale(1)';
        }, i * 60);
    });
    if (typeof attachCardModals === 'function') {
        attachCardModals(document.getElementById('events-container'));
    }
}

function fetchEvents() {
    var inp = document.getElementById('search-input');
    var q = inp ? inp.value.trim() : '';
    var url = '/events/search/?q=' + encodeURIComponent(q) + '&filter=' + currentFilter;
    fetch(url)
        .then(function (r) { return r.json(); })
        .then(function (data) {
            var box = document.getElementById('events-container');
            if (!box) return;
            if (!data.events.length) {
                box.innerHTML = '<div class="col-12" style="padding:36px 0;"><p style="color:var(--ink-3);">No events found.</p></div>';
                return;
            }
            box.innerHTML = data.events.map(buildCard).join('');
            animateNewCards();
        });
}

document.addEventListener('DOMContentLoaded', function () {
    var inp = document.getElementById('search-input');
    if (inp) {
        inp.addEventListener('input', function () {
            clearTimeout(searchTimer);
            searchTimer = setTimeout(fetchEvents, 280);
        });
    }
    document.querySelectorAll('.filter-pill').forEach(function (btn) {
        btn.addEventListener('click', function () {
            document.querySelectorAll('.filter-pill').forEach(function (b) { b.classList.remove('active'); });
            this.classList.add('active');
            currentFilter = this.dataset.filter;
            fetchEvents();
        });
    });
});
