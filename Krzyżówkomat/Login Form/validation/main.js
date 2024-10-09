function validateForm() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    // Sprawdzamy, czy email nie jest pusty i jest w poprawnym formacie
    const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;
    if (!email || !emailPattern.test(email)) {
        alert("Please enter a valid email address.");
        return false;
    }

    // Sprawdzamy, czy hasło ma co najmniej 8 znaków
    if (password.length < 8) {
        alert("Password must be at least 8 characters long.");
        return false;
    }

    // Jeśli walidacja jest poprawna, można wysłać formularz
    return true;