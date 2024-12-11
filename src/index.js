import {initMobileMenu} from './components/mobileMenu';
import {initTestimonialSwiper} from "./components/testimonialSwiper";
import {initFaq} from "./components/frequently_asked_questions";
import {initHoroscopeFrequencyFilterButtons} from "./components/initHoroscopeFrequencyFilterButtons";

document.addEventListener('DOMContentLoaded', () => {
  initMobileMenu();
  initTestimonialSwiper();
  initFaq();
  initHoroscopeFrequencyFilterButtons();
});
