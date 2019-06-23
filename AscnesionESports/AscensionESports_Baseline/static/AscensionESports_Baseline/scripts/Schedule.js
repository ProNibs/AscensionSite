// Variables
var number_of_weeks = uniqueArray(getUniquedates(match_times));
var next_match = compareDates(uniqueArray(match_times));


// Functions
function uniqueArray(arr) {
    var a = [];
    for (var i = 0, l=arr.length; i < l; i++) {
        if (a.indexOf(arr[i]) === -1) {
            a.push(arr[i]);
        }
    }
    return a;
}

function getUniquedates(arr) {
    var a = [];
    for (var i = 0, l = arr.length; i < l; i++) {
        a.push(arr[i].split(",", 1)[0]);
    }
    return a
}

// Going to add a Week X for each match history area
function changeMatchTimeToWeekNumber(arr) {
    // Need to iterate over each match history option
    $(".match_report").each(function () {
        // Get current class which has entire match_time
        var time_child = $(this).children(".time").text();
        for (i = 0; i <= arr.length; i++) {
            if (time_child.startsWith(arr[i])) {
                $(this).addClass("Week_" + (i+1));
            }
        }
    });
}

function getCurrentDate() {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();

    today = [mm, dd, yyyy];
    return today
}

// Gives the latest week number that is still in the future 
function compareDates(date_array) {
    var Months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    var current_date = getCurrentDate(); 
    var reformed_array = [];
    for (var i = 0; i < date_array.length; i++) {
        var x = date_array[i].split(",");
        var y = x[0].split(" ");
        reformed_array.push([Months.indexOf(y[0])+1, y[1], x[1]]);
    }
    var latest_date = number_of_weeks.length;
    for (var i = reformed_array.length-1; i > 0; i--) {
        if (current_date[2] < reformed_array[i][2]) {   // Check if scheduled year is in the future
            latest_date = (i / 2) + 1;
        } else if(current_date[2] <= reformed_array[i][2]) { //Check scheduled year is equal or greater than current
            if (current_date[0] < reformed_array[i][0]) {   // Check if scheduled month is in the future
                latest_date = (i / 2) + 1;
            } else if (current_date[0] <= reformed_array[i][0]) {  //Check scheduled month is equal or greater than current
                if (current_date[1] <= reformed_array[i][1]) {  //Check if schedule day is equal or greater than current
                    latest_date = (i / 2) + 1;
                }
            }
        }
    }
    return latest_date
}


// Ready the Document
$(document).ready(function () {
    changeMatchTimeToWeekNumber(number_of_weeks);
    for (i = 1; i <= number_of_weeks.length; i++) {
        var temp = $('<a/>', {
            text: 'Week ' + i,
            id: 'btn_' + i,
            role: 'button',
            class: 'btn btn-dark',
            click: function () {
                $(".btn").removeClass("focus");
                $(this).addClass("focus");
                $(".match_report").hide();
                $('.Week_'+ $(this).text().substr(-1)).show();
            }
        });
        $('.btn-group').append(temp);
    }
    // Logic for determining what is the default to be clicked
    $('#btn_' + compareDates(uniqueArray(match_times))).trigger('click');

})





