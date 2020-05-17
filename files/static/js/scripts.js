$(document).ready(function () {
    $("#url-submit").on('click', function () {
        var data = {}
        $("#url-form").serializeArray().forEach(function (elem) {
            data[elem.name] = elem.value;
        })
        $.ajax({
            url: '/v1/videos/',
            type: "POST",
            dataType: 'json',
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': data['csrfmiddlewaretoken']
            },
            data: JSON.stringify(data),
            success: function (result) {
                console.log(result);
            },
            error: function (xhr, resp, text) {
                console.log(xhr, resp, text);
            }
        })
    });
});