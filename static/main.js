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