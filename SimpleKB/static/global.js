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
    document.getElementById('messages').innerHTML = `
    <div class="alert-error alert d-flex align-items-center alert-dismissible 
    fade show animate__animated animate__fadeInDown">
        <svg class="bi flex-shrink-0 me-2" width="17" height="17" role="img">
        <use xlink:href="#exclamation-triangle-fill"/>
        </svg>
        ${message}
        <a class="alert-close-button" data-bs-dismiss="alert" aria-label="Close">
        <i class="fa-solid fa-xmark"></i>
        </a>
    </div>
    `;
}

// Utils
function get(selector, root = document) {
    return root.querySelector(selector);
  }
  
  function formatDate(date) {
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'pm' : 'am';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0'+minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return (date.getMonth()+1) + "/" + date.getDate() + "/" + date.getFullYear() + "  " + strTime;
  }  
