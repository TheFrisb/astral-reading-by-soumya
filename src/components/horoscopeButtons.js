export function initHoroscopeButtons() {
  const buttons = document.querySelectorAll('.chooseHoroscopeButton');
  const horoscopeSections = document.querySelectorAll('[data-horoscope-type]');

  if (!buttons.length || !horoscopeSections.length) return;

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
}
