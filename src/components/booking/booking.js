import {Datepicker} from "vanillajs-datepicker";

export function initBooking() {
  const datePickerInput = document.querySelector('#queryTimeSlotsInput');
  const timeSlotsParent = document.querySelector('#timeSlotsParent');
  const timeSlotsContainer = document.querySelector('#timeSlotsContainer');
  const timeSlotsChosenDay = document.querySelector('#timeSlotsChosenDayContainer');
  const orderIdInput = document.querySelector('#orderIdInput');
  const submitButton = document.querySelector('#submitTimeSlotButton');


  if (!datePickerInput) {
    return;
  }

  let selectedSlot = null;

  const orderId = orderIdInput.value;
  const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

  // get min date = current date + 1 week
  const minDate = new Date();
  minDate.setDate(minDate.getDate() + 7);

  const datepicker = new Datepicker(datePickerInput, {
    buttonClass: 'btn',
    autohide: true,
    clearBtn: false,
    format: 'yyyy-mm-dd',
    minDate: minDate,
    showDaysOfWeek: true,
  });


  // Add event listener to fetch time slots when a date is selected
  datePickerInput.addEventListener('changeDate', (e) => {

    const chosenDate = new Date(e.detail.date);
    console.log(chosenDate);

    const year = chosenDate.getFullYear();
    const month = String(chosenDate.getMonth() + 1).padStart(2, '0'); // Months are 0-based
    const day = String(chosenDate.getDate()).padStart(2, '0');
    const chosenDateFormatted = `${year}-${month}-${day}`;

    // Fetch time slots for the selected date
    fetchTimeSlots(orderId, chosenDateFormatted)
      .then((timeSlots) => {
        renderTimeSlots(timeSlots, timeSlotsContainer, timeSlotsChosenDay, chosenDateFormatted, userTimezone);
      })
      .catch((err) => {
        console.error('Error fetching time slots:', err);
        timeSlotsContainer.innerHTML = '<p class="error">No time slots available for the selected date</p>';
      });
  });

  /**
   * Fetch available time slots from the server.
   *
   * @param {string} orderId - The ID of the order.
   * @param {string} date - The selected date in YYYY-MM-DD format.
   * @param {string} timezone - The user's timezone.
   * @returns {Promise<Object[]>} A promise that resolves with the available time slots.
   */
  function fetchTimeSlots(orderId, date) {
    return fetch(`/booking/get-time-slots/?order_id=${orderId}&date=${date}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Failed to fetch time slots: ${response.statusText}`);
        }
        return response.json();
      })
      .then((data) => data.available_timeslots);
  }

  /**
   * Render available time slots under the specified container.
   *
   * @param {Object[]} timeSlots - The list of available time slots.
   * @param {HTMLElement} container - The container to render the time slots in.
   * @param {HTMLElement} chosenDayContainer - The element to display the chosen date.
   * @param {string} chosenDate - The chosen date in YYYY-MM-DD format.
   * @param {string} userTimezone - The user's local timezone.
   */
  function renderTimeSlots(timeSlots, container, chosenDayContainer, chosenDate, userTimezone) {
    // Clear existing time slots
    container.innerHTML = '';

    // Update the chosen date display
    chosenDayContainer.innerText = chosenDate;

    if (!timeSlots || timeSlots.length === 0) {
      container.innerHTML = '<p>No available time slots for this day.</p>';
      return;
    }

    // Render each time slot in the user's local timezone
    timeSlots.forEach((slot) => {
      const startTime = new Date(slot.start).toLocaleTimeString('en-US', {
        timeZone: userTimezone,
        hour: '2-digit',
        minute: '2-digit',
      });
      const endTime = new Date(slot.end).toLocaleTimeString('en-US', {
        timeZone: userTimezone,
        hour: '2-digit',
        minute: '2-digit',
      });

      const slotButton = document.createElement('button');
      slotButton.className =
        'p-4 rounded-lg text-sm font-medium transition-colors relative hover:scale-105 transform duration-200 bg-purple-50 text-purple-700 hover:bg-purple-100 hover:shadow slotButton';
      slotButton.textContent = `${startTime} - ${endTime}`;

      // add startTime and end time to the button
      slotButton.setAttribute('data-start-time', slot.start);
      slotButton.setAttribute('data-end-time', slot.end);

      // Optionally, add event listeners for interactions
      slotButton.addEventListener('click', () => {
        const allSlotButtons = document.querySelectorAll('.slotButton');
        allSlotButtons.forEach((button) => {
          button.classList.remove('bg-purple-600');
          button.classList.add('bg-purple-200');
          button.classList.remove('text-white');
          button.classList.add('text-purple-700');
          button.classList.add('hover:bg-purple-100');

        });
        slotButton.classList.add('bg-purple-600');
        slotButton.classList.remove('bg-purple-200');
        slotButton.classList.add('text-white');
        slotButton.classList.remove('text-purple-700');
        slotButton.classList.remove('hover:bg-purple-100');

        selectedSlot = {
          start: slot.start,
          end: slot.end,
        };

        // undisable the submit button
        submitButton.disabled = false;
      });

      container.appendChild(slotButton);
    });

    timeSlotsParent.classList.remove('hidden');
  }

  submitButton.addEventListener('click', () => {
    if (!selectedSlot) {
      alert('Please select a time slot before submitting.');
      return;
    }

    // convert the selected slot to UTC time
    let utc_start_time = new Date(selectedSlot.start).toISOString();
    let utc_end_time = new Date(selectedSlot.end).toISOString();

    const payload = {
      start_time: utc_start_time,
      end_time: utc_end_time,
      order: orderId,
    };

    console.log(payload);

    fetch('/booking/create-appointment/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
      },
      body: JSON.stringify(payload),
    })
      .then((response) => {
        if (!response.ok) {
          return response.json().then((data) => {
            throw new Error(data.detail || 'Failed to create appointment.');
          });
        }
        return response.json();
      })
      .then(() => {
        location.reload(); // Refresh the page on success
      })
      .catch((err) => {
        console.error('Error creating appointment:', err);
        alert('Failed to create appointment. Please try again.');
      });
  });
}