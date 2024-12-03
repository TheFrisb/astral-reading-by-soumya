import Glide from '@glidejs/glide';

export function initCarousel() {
  if (!document.querySelector('.glide')) return;

  new Glide('.glide', {
    type: 'carousel',
    startAt: 0,
    perView: 3,
    focusAt: 'center',
    autoplay: 3000,
    breakpoints: {
      1024: {
        perView: 2,
      },
      768: {
        perView: 1,
      },
    },
  }).mount();
}
