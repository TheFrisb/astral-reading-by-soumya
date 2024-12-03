import {initMobileMenu} from './components/mobileMenu';
import {initHoroscopeButtons} from './components/horoscopeButtons';
import {initAccordions} from './components/accordions';
import {initCarousel} from './components/carousel';

document.addEventListener('DOMContentLoaded', () => {
  initMobileMenu();
  initHoroscopeButtons();
  initAccordions();
  initCarousel();
});
