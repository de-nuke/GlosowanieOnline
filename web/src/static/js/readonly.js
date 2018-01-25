window.onload = function() {
    var f1 = document.getElementById('id_series_number');
    var f2 = document.getElementById('pesel');

    if(f1 && f1.value.length) {
        f1.setAttribute('readonly', 'true');
    }

    if(f2 && f2.value.length) {
        f2.setAttribute('readonly', 'true');
    }
};