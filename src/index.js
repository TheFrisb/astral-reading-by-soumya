import {initMobileMenu} from './components/mobileMenu';
import {initTestimonialSwiper} from "./components/testimonialSwiper";
import {initFaq} from "./components/frequently_asked_questions";
import {initHoroscopeFrequencyFilterButtons} from "./components/initHoroscopeFrequencyFilterButtons";
import {initCheckout} from "./components/checkout";
import {initBooking} from "./components/booking/booking";

document.addEventListener('DOMContentLoaded', () => {
  initMobileMenu();
  initTestimonialSwiper();
  initFaq();
  initHoroscopeFrequencyFilterButtons();
  initCheckout();
  initBooking();
});
