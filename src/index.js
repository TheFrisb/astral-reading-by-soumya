import {initMobileMenu} from './components/mobileMenu';
import {initTestimonialSwiper} from "./components/testimonialSwiper";
import {initFaq} from "./components/frequently_asked_questions";
import {initHoroscopeFrequencyFilterButtons} from "./components/initHoroscopeFrequencyFilterButtons";
import {initCheckout} from "./components/checkout";
import {initBooking} from "./components/booking/booking";
import {initReviewFormStarRating} from "./components/review_form/starRating";
import {initAppointmentTime} from "./components/appointmentTime";

document.addEventListener('DOMContentLoaded', () => {
  initMobileMenu();
  initTestimonialSwiper();
  initFaq();
  initHoroscopeFrequencyFilterButtons();
  initCheckout();
  initBooking();
  initReviewFormStarRating('starRatingContainer', 'rating');
  initAppointmentTime();
});
