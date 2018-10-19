document.execCommand("defaultParagraphSeparator", false, "p");
tag_counter = document.getElementById("tag_counter");
tag_list = document.getElementById('tag_list');
file_list = document.getElementById('file_list');
drop_zone = document.getElementById('drop_zone');
drop_zone_overlay = document.getElementById('drop_zone_overlay');
update_input_width(tag_list.firstElementChild);
oPreviewImg = new Image();
text_editor = document.getElementById('text_editor');
file_array = [];


function addTag(event) {
    if (tag_list.children[tag_list.childElementCount - 2].value !== '') {
        let i = tag_list.children[0].cloneNode();
        i.value = '';
        i.style.width = '';
        i.name = "tag" + tag_counter.value;
        tag_list.insertBefore(i, tag_list.children[tag_list.childElementCount - 1]);
        i.focus();
        tag_counter.value = Number(tag_counter.value) + 1;
        update_input_width(i);
    }
}

function event_add_todo_entry(event) {
    add_todo_entry(event.target.parentNode.parentNode.parentNode, event.target);
}

function add_todo_entry(parent_tbody, button) {
    let tbody = parent_tbody;
    let tr = document.createElement("tr");
    tr.innerHTML =
        '<td>' +
        '<input class="w3-check" type="checkbox" disabled="disabled">' +
        '</td>' +
        '<td style="vertical-align: center">' +
        '<input class="w3-input todo_entry" type="text" maxlength=200 onkeypress="entry_keypress(event)">' +
        '</td>' +
        '<td>' +
        '<i class="material-icons w3-button" onclick="event_add_todo_entry(event)">add</i>' +
        '</td>';
    tbody.appendChild(tr);
    if (button) {
        button.innerText = "clear";
        button.onclick = event_remove_todo_entry;
    }
    tr.children[1].children[0].focus();
}

function event_remove_todo_entry(event) {
    event.target.parentNode.parentNode.parentNode.removeChild(event.target.parentNode.parentNode);
}

function event_remove_todo_list(event) {
    event.target.parentNode.parentNode.removeChild(event.target.parentNode);
}

function event_add_todo_list(event) {
    let l = document.getElementById("todo_list_list");
    let div = document.createElement("div");
    div.classList.add("todo_list");
    div.innerHTML =
        '<i class="material-icons w3-button" style="float: right; padding: 5px; font-size: medium" onclick="event_remove_todo_list(event)">clear</i>' +
        '<table class="w3-table" style="width: fit-content"><tbody></tbody></table>';
    l.appendChild(div);
    add_todo_entry(div.children[1].firstChild);
}

function show_and_play_animation(o) {
    o.style.display = "block";
    o.style.animation = "none";
    setTimeout(function () {o.style.animation = "";}, 10);
}

function show_not_enought_space_msg(total_size) {
    o = document.getElementById("error_no_space");
    show_and_play_animation(o);
    let msg = o.innerText;
    let ind = msg.indexOf(" Attachment:");
    if (ind !== -1){
        msg = msg.slice(0, ind);
    }

    msg += " Attachment: ";
    if (total_size >= 1024*1024*1024) {
        msg += (total_size/(1024*1024*1024)).toFixed(2) + " GB";
    }else if (total_size >= 1024*1024){
        msg += (total_size/(1024*1024)).toFixed(2) + " MB";
    }else if (total_size >= 1024){
        msg += (total_size/(1024)).toFixed(2) + " KB";
    }else{
        msg += total_size + " Bytes";
    }
    o.innerText = msg;
}

function submit(event) {
    document.getElementById('text_input').value = text_editor.innerHTML;

    let todo_list = document.getElementById('todo_list_list');
    document.getElementById('todo_list_count').value = todo_list.childElementCount;

    let note_form = document.getElementById('note_form');
    for (let todo_ind = 0; todo_ind < todo_list.childElementCount; todo_ind++) {
        let entrys = todo_list.children[todo_ind].getElementsByClassName('todo_entry');
        for (let entry_ind = 0; entry_ind < entrys.length; entry_ind++) {
            entrys[entry_ind].name = "todo_entry_" + todo_ind + "_" + entry_ind;
        }
        let cnt = document.createElement('input');
        cnt.type = 'hidden';
        cnt.value = entrys.length;
        cnt.name = 'todo_entry_count_' + todo_ind;
        note_form.appendChild(cnt)
    }

    let total_size = 0;
    for (ind=0; ind<file_array.length; ind++){
        let f = file_array[ind];
        total_size += f.size;
    }
    if (total_size > free_space){
        show_not_enought_space_msg(total_size);
        return;
    }

    let inputs = note_form.getElementsByTagName('input');
    let formData = new FormData();

    for (let ind=0; ind<inputs.length; ind++){
        let i = inputs[ind];
        formData.append(i.name, i.value);
    }
    for (ind=0; ind<file_array.length; ind++){
        let f = file_array[ind];
        formData.append('file' + ind, f, f.name);
    }

    let req = new XMLHttpRequest();
    let error = false;
    let progress_overlay = document.getElementById("progress_overlay");
    let progress_bar = document.getElementById("progress_bar");
    req.upload.onprogress = function (e){
        let pr = (e.loaded/e.total*100).toFixed(2) + "%";
        progress_bar.style.width = pr;
        progress_bar.innerText = pr;
    };
    req.onload = function (){
        let ans = JSON.parse(req.responseText);
        if (ans.status === "success"){
            window.location.href = "/"
        }else if (ans.status === "error"){
            error = true;
            progress_overlay.style.display = "none";
            switch (ans.error) {
                case "no title":
                    o = document.getElementById("error_no_title");
                    show_and_play_animation(o);
                    break;
                case "no space":
                    show_not_enought_space_msg(ans.required);
                    break;
            }
        }
    };
    req.open("POST", '/note/create/add');
    req.send(formData);
    setTimeout(function () {if (!error) progress_overlay.style.display = "flex"}, 200);
}

function handleDragOver(evt) {
    evt.stopPropagation();
    evt.preventDefault();
    evt.dataTransfer.dropEffect = 'copy'; // Explicitly show this is a copy.
}

function event_handleFiles(event) {
    event.stopPropagation();
    event.preventDefault();
    handleFiles(event.dataTransfer.files);
}

function handleFiles(files) {

    function handle_file(ind) {
        let file = files[ind];
        file_array.push(file);
        let container_div = document.createElement('div');
        container_div.classList.add('thumbnail_container');
        container_div.title = file.name;
        container_div.style.position = "relative";
        container_div.innerHTML =
            '<i ' +
            'class="material-icons w3-button"' +
            ' style="position: absolute; right: 0; top: 0; padding: 5px; font-size: 15px"' +
            ' onclick="remove_file(event)">clear</i>';
        if (/image*/.test(file.type)) {
            let file_reader = new FileReader();

            let img = document.createElement('img');
            img.classList.add('thumbnail');
            img.src = URL.createObjectURL(file);
            container_div.appendChild(img);
            file_list.insertBefore(container_div, file_list.children[file_list.childElementCount - 1]);
        }else{

            container_div.innerHTML += '<i class="material-icons thumbnail">insert_drive_file</i>' +
                '<label class="file_label">' + short_file_name(file.name, 25) + '</label>';
            file_list.insertBefore(container_div, file_list.children[file_list.childElementCount - 1]);

        }
    }
    for (let i=0; i<files.length; i++){
        handle_file(i);
    }
    document.getElementById("file_choose").value = '';
    drop_zone_overlay.dispatchEvent(new Event('dragleave'));
}

function remove_file(event){
    let ind = 0;
    let child = event.target;
    while( (child = child.previousSibling) != null ){
        ind++;
    }

    file_array.splice(ind, 1);
    event.target.parentElement.parentElement.removeChild(event.target.parentElement);

}

drop_zone_overlay.addEventListener('dragover', handleDragOver, false);

drop_zone_overlay.addEventListener('dragenter', function (e) {
    drop_zone.style.backgroundColor = "#ccc";
    e.stopPropagation();
}, false);

drop_zone_overlay.addEventListener('dragleave', function (e) {
    drop_zone.style.backgroundColor = "white";
    e.stopPropagation();
}, false);

drop_zone_overlay.addEventListener('drop', event_handleFiles, false);

drop_zone_overlay.addEventListener('click', function () {document.getElementById("file_choose").click();});
document.getElementById("file_choose").onchange = function (event) {handleFiles(event.target.files);};
