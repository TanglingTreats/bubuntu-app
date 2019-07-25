var links = document.getElementsByClassName("nav-link");
var path = window.location.pathname;

console.log(path);

for(let i = 0; i < links.length; i++) {
    if(links[i].getAttribute("href") === path ) {
        links[i].parentElement.classList.add("active");
    }
}
