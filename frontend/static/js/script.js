const server_url = "http://localhost:8000"

function menu() {
    console.log(document.getElementById("mySidebar").style.display)
    if (document.getElementById("mySidebar").style.display != "block") {
        document.getElementById("mySidebar").style.display = "block";

    }
    else {
        document.getElementById("mySidebar").style.display = "none";
    }
}
