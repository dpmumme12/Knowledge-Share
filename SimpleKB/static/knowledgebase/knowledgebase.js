var change_folder_elements = document.getElementsByClassName("change-folder-class");

  for (var i = 0; i < change_folder_elements.length; i++) {
    change_folder_elements[i].addEventListener('click', single_change_folder);
  }

function single_change_folder(event) {
    var change_folder_popup = new bootstrap.Modal(document.getElementById('ChangeFolderPopup'))
    var button = event.currentTarget;
    var id = button.getAttribute('data-change-folder-id');
    var object_type = button.getAttribute('data-change-folder-type');

    object = [{'id': id, 'object_type':object_type}];
    document.getElementById('id_objects').value = JSON.stringify(object);

    change_folder_popup.show()
}