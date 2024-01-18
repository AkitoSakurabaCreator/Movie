function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

document.querySelector('#mylist').addEventListener('click', function(e) {
    e.preventDefault();

    $.ajax({
        'url': 'mylist_add',
        'type': 'POST',
        'data': {
            'movie_id': this.id
        },
        'dataType': 'json'
    })
    .done(function(response){
        console.log(response.status);
        console.log(e)
        if (response.status == "True") {
            e.src = "/static/images/myList.svg"
            e.alt = "mylist add link"
        } else {
            e.src = "/static/images/check.svg"
            e.alt = "mylist already added"
        }
        if (response.status == 'login' ){
            window.location.href = 'accounts/login'
        }
    })
});