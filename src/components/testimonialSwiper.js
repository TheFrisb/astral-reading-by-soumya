import Swiper from "swiper";

export function initTestimonialSwiper() {

  if (!document.querySelector('.testimonials-swiper')) return;

  let swiper = new Swiper('.testimonials-swiper', {
    slidesPerView: 1,
    spaceBetween: 30,
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    autoplay: {
      delay: 5000,
      disableOnInteraction: false,
    },
    loop: true,
    breakpoints: {
      640: {
        slidesPerView: 2,
      },
      1024: {
        slidesPerView: 3,
      }
    }
  });


  const left_arrow = document.querySelector('.swiper-button-prev');
  const right_arrow = document.querySelector('.swiper-button-next');

  left_arrow.addEventListener('click', () => {
    swiper.slidePrev();
  });

  right_arrow.addEventListener('click', () => {
    swiper.slideNext();
  });
}