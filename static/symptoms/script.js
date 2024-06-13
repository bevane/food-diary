
document.addEventListener('DOMContentLoaded', function() {

    const datetimeInputField = document.querySelector('.datetime-input');
    const availableSymptoms = JSON.parse(document.getElementById('registered-symptoms').textContent);

    if (!sessionStorage.getItem("lastDatetimeInput")) {
        // set datetime to now time if user launches a new session
        // so that the default datetime value they see is their local time
        (function setDatetimeToNow() {
            // getTimezoneOffset returns offset in minutes
            const UTCOffset = (new Date()).getTimezoneOffset();
            // When local datetime is converted to ISOString, the local datetime is
            // to UTC time by toISOString() 
            // so that datetime.value will still show the datetime according to user's 
            // timezone while being ISO format to support the form datetime-local input
            const localDatetimeISO = new Date(Date.now() - UTCOffset * 60000).toISOString().slice(0, -8);
            datetimeInputField.value = localDatetimeISO;
        })();
    } else {
        // set datetime to previously submitted datetime if user is in same session
        // because usually a user would want to enter multiple entries with same
        // or similar timestamp as their last entry
        datetimeInputField.value = sessionStorage.getItem("lastDatetimeInput")
    }

    addEventListener("submit", () => {
        submittedDatetime = document.querySelector('.datetime-input').value
        sessionStorage.setItem("lastDatetimeInput", submittedDatetime)
    });

    const UTCOffsetData = document.querySelectorAll('.utc-offset');
    UTCOffsetData.forEach(function(offset) {
        // get the offset between UTC and user's local timezone
        // // and set the input value of utc-offset which will be 
        // sent to backend
        const UTCOffset = (new Date()).getTimezoneOffset();
        offset.value = UTCOffset;
    });

    const UTCDatetimes = document.querySelectorAll('.utc-datetime');
    UTCDatetimes.forEach(function(datetime) {
        datetime.innerHTML = new Date(datetime.innerHTML).toLocaleString()
    });

    (function autocompleteSymptoms() {
        $("#symptom_name").autocomplete({
            source: function(request, response) {
                // limit max number of results in response to prevent slowdown
                const results = $.ui.autocomplete.filter(availableSymptoms, request.term);
                // will result in exact matches at the top of the response list
                // and lowercase above uppercase for same length of result
                // while still allowing middle of the word searches
                results.sort((a, b) => a.length - b.length || a.localeCompare(b));
                response(results.slice(0, 5));
            },
            minLength: 3,
        });
    })();
});