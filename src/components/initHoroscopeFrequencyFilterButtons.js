export function initHoroscopeFrequencyFilterButtons() {
  const horoscopeFilterButtons = document.querySelectorAll('.horoscopeFilterButton');
  const monthlyHoroscopes = document.querySelectorAll('.horoscopeCard[data-frequency="monthly"]');
  const yearlyHoroscopes = document.querySelectorAll('.horoscopeCard[data-frequency="yearly"]');

  if (horoscopeFilterButtons.length === 0) {
    return;
  }

  horoscopeFilterButtons.forEach(button => {
    button.addEventListener('click', () => {
      const activeButton = document.querySelector('.horoscopeFilterButton.active');
      activeButton.classList.remove('active');
      button.classList.add('active');

      const frequency = button.getAttribute('data-frequency');

      if (frequency === 'monthly') {
        console.log('Showing monthly horoscopes');
        yearlyHoroscopes.forEach(horoscope => {
          horoscope.classList.add('!hidden')
        });
        monthlyHoroscopes.forEach(horoscope => {
          horoscope.classList.remove('!hidden')
        });
      } else {
        console.log('Showing yearly horoscopes');
        monthlyHoroscopes.forEach(horoscope => {
          horoscope.classList.add('!hidden')
        });
        yearlyHoroscopes.forEach(horoscope => {
          horoscope.classList.remove('!hidden')
        });
      }
    });
  });
}