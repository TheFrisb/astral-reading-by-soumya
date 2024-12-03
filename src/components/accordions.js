export function initAccordions() {
  const accordions = document.querySelectorAll('.accordion');

  if (!accordions.length) return;

  accordions.forEach(elm => {
    const button = elm.querySelector('.toggle-button');
    const content = elm.querySelector('.content');
    const plusIcon = button.querySelector('.plus');

    if (!button || !content || !plusIcon) return;

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
}
