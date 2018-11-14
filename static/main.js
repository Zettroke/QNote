function mark_todo_entry(entry_id, checkbox) {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && !(this.status === 200)) {
            checkbox.checked = !checkbox.checked;
        }
    };
    xhttp.open("GET", "note/mark_todo_entry/" + entry_id, true);
    xhttp.send();

}

function event_update_input_width(event) {
    update_input_width(event.target);
}

function update_input_width(element) {
    let d = document.createElement('div');
    d.classList.add("tag");
    d.style.width = "fit-content";
    d.style.width += "-moz-fit-content";
    d.innerText = element.value;
    document.body.appendChild(d);
    let w = d.clientWidth;
    document.body.removeChild(d);
    if (w > 40) {
        element.style.width = (w+5) + "px";
    }else{
        element.style.width = 45 + 'px';
    }
}

function short_file_name(name, len){
    dot = name.lastIndexOf('.');

    if (name.length > len) {
        if (dot === -1) {
            return name.slice(0, len) + "...";
        } else {
            ext = name.slice(dot);
            if (ext.length > len) {
                return '... ' + ext;
            } else {
                return name.slice(0, len - ext.length) + '... <span style="word-break: normal">' + ext + '</span>';
            }
        }
    }else{
        if (dot === -1) {
            return name;
        } else {
            ext = name.slice(dot);
            return name.slice(0, name.length - ext.length) + '<span style="word-break: normal">' + ext + '</span>';

        }
    }
}

function format_file_size(total_size) {
    if (total_size >= 1024*1024*1024) {
        return (total_size/(1024*1024*1024)).toFixed(1) + " GB";
    }else if (total_size >= 1024*1024){
        return (total_size/(1024*1024)).toFixed(1) + " MB";
    }else if (total_size >= 1024){
        return (total_size/(1024)).toFixed(1) + " KB";
    }else{
        return total_size + " bytes";
    }
}