
function image_upload_handler (blobInfo, success, failure, progress) {
    const article_id = JSON.parse(document.getElementById('article_id').textContent);
    var xhr, formData;
  
    xhr = new XMLHttpRequest();
    xhr.withCredentials = false;
    xhr.open('POST', '/ImageUpload');
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken')); // manually set header
  
    xhr.upload.onprogress = function (e) {
      progress(e.loaded / e.total * 100);
    };
  
    xhr.onload = function() {
      var json;
  
      if (xhr.status === 403) {
        failure('HTTP Error: ' + xhr.status, { remove: true });
        return;
      }
  
      if (xhr.status < 200 || xhr.status >= 300) {
        failure('HTTP Error: ' + xhr.status);
        return;
      }
  
      json = JSON.parse(xhr.responseText);
  
      if (!json || typeof json.location != 'string') {
        failure('Invalid JSON: ' + xhr.responseText);
        return;
      }
  
      success(json.location);
    };
  
    xhr.onerror = function () {
      failure('Image upload failed due to a XHR Transport error. Code: ' + xhr.status);
    };
  
    formData = new FormData();
    formData.append('file', blobInfo.blob(), blobInfo.filename());
    formData.append('article_id', article_id)
  
    xhr.send(formData);
  };
