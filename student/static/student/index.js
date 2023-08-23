document.querySelector("#class_button").onclick = () => {
    document.querySelector("#class_form").style.display = "block";
}

document.querySelector("#class_form").onsubmit = () => {
    let class_id = document.querySelector("#selected_class").value;
    window.location.replace(`/student/staff_page/${class_id}`);
    return false;
}