
document.addEventListener('DOMContentLoaded', function() {

    const datetimes = document.querySelectorAll('.datetime-input');
    datetimes.forEach(function (datetime) {
        // getTimezoneOffset returns offset in minutes
        const UTCOffset = (new Date()).getTimezoneOffset();
        // When local datetime is converted to ISOString, the local datetime is
        // is also converted to UTC time
        // UTCOffset is subtracted from Date.now to offset the automatic conversion
        // to UTC time by toISOString() 
        // so that datetime.value will still show the datetime according to user's 
        // timezone while being ISO format to support the form datetime-local input
        var localDatetimeISO = new Date(Date.now() - UTCOffset * 60000).toISOString().slice(0, -8);
        datetime.value = localDatetimeISO;
    });
    
    const UTCOffsetData = document.querySelectorAll('.utc-offset');
    UTCOffsetData.forEach(function (offset) {
        // get the offset between UTC and user's local timezone
        // and set the input value of utc-offset which will be 
        // sent to backend
        const UTCOffset = (new Date()).getTimezoneOffset();
        offset.value = UTCOffset;
    });
});
