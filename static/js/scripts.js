/*!
* Start Bootstrap - Shop Item v5.0.6 (https://startbootstrap.com/template/shop-item)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-item/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

flatpickr("#id_datetime", {
    enableTime: true,
    dateFormat: "Y-m-d H:i",
    minDate: "today",
    time_24hr: true,
});


document.getElementById('id_date').addEventListener('change', function() {
    var selectedDate = this.value;
    fetch(`/get-available-slots/?date=${selectedDate}`)
        .then(response => response.json())
        .then(data => {
            // Clear existing options
            var timeSelect = document.getElementById('id_time');
            timeSelect.innerHTML = '';

            // Populate time select with available slots
            data.available_slots.forEach(function(slot) {
                var option = document.createElement('option');
                option.value = slot;
                option.text = slot;
                timeSelect.appendChild(option);
            });
        });
});