export function initFaq() {
  const faqTogglerButtons = document.querySelectorAll('.faqTogglerButton');

  if (faqTogglerButtons.length === 0) {
    return;
  }

  faqTogglerButtons.forEach(button => {

    button.addEventListener('click', () => {
      const icon = button.querySelector('.faqTogglerButtonIcon');
      const content = button.nextElementSibling;

      if (button.classList.contains('active')) {
        button.classList.remove('active');
        icon.classList.remove('rotate-180');
        content.classList.add('max-h-0', 'opacity-0');

      } else {
        button.classList.add('active');
        icon.classList.add('rotate-180');
        content.classList.remove('max-h-0', 'opacity-0');
      }
    });
  });
}