
$('#login_form').one('submit', function() {
    if (validateForm()) {
        $('#login_btn').prop('disabled', true);
    } else {
        return false;
    }
});

$('#std_form').one('submit', function() {
    if (validateForm()) {
        $('#std_btn').prop('disabled', true);
    } else {
        return false;
    }
});

$('#admin_form').one('submit', function() {
    if (validateForm()) {
        $('#admin_btn').prop('disabled', true);
    } else {
        return false;
    }
});

function validateForm() {
    var password = document.getElementById('password').value;
    var imageInput = document.getElementById('image');
    var imageSize = imageInput.files[0] ? imageInput.files[0].size : 0; 

    var passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/;
    if (!passwordRegex.test(password)) {
        alert('Password must include at least one lowercase letter, one uppercase letter, one number, and one special character.');
        return false;
    }

    if (password.length < 8) {
        alert('Password must be at least 8 characters long.');
        return false;
    }

    var allowedSize = 1024 * 1024; 
    if (imageSize > allowedSize) {
        alert('Image size exceeds the allowed limit (1 MB).');
        return false;
    }

    return true;
}
