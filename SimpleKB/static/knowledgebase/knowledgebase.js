/////////////////////////////////////////////////////
/// Script for the Home page "knowledgebase.html" ///
/////////////////////////////////////////////////////

/// getting inital data and setting event listners
const user_folders = JSON.parse(document.getElementById('user_folders').textContent);
var change_folder_elements = document.getElementsByClassName("change-folder-class");

for (var i = 0; i < change_folder_elements.length; i++) {
  change_folder_elements[i].addEventListener('click', single_change_folder);
}

document.getElementById('change-folder-action').addEventListener('click', multiple_change_folder);
document.getElementById('delete-items-action').addEventListener('click', bulk_delete);

/// FUnction for deleting mulple items at once
function bulk_delete(event) {
  var items = document.querySelectorAll(".item-checkbox-class");
  var checked_items = [];
  items.forEach(element => {
    if (element.checked) {
      checked_items.push(element);
    }
  });

  if (checked_items.length === 0) {
    error_message('No items are selected');
    return;
  }

  var objects = [];
  checked_items.forEach(element => {
    var id = element.getAttribute('data-change-folder-id');
    var object_type = element.getAttribute('data-change-folder-type');

    objects.push({'id': id, 'object_type':object_type});
  });

  document.getElementById('id_bulk_delete-objects').value = JSON.stringify(objects);

  document.getElementById('BulkDeleteButton').click();
}


/// Function for changing the folder for a single item
function single_change_folder(event) {
    var change_folder_popup = new bootstrap.Modal(document.getElementById('ChangeFolderPopup'))
    var button = event.currentTarget;
    var id = button.getAttribute('data-change-folder-id');
    var object_type = button.getAttribute('data-change-folder-type');

    var object = [{'id': id, 'object_type':object_type}];
    document.getElementById('id_change_folder-objects').value = JSON.stringify(object);

    if (object[0].object_type === 'folder') {
      var folders = filter_user_folders(object);
    }
    else {
      var folders = user_folders;
    }

    var folder_options = document.getElementById('id_change_folder-folder');

    folder_options.innerHTML = '<option value="" selected="">(Root)</option>';

    folders.forEach(folder => {
      folder_options.innerHTML += `<option value="${folder.id}" >${folder.name}</option>`
    });

    change_folder_popup.show();
}


/// Function for changing the folder for a multiple item's
function multiple_change_folder(event) {
  var items = document.querySelectorAll(".item-checkbox-class");
  var checked_items = [];
  items.forEach(element => {
    if (element.checked) {
      checked_items.push(element);
    }
  });

  if (checked_items.length === 0) {
    error_message('No items are selected');
    return;
  }
  
  var change_folder_popup = new bootstrap.Modal(document.getElementById('ChangeFolderPopup'))

  var objects = [];
  checked_items.forEach(element => {
    var id = element.getAttribute('data-change-folder-id');
    var object_type = element.getAttribute('data-change-folder-type');

    objects.push({'id': id, 'object_type':object_type});
  });

  document.getElementById('id_change_folder-objects').value = JSON.stringify(objects);

  var folder_objects = objects.filter(x => x.object_type === 'folder');
  if (folder_objects.length !== 0) {
    var folders = filter_user_folders(folder_objects);
  }
  else {
    var folders = user_folders
  }

  var folder_options = document.getElementById('id_change_folder-folder');

  folder_options.innerHTML = '<option value="" selected="">(Root)</option>';

  folders.forEach(folder => {
    folder_options.innerHTML += `<option value="${folder.id}" >${folder.name}</option>`
  });

  change_folder_popup.show();

}


/// takes a list of folder objects and filters out any folders that would
///   cause folder structure inconsistency
function filter_user_folders(objects) {
  var folders = user_folders;
  user_folders.forEach(folder => {
      var object = objects.filter(x => x.id == folder.id);
      if (object.length !== 0) {
          sub_folders = get_sub_folders(object[0].id);
          folders = folders.filter(x => x.id != object[0].id);
          folders = folders.filter(x => sub_folders.filter(s => s.id == x.id) == 0);
      }
  });

  return folders;
}

/// Recursive function that takse a folder id and gets all of its sub folders
function get_sub_folders(folder_id) {
  var sub_folders = user_folders.filter(f => f.parent_folder == folder_id);
  var out_sub_folders = sub_folders;
  
  sub_folders.forEach(folder => {
    sub = get_sub_folders(folder.id);
    out_sub_folders.push(...sub);
  });
  

  return out_sub_folders;
}