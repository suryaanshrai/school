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