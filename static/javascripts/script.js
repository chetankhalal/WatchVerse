window.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('.nav-item');

    // Normalize current path
    const currentUrl = new URL(window.location.href);
    let currentPath = currentUrl.pathname.replace(/\/$/, '');

    navLinks.forEach(link => {
        const linkUrl = new URL(link.href, window.location.origin);
        let linkPath = linkUrl.pathname.replace(/\/$/, '');

        // Case 1: Exact match
        if (currentPath === linkPath) {
            link.classList.add('active');
            return;
        }

        // Case 2: Partial match (for nested routes)
        if (currentPath.startsWith(linkPath + '/')) {
            link.classList.add('active');
            return;
        }

        // Case 3: Query param match (optional strict match)
        if (currentPath === linkPath && currentUrl.search === linkUrl.search) {
            link.classList.add('active');
        }
    });
});

const cards = document.querySelectorAll('.mega-card');

cards.forEach(card => {
    const target = card.querySelector('.hover-card');
    const trigger = card.querySelector('.card')
    // IMPORTANT: hover-card should be INSIDE each card

    card.addEventListener('mouseenter', () => {
        target.style.display = 'block';
        trigger.style.display = 'none';
    });

    card.addEventListener('mouseleave', () => {
        // small delay prevents flicker
        setTimeout(() => {
            if (!card.matches(':hover')) {
                target.style.display = 'none';
                trigger.style.display = 'block';
            }
        }, 50);
    });
});