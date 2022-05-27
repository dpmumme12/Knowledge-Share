const default_user_img = JSON.parse(get('#default_user_img').textContent);
const article_list = get("#article-list");
get('#search-form').addEventListener('submit', search_form_submit);
const loader = get(".loader");
const hideLoader = () => {
    loader.classList.remove('show-loader');
  };
  
  const showLoader = () => {
    loader.classList.add('show-loader');
  };
var newsfeed_page = 1;

async function search_form_submit(event) {
    event.preventDefault();
    var form_data = new FormData(get('#search-form'))
    newsfeed_page = 1;
    article_list.innerHTML = '';
    await load_newsfeed(form_data);
}

async function get_newsfeed(page, form_data=null) {
    const search_params = new URLSearchParams();

    if (form_data !== null) {
        form_data.forEach(function(value, key) {
            search_params.append(key, value);
        });
    }

    var response = await fetch(`/articlefeed/api/articlefeed?page=${page}&` + search_params);

    if(!response.ok) {
      error_message(`An error ocurred gathering notifications: ${response.status}`);
    }
    
    return await response.json();
}

function appendArticle(id, img, title, content, date, username, full_name) {
    var mt = 0;
    if (full_name === '') {mt = 3};
    const articleHTML = `
    <li class="list-group-item pt-3">
    <div class="col-md-12 me-auto">
            <div class="profile-card pb-2">
                <div class="d-inline-block float-start">
                <a href="/Dashboard/${username}" class="text-decoration-none text-dark">
                <img src="${img}" alt="Profile Picture" class="rounded-circle article-profile-img">
                </div>
                <div class="d-inline-block ps-2">
                    <h6 class="mb-0">${full_name}</h6>
                    <p class="mt-${mt} mb-0">@${username}</p>
                </div>
                 </a>
            </div>
            <a href="/knowledgebase/Article/${id}" class="text-decoration-none text-dark">
            <h3>${title}</h3>
            <p>${content}</p>
            </a>
            <div class="text-end"><small class="text-end">${formatDate(date)}</small></div>
    </div>
    </li>
    `;
  
    article_list.insertAdjacentHTML('beforeend', articleHTML);
  }

async function load_newsfeed(form_data) {
    get('#articleList-load-more-btn').innerHTML = '';
    showLoader();
    var articles = await get_newsfeed(newsfeed_page, form_data);

    if (articles.results.length === 0) {
      article_list.innerHTML = '<p>No articles found...</p>';
    }
    
    articles.results.forEach(article => {
        var img = article.profile_img;
        if (img === null) {img = default_user_img};

        appendArticle(article.id, img, article.title, article.truncated_content,
                      new Date(article.updated_on), article.username, article.full_name);
    });

    if(articles.next !== null) {
        newsfeed_page++;
        load_more = `<button class="btn btn-primary" 
                    onclick="load_newsfeed()">Load more</button>
                    `;

        get('#articleList-load-more-btn').innerHTML = load_more;
      }
    else {
        newsfeed_page = null;
        get('#articleList-load-more-btn').innerHTML = '';
      }
    hideLoader();
}

load_newsfeed()