export function initMobileMenu() {
  const mobileMenuTogglerButtons = document.querySelectorAll('.mobileMenuTogglerButton');
  const mobileMenu = document.getElementById('mobileMenu');
  const overlay = document.getElementById('overlay');

  if (!mobileMenu || !overlay || mobileMenuTogglerButtons.length === 0) {
    return;
  }

  mobileMenuTogglerButtons.forEach((button) => {
    button.addEventListener('click', () => {
      if (mobileMenu.classList.contains('active')) {
        mobileMenu.classList.remove('active');
        overlay.classList.remove('active');

        mobileMenu.classList.add('mobile-menu-exit');
        overlay.classList.add('mobile-menu-overlay-exit');

        setTimeout(() => {
          mobileMenu.classList.remove('mobile-menu-exit');
          overlay.classList.remove('mobile-menu-overlay-exit');
        }, 300);
      } else {
        console.log("clicked")
        mobileMenu.classList.add('active');
        overlay.classList.add('active');

        mobileMenu.classList.add('mobile-menu-enter');
        overlay.classList.add('mobile-menu-overlay-enter');

        requestAnimationFrame(() => {
          mobileMenu.classList.add('mobile-menu-enter-active');
          overlay.classList.add('mobile-menu-overlay-enter-active');
        });

        setTimeout(() => {
          mobileMenu.classList.remove('mobile-menu-enter', 'mobile-menu-enter-active');
          overlay.classList.remove('mobile-menu-overlay-enter', 'mobile-menu-overlay-enter-active');
        }, 300);
      }
    });
  });
}