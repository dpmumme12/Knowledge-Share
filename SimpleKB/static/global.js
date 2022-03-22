//takes cookie name input and gets a cookie from browser if it exists 
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function error_message(message) {
    document.getElementById('messages').innerHTML = `<div class=" alert-error alert d-flex align-items-center alert-dismissible fade show animate__animated animate__fadeInDown">
                                                        <svg class="bi flex-shrink-0 me-2" width="17" height="17" role="img">
                                                            <use xlink:href="#exclamation-triangle-fill"/>
                                                        </svg>
                                                        ${message}
                                                        <a class="alert-close-button" data-bs-dismiss="alert" aria-label="Close"><i class="fa-solid fa-xmark"></i></a>
                                                    </div>`;
}