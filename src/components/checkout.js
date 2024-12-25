import autoComplete from "@tarekraafat/autocomplete.js";

export function initCheckout() {
  const timeInput = document.querySelector(".time-input");
  const placeOfBirthInput = document.querySelector("#place_of_birth");

  if (!timeInput || !placeOfBirthInput) {
    return;
  }

  timeInput.addEventListener("input", (event) => {
    let value = timeInput.value;

    value = value.replace(/\D/g, "");

    if (value.length > 2) {
      value = value.slice(0, 2) + ":" + value.slice(2);
    }

    value = value.slice(0, 5);

    const [hours, minutes] = value.split(":");

    if (hours && (parseInt(hours, 10) < 1 || parseInt(hours, 10) > 12)) {
      value = "12" + (minutes ? ":" + minutes : "");
    }

    if (minutes && parseInt(minutes, 10) > 59) {
      value = (hours ? hours : "12") + ":59";
    }

    timeInput.value = value;
  });

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
      keys: ["town", "state_name", "country_code", "postal_code"],
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
          document.querySelector("#place_of_birth").value = selection.town + ", " + selection.state_name + ", " + selection.country_code + ", " + selection.postal_code;
        }
      }
    }

  }


  const autocomplete = new autoComplete(autocompleteConfig);

}