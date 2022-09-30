function applyMarkerClasses(marker) {
    marker.classList.add("btn-group");
    marker.classList.add("buttons-gutter");
    marker.classList.add("p-0");
    marker.classList.add("border-0");
    marker.classList.add("dropend");
}

let for_marker = () => {
    const marker = document.createElement("div");
    marker.innerHTML = `
        <button type="button" class="btn btn-info dropdown-toggle py-0 px-1 m-0" data-bs-toggle="dropdown"
                aria-expanded="false"> </button>
        <div class="dropdown-menu dropdown-menu-end text-success">
            <a class="dropdown-item" href="#">Learn about for loops</a>
            <a class="dropdown-item" href="#">Unravel for loop</a>
            <a class="dropdown-item" href="#">Toggle variable tracking</a>
            <a class="dropdown-item" href="#">Execute code up to this line</a>
        </div>
    `;
    applyMarkerClasses(marker);
    return marker;
}

let if_marker = () => {
    const marker = document.createElement("div");
    marker.innerHTML = `
        <button type="button" class="btn btn-info dropdown-toggle py-0 px-1 m-0" data-bs-toggle="dropdown"
                aria-expanded="false"> </button>
        <div class="dropdown-menu dropdown-menu-end text-success">
            <a class="dropdown-item" href="#">Learn about if</a>
            <a class="dropdown-item" href="#">Execute code up to this line</a>
        </div>
    `;
    applyMarkerClasses(marker);
    return marker;
}
let main_marker = () => {
    var marker = document.createElement("div");
    marker.innerHTML = `
        <button type="button" class="btn btn-info dropdown-toggle py-0 px-1 m-0" data-bs-toggle="dropdown" 
                aria-expanded="false"> </button>
        <div class="dropdown-menu dropdown-menu-end text-success">
            <a class="dropdown-item" href="#">Learn about main</a>
            <a class="dropdown-item" href="#">Execute code up to this line</a>
        </div>
    `;
    applyMarkerClasses(marker);
    return marker;
}

let int_marker = () => {
    var marker = document.createElement("div");
    marker.innerHTML = `
        <button type="button" class="btn btn-info dropdown-toggle py-0 px-1 m-0" data-bs-toggle="dropdown" 
                aria-expanded="false"> </button>
        <div class="dropdown-menu dropdown-menu-end text-success">
            <a class="dropdown-item" href="#">Learn about declarations</a>
            <a class="dropdown-item" href="#">Toggle variable tracking</a>
            <a class="dropdown-item" href="#">Execute code up to this line</a>
        </div>
    `;
    applyMarkerClasses(marker);
    return marker;
}

let other_marker = () => {
    var marker = document.createElement("div");
    marker.innerHTML = `
        <button type="button" class="btn btn-info dropdown-toggle py-0 px-1 m-0" data-bs-toggle="dropdown" 
                aria-expanded="false"> </button>
        <div class="dropdown-menu dropdown-menu-end text-success">
            <a class="dropdown-item" href="#">Execute code up to this line</a>
            <div class="submenu position-relative">
                <div class="dropdown-item disabled text-dark">Submenu &raquo;</div>
                <div class = "dropdown-menu dropdown-submenu start-100 position-absolute" style="top: -7px;">
                    <a class="dropdown-item" href="#">Nested menu item</a>
                    <a class="dropdown-item" href="#">Nested menu item</a>
                </div>
            </div>
        </div>
    `;
    marker.classList.add("other-marker");
    applyMarkerClasses(marker);
    return marker;
}

let int_widget = (name, value, offset) => {
    let widget = document.createElement("span");
    widget.innerHTML = `${name} = ${value}`;
    widget.classList.add("badge");
    widget.classList.add("bg-primary");
    widget.classList.add("position-relative");
    widget.style = `left: ${offset}px; font-size: 1rem;`;
    return widget;
}