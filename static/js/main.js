document.addEventListener('DOMContentLoaded', () => {
  const menuIcon = document.getElementById('mobileMenuIcon');
  const closeIcon = document.getElementById('mobileMenuCloseIcon');
  const mobileMenu = document.getElementById('mobileMenu');

  const buttons = document.querySelectorAll('.chooseHoroscopeButton');
  const horoscopeSections = document.querySelectorAll('[data-horoscope-type]');

  const accordions = document.querySelectorAll('.accordion');

  buttons.forEach(button => {
    button.addEventListener('click', () => {
      // Remove the active class from all buttons
      buttons.forEach(btn => btn.classList.remove('active'));
      // Add the active class to the clicked button
      button.classList.add('active');

      // Get the horoscope type to show
      const typeToShow = button.getAttribute('data-show-horoscope-type');

      // Show the appropriate horoscopes
      horoscopeSections.forEach(section => {
        if (section.getAttribute('data-horoscope-type') === typeToShow) {
          section.classList.remove('!hidden');
        } else {
          section.classList.add('!hidden');
        }
      });
    });
  });

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

  accordions.forEach(elm => {
    const button = elm.querySelector('.toggle-button');
    const content = elm.querySelector('.content');
    const plusIcon = button.querySelector('.plus');

    button.addEventListener('click', () => {
      const isHidden = content.classList.toggle('invisible');
      content.style.maxHeight = isHidden ? '0px' : `${content.scrollHeight + 100}px`;
      button.classList.toggle('text-blue-600', !isHidden);
      button.classList.toggle('text-gray-800', isHidden);
      content.classList.toggle('pb-6', !isHidden);
      plusIcon.classList.toggle('hidden', !isHidden);
      plusIcon.classList.toggle('block', isHidden);
    });
  });

  new Glide('.glide', {
    type: 'carousel',
    startAt: 0,
    perView: 3, // Number of slides visible
    focusAt: 'center', // Focus the active slide in the center
    autoplay: 3000, // Autoplay every 3 seconds
    breakpoints: {
      768: {
        perView: 1 // On small screens, show 1 slide at a time
      },
      1024: {
        perView: 2 // On medium screens, show 2 slides
      }
    }
  }).mount();


});