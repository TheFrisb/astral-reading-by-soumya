document.addEventListener('DOMContentLoaded', () => {
  const menuIcon = document.getElementById('mobileMenuIcon');
  const closeIcon = document.getElementById('mobileMenuCloseIcon');
  const mobileMenu = document.getElementById('mobileMenu');

  menuIcon.addEventListener('click', () => {
    mobileMenu.classList.remove('opacity-0', 'max-h-0', 'scale-y-0');
    mobileMenu.classList.add('opacity-100', 'max-h-screen', 'scale-y-100', 'p-2');

    menuIcon.classList.add('hidden');
    closeIcon.classList.remove('hidden');
  });

  closeIcon.addEventListener('click', () => {
    mobileMenu.classList.add('opacity-0', 'max-h-0', 'scale-y-0');
    mobileMenu.classList.remove('opacity-100', 'max-h-screen', 'scale-y-100', 'p-2');

    closeIcon.classList.add('hidden');
    menuIcon.classList.remove('hidden');
  });
}); 