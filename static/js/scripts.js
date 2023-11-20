/*!
* Start Bootstrap - Agency v7.0.12 (https://startbootstrap.com/theme/agency)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-agency/blob/master/LICENSE)
*/

// Scripts

window.addEventListener('DOMContentLoaded', event => {
    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }
    };

    // Shrink the navbar when the page is scrolled
    navbarShrink();
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

    // Setup for the confirmation modal
    var confirmReservationModal = document.getElementById('confirmReservationModal');
    if (confirmReservationModal) {
        confirmReservationModal.addEventListener('show.bs.modal', function (event) {
            var button = event.relatedTarget;
            var cakeId = button.getAttribute('data-cake-id');
            var confirmButton = confirmReservationModal.querySelector('#confirmReservationButton');
            confirmButton.onclick = function () {
                window.location.href = `/reservations/create/${cakeId}/`; // Redireciona para a página de criação de reserva
            };
        });
    }
});

// Flatpickr setup for date and time selection
if (document.getElementById("id_datetime")) {
    flatpickr("#id_datetime", {
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        minDate: "today",
        time_24hr: true,
    });
}

// Event listener for date selection
var dateElement = document.getElementById('id_date');
if (dateElement) {
    dateElement.addEventListener('change', function() {
        var selectedDate = this.value;
        fetch(`/get-available-slots/?date=${selectedDate}`)
            .then(response => response.json())
            .then(data => {
                var timeSelect = document.getElementById('id_time');
                timeSelect.innerHTML = '';
                data.available_slots.forEach(function(slot) {
                    var option = document.createElement('option');
                    option.value = slot;
                    option.text = slot;
                    timeSelect.appendChild(option);
                });
            });
    });
}

// Function to handle reservation confirmation
function confirmReservation(cakeId) {
    fetch(`/reserve/${cakeId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ cake_id: cakeId })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert('Reservation successful!');
            location.reload();
        } else {
            alert('Reservation failed.');
        }
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
        alert('An error occurred. Please try again.');
    });
}

// Function to get a cookie value by name
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// Auto-hide alert messages after 2 seconds
window.addEventListener('DOMContentLoaded', (event) => {
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => alert.style.display = 'none');
    }, 2000);  // 2000 milliseconds = 2 seconds
});
