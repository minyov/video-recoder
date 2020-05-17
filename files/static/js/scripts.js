$(document).ready(function () {
    $("#file-submit").on('click', function () {
        var fd = new FormData();
        var files = $('#file-input')[0].files[0];
        fd.append('file', files);

        $.ajax({
            url: '/v1/videos/',
            type: "POST",
            data: fd,
            contentType: false,
            processData: false,
            headers: {
                'X-CSRFToken': $("input[name='csrfmiddlewaretoken']").val()
            },
            success: function (result) {
                alert('Файл отправлен')
                window.location.reload()
            },
            error: function (xhr, resp, text) {
                alert('Ошибка отправки файла')
            },
            complete: function () {
                $("input[name='url']").val('')
            }
        })
    });
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
                alert('Ссылка в обработке')
                window.location.reload()
            },
            error: function (xhr, resp, text) {
                alert('Ошибка отправки ссылки')
            },
            complete: function () {
                $("input[name='url']").val('')
            }
        })
    });
});