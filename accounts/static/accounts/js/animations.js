document.addEventListener('DOMContentLoaded', function () {

    var strip = document.getElementById('performer-strip');
    var prevBtn = document.getElementById('perf-prev');
    var nextBtn = document.getElementById('perf-next');
    if (strip && nextBtn) nextBtn.addEventListener('click', function () { strip.scrollBy({ left: 280, behavior: 'smooth' }); });
    if (strip && prevBtn) prevBtn.addEventListener('click', function () { strip.scrollBy({ left: -280, behavior: 'smooth' }); });

    if (typeof IntersectionObserver !== 'undefined') {
        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry, i) {
                if (entry.isIntersecting) {
                    var el = entry.target;
                    setTimeout(function () {
                        el.style.opacity = '1';
                        el.style.transform = 'translateY(0) scale(1)';
                    }, i * 60);
                    io.unobserve(el);
                }
            });
        }, { threshold: 0.06 });

        document.querySelectorAll('.event-card').forEach(function (card) {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px) scale(0.97)';
            card.style.transition = 'opacity 0.45s ease, transform 0.45s cubic-bezier(0.34,1.56,0.64,1)';
            io.observe(card);
        });
    }

    attachCardModals(document);
});

function attachCardModals(root) {
    var modalEl = document.getElementById('eventModal');
    if (!modalEl) return;

    root.querySelectorAll('.event-card[data-id]').forEach(function (card) {
        card.addEventListener('click', function (e) {
            if (e.target.closest('a') || e.target.closest('button')) return;
            openEventModal(this);
        });
    });
}

function openEventModal(card) {
    var d = card.dataset;
    document.getElementById('modal-name').textContent     = d.name || '';
    document.getElementById('modal-date').textContent     = d.date || '';
    document.getElementById('modal-time').textContent     = d.time || '';
    document.getElementById('modal-location').textContent = d.location || '';
    document.getElementById('modal-desc').textContent     = d.description || '';

    var imgWrap = document.getElementById('modal-img-wrap');
    var img     = document.getElementById('modal-img');
    if (d.image) {
        img.src = d.image;
        imgWrap.style.display = 'block';
    } else {
        imgWrap.style.display = 'none';
    }

    var badgesEl = document.getElementById('modal-badges');
    badgesEl.innerHTML = '';
    if (d.priceZero === '1') {
        badgesEl.innerHTML += '<span class="badge-free">Free</span>';
    } else {
        badgesEl.innerHTML += '<span class="badge-price">$' + (d.price || '0') + '</span>';
    }
    if (d.full === '1') {
        badgesEl.innerHTML += '<span class="badge-full">Fully Booked</span>';
    } else {
        badgesEl.innerHTML += '<span class="badge-spots">' + (d.spots || '0') + ' spots left</span>';
    }

    var regBtn = document.getElementById('modal-register-btn');
    if (d.registered === '1') {
        regBtn.textContent = 'Already Registered';
        regBtn.className = 'btn-outline';
        regBtn.removeAttribute('href');
        regBtn.style.pointerEvents = 'none';
    } else if (d.full === '1') {
        regBtn.textContent = 'Fully Booked';
        regBtn.className = 'btn-outline';
        regBtn.removeAttribute('href');
        regBtn.style.pointerEvents = 'none';
    } else {
        regBtn.textContent = 'Register';
        regBtn.className = 'btn-primary';
        regBtn.href = d.registerUrl || '#';
        regBtn.style.pointerEvents = '';
    }

    var modal = new bootstrap.Modal(document.getElementById('eventModal'));
    modal.show();
}
