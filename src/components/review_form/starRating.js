export function initReviewFormStarRating(containerId, hiddenInputId) {
  const container = document.getElementById(containerId);
  const hiddenInput = document.getElementById(hiddenInputId);

  if (!container || !hiddenInput) {
    return;
  }

  const starButtons = container.querySelectorAll(".leaveAReviewStarRatingButton");

  let selectedRating = 0; // Store the selected rating

  // Handle hover
  starButtons.forEach((button, index) => {
    button.addEventListener("mouseenter", () => {
      updateStars(index + 1);
    });

    button.addEventListener("mouseleave", () => {
      updateStars(selectedRating); // Reset to selected rating on mouse leave
    });

    // Handle click
    button.addEventListener("click", () => {
      selectedRating = index + 1;
      hiddenInput.value = selectedRating; // Update hidden input
    });
  });

  // Function to update star styles
  function updateStars(rating) {
    starButtons.forEach((button, index) => {
      const star = button.querySelector("svg");
      if (index < rating) {
        star.classList.remove("text-gray-300");
        star.classList.add("text-yellow-400");
        star.classList.add("fill-yellow-400");
      } else {
        star.classList.remove("fill-yellow-400");
        star.classList.remove("text-yellow-400");
        star.classList.add("text-gray-300");
      }
    });
  }
}
