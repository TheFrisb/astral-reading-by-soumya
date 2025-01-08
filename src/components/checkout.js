import autoComplete from "@tarekraafat/autocomplete.js";

export function initCheckout() {
  const timeInput = document.querySelector(".time-input");
  const placeOfBirthInput = document.querySelector("#place_of_birth");

  if (!timeInput || !placeOfBirthInput) {
    return;
  }
  let lastValidValue = "";

  timeInput.addEventListener("input", () => {
    let raw = timeInput.value.replace(/\D/g, "");

    let formatted = raw;

    // Insert ':' if there are more than 2 digits
    if (raw.length > 2) {
      formatted = raw.slice(0, 2) + ":" + raw.slice(2, 4);
    }

    // If the new input is valid (full or partial), update lastValidValue
    if (isValidOrPartial(formatted)) {
      lastValidValue = formatted;
    } else {
      // Otherwise, revert to last known valid value
      formatted = lastValidValue;
    }

    timeInput.value = formatted;
  });

  /**
   * Checks if the string is a valid (or valid partial) 12-hour time of the form:
   *   - "HH:MM" with HH = 01–12, MM = 00–59
   *   - partial input that could still become valid:
   *       "", "0", "01", "09", "1", "12:", "12:3", etc.
   */
  function isValidOrPartial(value) {
    // Allow empty (nothing typed yet)
    if (!value) return true;

    // Split on potential ':'
    const parts = value.split(":");

    // 1) If we have just hours (no colon yet)
    if (parts.length === 1) {
      const hh = parts[0];
      // Let them type up to 2 digits for hours, as long as it could become valid
      // "0", "1", "01", "09", "12" are all potentially valid partial hours
      // We'll allow "0" or "00" temporarily if the user is trying to type "09".
      // But strictly, "00" won't ever become valid if the user stops there,
      // so you can decide if you want to allow that as a partial or revert immediately.
      // Below is a simple check that the numeric value is <= 12 so the user can type "09", "10", "12".
      if (/^\d{1,2}$/.test(hh)) {
        const num = parseInt(hh, 10);
        // If the user typed 0 or 00 alone, we’ll still allow it as partial
        // to let them finish typing "09", etc.
        // If they type 13, it’s invalid.
        return (num >= 0 && num <= 12);
      }
      return false;
    }

    // 2) If we have hours and minutes
    if (parts.length === 2) {
      const [hh, mm] = parts;

      // Hours must be 01–12 (leading zero allowed)
      // But we do allow partial “0”, “00” if the user typed only 1 or 2 digits so far.
      // So for the full valid time, we check:
      //   HH must be two digits 01–12
      //   MM must be two digits 00–59
      //
      // For partial, we allow something like "09:" or "09:3"
      // to let them finish typing minutes.

      // 2.1) hours check
      if (hh.length > 2) return false; // e.g. "123:"
      if (!/^\d{1,2}$/.test(hh)) return false;
      const hourNum = parseInt(hh, 10);
      // "00" is not a valid final hour, but could be partial if user is trying "09"
      // For a final valid time, 1 <= hourNum <= 12
      // For partial, we let "0"/"00" hang around until they type the second digit.
      if (hourNum < 0 || hourNum > 12) return false;

      // 2.2) minutes check
      // If minutes is empty (like "09:"), let it pass as partial
      if (mm === "") return true;
      // If minutes is one digit (like "09:3"), let it pass as partial
      if (/^\d{1}$/.test(mm)) {
        const minNum = parseInt(mm, 10);
        return (minNum >= 0 && minNum <= 5);
        // e.g., "09:5" is still partial, might become "09:59"
      }

      // If two digits, must be between 00 and 59
      if (/^\d{2}$/.test(mm)) {
        const minNum = parseInt(mm, 10);
        return (minNum >= 0 && minNum <= 59);
      }

      // Otherwise (more than 2 digits in minutes or non-numeric)
      return false;
    }

    // More than one colon or invalid structure
    return false;
  }

  const autocompleteConfig = {
    selector: "#place_of_birth",
    data: {
      src: async (query) => {
        try {
          const source = await fetch("/location-search/?town=" + query);
          const data = await source.json();
          return data;
        } catch (error) {
          return error;
        }
      },
      keys: ["town", "state_name", "country_code", "postal_code", "latitude", "longitude", "full_address"],
    },

    resultItem: {
      element: (element, suggestion) => {
        element.innerHTML = `
          <div class="autocomplete-suggestion">
            <span>${suggestion.value.town} ${suggestion.value.state_name}, ${suggestion.value.country_code}, ${suggestion.value.postal_code}</span>
          </div>  
        `;
      },

      highlight: true,
    },

    debounce: 300,

    placeholder: "Enter your place of birth",

    searchEngine: "loose",


    events: {
      input: {
        selection(event) {
          const selection = event.detail.selection.value;
          document.querySelector("#place_of_birth").value = selection.town + ", " + selection.state_name + ", " + selection.country_code + ", " + selection.postal_code + " | " + "Latitude: " + selection.latitude + ", Longitude: " + selection.longitude;
        }
      }
    }

  }


  const autocomplete = new autoComplete(autocompleteConfig);

}