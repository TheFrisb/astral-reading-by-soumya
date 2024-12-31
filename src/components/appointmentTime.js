export function initAppointmentTime() {
  const appointmentElement = document.getElementById('appointmentTime');
  const utcDateTime = appointmentElement?.getAttribute('data-utc');

  if (!utcDateTime) {
    console.error('No UTC date provided for the appointment.');
    return;
  }

  // Convert the UTC datetime string to a Date object
  const appointmentStartTime = new Date(utcDateTime);

  // Get the user's local timezone
  const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

  // Format options for date and time
  const dateOptions = {
    timeZone: userTimezone,
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  };

  const timeOptions = {
    timeZone: userTimezone,
    hour: 'numeric',
    minute: 'numeric',
    hour12: true,
  };

  // Generate local date and time strings
  const localDate = appointmentStartTime.toLocaleString('en-US', dateOptions);
  const localTime = appointmentStartTime.toLocaleString('en-US', timeOptions);

  // Render the date and time to their respective containers
  document.getElementById('userDate').textContent = localDate;
  document.getElementById('userTime').textContent = localTime;
}