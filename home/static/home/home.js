let clickcount = 0;
let sidebarbutton=document.querySelector('#sidebar');
sidebarbutton.addEventListener('click', ()=> {
        let menubar=document.querySelector('#menubar');
        if(clickcount == 0) {
            menubar.style.left="0cm";
            clickcount = 1;
        }
        else {
            menubar.style.left="-6cm";
            clickcount=0;
        }  
});