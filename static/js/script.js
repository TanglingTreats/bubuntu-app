var links = document.getElementsByClassName("nav-link");
var path = window.location.pathname;

console.log(path);

for(let i = 0; i < links.length; i++) {
    console.log("In for loop");
    console.log(links[i].getAttribute("href"));
    if(links[i].getAttribute("href") === path ) {
        console.log("In If")
        links[i].parentElement.classList.add("active");
    }
}
