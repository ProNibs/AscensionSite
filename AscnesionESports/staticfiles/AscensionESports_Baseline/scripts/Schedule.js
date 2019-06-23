var button1 = document.getElementById('b1');
var button2 = document.getElementById('b2');
var button3 = document.getElementById('b3');
var button4 = document.getElementById('b4');
var button5 = document.getElementById('b5');
var button6 = document.getElementById('b6');
var button7 = document.getElementById('b7');
var button8 = document.getElementById('b8');
var button9 = document.getElementById('b9');

// Have these similar to navbar attached to top and have the buttons bring you down to where you need to be
$(document).ready(function () {
    for (i = 1; i <= 10; i++) {
        var temp = $('<a/>', {
            text: 'Week' + i,
            id: 'btn_' + i,
            role: 'button',
            class: 'btn btn-dark'
        });
        $('.btn-group').append(temp);
    }
})

