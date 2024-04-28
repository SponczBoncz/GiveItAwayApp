document.addEventListener("DOMContentLoaded", function() {
  let chosenCategories = [];
  let institutionChecked = null;
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      // TODO: get data from inputs and show them in summary
    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit(e) {
      // e.preventDefault();
      this.currentStep++;
      this.updateForm();
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }

  const categoryCheckboxes = document.querySelectorAll(".category-checkbox");

  const institutions = document.querySelectorAll("[data-institution-name]");

  // Add event listener to category checkboxes
  categoryCheckboxes.forEach(checkbox => {
    checkbox.addEventListener("change", () => {
      const selectedNames = Array.from(categoryCheckboxes)
        .filter(cb => cb.checked)
        .map(cb => cb.value); // Get selected names

      // Show/hide institutions based on selected names
      institutions.forEach(institution => {
        const institutionName = institution.getAttribute("data-institution-name");
        const institutionCategories = institution.getAttribute("data-categories").split(",");
        const isVisible = selectedNames.some(name => institutionCategories.includes(name));
        institution.style.display = isVisible ? "block" : "none";
      });
      chosenCategories = selectedNames;
    });
  });

  const formData = {
    bags: null,
  };


  // Event listener for the "Next" button in Step 2
  const step2NextButton = document.querySelector('[data-step="2"] .next-step');
  if (step2NextButton) {
    // Store the input value when clicking the "Next" button
    step2NextButton.addEventListener("click", function () {
      // Get the value from the "bags" input field
      const bagsInput = document.querySelector('[data-step="2"] input[name="bags"]').value;
      formData.bags = bagsInput;

      const step3NextButton = document.querySelector('[data-step="3"] .next-step');

      step3NextButton.addEventListener("click", function () {

        const checkedRadioButton = document.querySelector('[data-step="3"] input[name="organization"]:checked');

        if (checkedRadioButton) {
          // Find the parent label or surrounding div
          const parentLabel = checkedRadioButton.closest('label');

          // Check for the title containing the institution name
          if (parentLabel) {
            const institutionTitle = parentLabel.querySelector('.title').innerText.trim();
            institutionChecked = institutionTitle;
            console.log("Selected institution:", institutionTitle);
          }
          else {
            console.log("Parent label not found.");
          }
        }
        else {
          console.log("No radio button is checked.");
        }
        const step4NextButton = document.querySelector('[data-step="4"] .next-step');

        step4NextButton.addEventListener("click", function () {

          const streetInput = document.querySelector('[data-step="4"] input[name="address"]').value;
          const cityInput = document.querySelector('[data-step="4"] input[name="city"]').value;
          const postCodeInput = document.querySelector('[data-step="4"] input[name="postcode"]').value;
          const phoneNoInput = document.querySelector('[data-step="4"] input[name="phone"]').value;
          const dateInput = document.querySelector('[data-step="4"] input[name="data"]').value;
          const hourInput = document.querySelector('[data-step="4"] input[name="time"]').value;
          const commentsInput = document.querySelector('[data-step="4"] textarea[name="more_info"]').value;

          const step5Content = document.querySelector('[data-step="5"]');

          if (step5Content) {
            const bagsSummary = step5Content.querySelector('#bags');
            // const bagsInputHidden = step5Content.querySelector('#bags-input');
            const organizationSummary = step5Content.querySelector('#organization');
            // const organizationInputHidden = step5Content.querySelector('#organization-input');
            const streetInputSummary = step5Content.querySelector('#street');
            // const streetInputHidden = step5Content.querySelector('#street-input');
            const cityInputSummary = step5Content.querySelector('#city');
            // const cityInputHidden = step5Content.querySelector('#city-input');
            const postCodeInputSummary = step5Content.querySelector('#post_code');
            // const postCodeInputHidden = step5Content.querySelector('#postcode-input');
            const phoneNoInputSummary = step5Content.querySelector('#phone');
            // const phoneNoInputHidden = step5Content.querySelector('#phone-input');
            const dateInputSummary = step5Content.querySelector('#date');
            // const dateInputHidden = step5Content.querySelector('#date-input');
            const hourInputSummary = step5Content.querySelector('#hour');
            // const hourInputHidden = step5Content.querySelector('#time-input');
            const commentInputSummary = step5Content.querySelector('#comment');
            // const commentInputHidden = step5Content.querySelector('#comment-input');
            const categoriesInputHidden = step5Content.querySelector('#categories-input');
            // chosenCategories = chosenCategories.toLowerCase();
            if (bagsSummary) {
              if (formData.bags == 1) {
                bagsSummary.innerText = `${formData.bags} worek zawierający ${chosenCategories}`.toLowerCase();
              } else if (formData.bags < 5) {
                bagsSummary.innerText = `${formData.bags} worki zawierające ${chosenCategories}`.toLowerCase(); // Update summary with number of bags
              } else if (formData.bags < 21) {
                bagsSummary.innerText = `${formData.bags} worków zawierających ${chosenCategories}`.toLowerCase(); // Update summary with number of bags
              } else if (formData.bags < 100) {
                const x = formData.bags % 10;
                if (x > 1 && x < 5) {
                  bagsSummary.innerText = `${formData.bags} worki zawierające ${chosenCategories}`.toLowerCase();
                } else {
                  bagsSummary.innerText = `${formData.bags} worków zawierających ${chosenCategories}`.toLowerCase();
                }
              } else {
                const x = formData.bags % 100;
                const y = formData.bags % 10;

                if (x > 20 && y > 1 && y < 5) {
                  bagsSummary.innerText = `${formData.bags} worki zawierające ${chosenCategories}`.toLowerCase();
                } else {
                  bagsSummary.innerText = `${formData.bags} worków zawierających ${chosenCategories}`.toLowerCase();
                }
              }
              // bagsInputHidden.innerText = formData.bags
            }
            if (organizationSummary) {
              institutionChecked = institutionChecked.replace('Fundacja', 'fundacji').replace('Zbiórka lokalna', 'zbiórki lokalnej').replace('Organizacja pozarządowa', 'organizacji pozarządowej').replace(/[\r\n]+/g, ' ');
              organizationSummary.innerText = `Dla ${institutionChecked}`;
              // organizationInputHidden.innerText = checkedRadioButton.value;
            }
            if (streetInput) {
              streetInputSummary.innerText = streetInput;
              // streetInputHidden.innerText = streetInput;
            }
            if (cityInput) {
              cityInputSummary.innerText = cityInput;
              // cityInputHidden.innerText = cityInput;
            }
            if (postCodeInput) {
              postCodeInputSummary.innerText = postCodeInput;
              // postCodeInputHidden.innerText = postCodeInput;
            }
            if (phoneNoInput) {
              phoneNoInputSummary.innerText = phoneNoInput;
              // phoneNoInputHidden.innerText = phoneNoInput;
            }
            if (dateInput) {
              dateInputSummary.innerText = dateInput;
              // dateInputHidden.innerText = dateInput;
            }
            if (hourInput) {
              hourInputSummary.innerText = hourInput;
              // hourInputHidden.innerText = hourInput;
            }
            if (commentsInput) {
              commentInputSummary.innerText = commentsInput;
              // commentInputHidden.innerText = commentsInput;
            }
            categoriesInputHidden.innerText = chosenCategories;
            console.log(chosenCategories);
          }
        });
      });
    });
  }
});
