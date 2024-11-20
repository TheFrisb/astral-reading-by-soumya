export function initAppointmentTime() {
  const appointmentElement = document.getElementById('appointmentTime');

  if (!appointmentElement) {
    return;
  }

  const utcDateTime = appointmentElement?.getAttribute('data-utc');

  if (!utcDateTime) {
    console.error('No UTC date provided for the appointment.');
    return;
  }

  const appointmentStartTime = new Date(utcDateTime);

  const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

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

  const localDate = appointmentStartTime.toLocaleString('en-US', dateOptions);
  const localTime = appointmentStartTime.toLocaleString('en-US', timeOptions);

  document.getElementById('userDate').textContent = localDate;
  document.getElementById('userTime').textContent = localTime;
}