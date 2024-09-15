document.addEventListener('DOMContentLoaded', () => {
    const bookingForm = document.getElementById('booking-form');
    if (bookingForm) {
        bookingForm.addEventListener('submit', handleBookingSubmit);
    }
});

async function handleBookingSubmit(event) {
    event.preventDefault();
    const form = event.target;
    const clubId = document.getElementById('club-id').value;
    const name = form.name.value;
    const email = form.email.value;
    const date = form.date.value;

    try {
        const response = await fetch('/book', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ club_id: clubId, name, email, date }),
        });

        if (response.ok) {
            const result = await response.json();
            showBookingMessage(result.message);
            form.reset();
        } else {
            const error = await response.json();
            showBookingMessage(error.error, true);
        }
    } catch (error) {
        console.error('Error:', error);
        showBookingMessage('An error occurred. Please try again.', true);
    }
}

function showBookingMessage(message, isError = false) {
    const messageElement = document.getElementById('booking-message');
    messageElement.textContent = message;
    messageElement.classList.remove('hidden', 'text-green-600', 'text-red-600');
    messageElement.classList.add(isError ? 'text-red-600' : 'text-green-600');
}
