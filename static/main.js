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

function event_update_input_width() {
    update_input_width(event.target);
}

function update_input_width(element) {
    let d = document.createElement('div');
    d.classList.add("tag");
    d.style.width = "fit-content";
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