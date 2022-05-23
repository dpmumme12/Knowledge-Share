const default_user_img = JSON.parse(get('#default_user_img').textContent);
get('#search-form').addEventListener('submit', search_form_submit);
var newsfeed_page = 1;

function search_form_submit(event) {
    event.preventDefault();
    form_data = new FormData(get('#search-form'))
    newsfeed_page = 1;
    load_newsfeed(form_data);
}

async function get_newsfeed(page, form_data=null) {
    const search_params = new URLSearchParams();

    if (form_data !== null) {
        form_data.forEach(function(value, key) {
            search_params.append(key, value);
        });
    }

    var response = await fetch(`/newsfeed/api/newsfeed?` + search_params);

    if(!response.ok) {
      error_message(`An error ocurred gathering notifications: ${response.status}`);
    }
    
    return await response.json();
}

async function load_newsfeed(form_data) {
    t = await get_newsfeed(1, form_data);
    console.log(t);
}

load_newsfeed()