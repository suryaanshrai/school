document.querySelector("#searchbar").onkeyup = () => {
    let query = document.querySelector("#searchbar").value;
    if (query != "") {
        let searchbox = document.querySelector("#searchResults");
        searchbox.innerHTML = "";
        fetch(`search?q=${query}`)
        .then(request => request.json())
        .then(data => {
            if (data["res"].length != 0){
                data["res"].forEach(element => {
                    if (element["quantity"] != 0) {
                        // console.log(`${element["name"]} by ${element["author"]}: Available :D`)
                        let option=document.createElement("p");
                        option.innerHTML = `${element["id"]} - ${element["name"]} by ${element["author"]}: Available :D`;
                        searchbox.append(option);
                    }
                    else {
                        // console.log(`${element["name"]} by ${element["author"]}: Currentlu Unavailble :(`)
                        let option=document.createElement("p");
                        option.innerHTML = `${element["id"]} - ${element["name"]} by ${element["author"]}: Unavailable :(`;
                        searchbox.append(option);
                    }
                });
            }
            else {
                let searchbox = document.querySelector("#searchResults");
                searchbox.innerHTML = "No Results :(";
            }
            if (data["res_u"].length != 0) {
                document.querySelector("#searchResults").innerHTML = "";
                data["res_u"].forEach(element => {
                    let option=document.createElement("p");
                    option.innerHTML = `${element["username"]} issued ${element["book_name"]} due on ${element["due_date"]}`;
                    searchbox.append(option);
                })
            }
        });
    }
    else {
        document.querySelector("#searchResults").innerHTML = "";
    }
}


document.querySelectorAll(".noReturnForm").forEach(form => {
    form.onsubmit = () => {
        fetch(form.action, {
            method:'POST',
            body: new FormData(form),
        })
        .then(response => response.json())
        .then(data => {
            form.querySelectorAll('input').forEach(input=> {
                if (input.type != "hidden") {
                    input.value = "";
                }
            });
            let message = document.querySelector("#message");
            message.classList.add('slideinanim','alert','alert-primary')
            message.innerHTML = data["message"];
            setTimeout(()=> {
                message.classList.remove('slideinanim','alert','alert-primary');
                message.innerHTML = "";
            }, 5000)
        })
        return false;
    }
});

document.querySelectorAll('.dispButton').forEach(button=> {
    button.onclick = () => {
        document.querySelectorAll('.pages').forEach(page=>page.style.display="none");
        document.querySelector(`#${button.value}`).style.display = "block";  
        document.querySelector(`#${button.value}`).classList.add("slideinanim")
    }
})