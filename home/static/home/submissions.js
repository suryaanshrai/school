// On form submission display a thank you message and close the window after five seconds
// check file size limit
// stylize the page such that only one form is visible at a time
document.querySelectorAll('.pageButton').forEach(button => {
    button.onclick = () => {
        document.querySelectorAll('.pages').forEach(page => {
            page.style.display="none";
        });
        let activepage=document.querySelector(`#page${button.value}`);
        activepage.style.display = "block";
        activepage.classList.add("slideinanim");
    };
});