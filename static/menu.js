function toggleMobileNav() {
    var overlayNav = document.querySelector('.overlay-nav');
    var desktopNav = document.querySelector('.desktop-nav');

    if (overlayNav.style.width === '50%') {
        overlayNav.style.width = '0';
        document.body.classList.remove('mobile-nav-active');
    } else {
        overlayNav.style.width = '50%';
        document.body.classList.add('mobile-nav-active');
    }
}
