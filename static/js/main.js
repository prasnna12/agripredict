/**
 * AgriPredict AI - Core Frontend Logic
 * Handles mobile nav, input presets, loading states, validation, and analytics charts.
 */

document.addEventListener('DOMContentLoaded', () => {
  initMobileNav();
  initPresetChips();
  initFormValidation();
  initHistoryClear();
});

// Mobile navigation toggle
function initMobileNav() {
  const toggleBtn = document.querySelector('.mobile-toggle');
  const navLinks = document.querySelector('.nav-links');

  if (toggleBtn && navLinks) {
    toggleBtn.addEventListener('click', () => {
      navLinks.classList.toggle('mobile-open');
      const isExpanded = navLinks.classList.contains('mobile-open');
      toggleBtn.setAttribute('aria-expanded', isExpanded);
    });
  }
}

// Preset chips handler for quick demonstration
function initPresetChips() {
  const chips = document.querySelectorAll('.preset-chip');
  if (!chips.length) return;

  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      const n = chip.getAttribute('data-n');
      const p = chip.getAttribute('data-p');
      const k = chip.getAttribute('data-k');
      const temp = chip.getAttribute('data-temp');
      const hum = chip.getAttribute('data-hum');
      const ph = chip.getAttribute('data-ph');
      const rain = chip.getAttribute('data-rain');

      setInputValue('nitrogen', n);
      setInputValue('phosphorus', p);
      setInputValue('potassium', k);
      setInputValue('temperature', temp);
      setInputValue('humidity', hum);
      setInputValue('ph', ph);
      setInputValue('rainfall', rain);

      // Flash visual highlight
      const form = document.getElementById('predictionForm');
      if (form) {
        form.style.transition = 'outline 0.3s ease';
        form.style.outline = '2px solid #16a34a';
        setTimeout(() => {
          form.style.outline = 'none';
        }, 600);
      }
    });
  });
}

function setInputValue(id, val) {
  const el = document.getElementById(id);
  if (el && val !== null) {
    el.value = val;
  }
}

// Form submission & loading state
function initFormValidation() {
  const form = document.getElementById('predictionForm');
  const loadingOverlay = document.getElementById('loadingOverlay');

  if (form) {
    form.addEventListener('submit', (e) => {
      // Validate inputs
      const inputs = [
        { id: 'nitrogen', name: 'Nitrogen (N)', min: 0, max: 200 },
        { id: 'phosphorus', name: 'Phosphorus (P)', min: 0, max: 200 },
        { id: 'potassium', name: 'Potassium (K)', min: 0, max: 300 },
        { id: 'temperature', name: 'Temperature', min: -10, max: 60 },
        { id: 'humidity', name: 'Humidity', min: 1, max: 100 },
        { id: 'ph', name: 'Soil pH', min: 0, max: 14 },
        { id: 'rainfall', name: 'Rainfall', min: 0, max: 600 }
      ];

      for (const item of inputs) {
        const el = document.getElementById(item.id);
        if (!el) continue;
        const val = parseFloat(el.value);

        if (isNaN(val)) {
          e.preventDefault();
          alert(`Please enter a valid numerical value for ${item.name}.`);
          el.focus();
          return;
        }

        if (val < item.min || val > item.max) {
          e.preventDefault();
          alert(`${item.name} must be between ${item.min} and ${item.max}.`);
          el.focus();
          return;
        }
      }

      // Show loading overlay
      if (loadingOverlay) {
        loadingOverlay.classList.add('active');
      }
    });
  }
}

// Clear history confirmation
function initHistoryClear() {
  const clearForm = document.getElementById('clearHistoryForm');
  if (clearForm) {
    clearForm.addEventListener('submit', (e) => {
      const confirmed = confirm('Are you sure you want to clear all prediction history? This action cannot be undone.');
      if (!confirmed) {
        e.preventDefault();
      }
    });
  }
}
