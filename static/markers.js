let for_marker = () => {
    var marker = document.createElement("div");
    marker.innerHTML = `
  <button type="button" class="btn btn-info dropdown-toggle py-0 px-1 m-0" data-bs-toggle="dropdown" aria-expanded="false">
  </button>
  <ul class="dropdown-menu dropdown-menu-end text-success">
    <li><a class="dropdown-item" href="#">Learn about for loops</a></li>
    <li><a class="dropdown-item" href="#">Unravel for loop</a></li>
    <li><a class="dropdown-item" href="#">Toggle variable tracking</a></li>
    <li><a class="dropdown-item" href="#">Execute code up to this line</a></li>
  </ul>
`;
    marker.classList.add("btn-group");
    marker.classList.add("buttons-gutter");
    marker.classList.add("p-0");
    marker.classList.add("border-0");
    marker.classList.add("dropend");
    return marker;
}

let if_marker = () => {
    var marker = document.createElement("div");
    marker.innerHTML = `
  <button type="button" class="btn btn-info dropdown-toggle py-0 px-1 m-0" data-bs-toggle="dropdown" aria-expanded="false">
  </button>
  <ul class="dropdown-menu dropdown-menu-end text-success">
    <li><a class="dropdown-item" href="#">Learn about if</a></li>
    <li><a class="dropdown-item" href="#">Execute code up to this line</a></li>
  </ul>
`;
    marker.classList.add("btn-group");
    marker.classList.add("buttons-gutter");
    marker.classList.add("p-0");
    marker.classList.add("border-0");
    marker.classList.add("dropend");
    return marker;
}
let main_marker = () => {
    var marker = document.createElement("div");
    marker.innerHTML = `
  <button type="button" class="btn btn-info dropdown-toggle py-0 px-1 m-0" data-bs-toggle="dropdown" aria-expanded="false">
  </button>
  <ul class="dropdown-menu dropdown-menu-end text-success">
    <li><a class="dropdown-item" href="#">Learn about main</a></li>
    <li><a class="dropdown-item" href="#">Execute code up to this line</a></li>
  </ul>
`;
    marker.classList.add("btn-group");
    marker.classList.add("buttons-gutter");
    marker.classList.add("p-0");
    marker.classList.add("border-0");
    marker.classList.add("dropend");
    return marker;
}

let int_marker = () => {
    var marker = document.createElement("div");
    marker.innerHTML = `
  <button type="button" class="btn btn-info dropdown-toggle py-0 px-1 m-0" data-bs-toggle="dropdown" aria-expanded="false">
  </button>
  <ul class="dropdown-menu dropdown-menu-end text-success">
    <li><a class="dropdown-item" href="#">Learn about declarations</a></li>
    <li><a class="dropdown-item" href="#">Toggle variable tracking</a></li>
    <li><a class="dropdown-item" href="#">Execute code up to this line</a></li>
  </ul>
`;
    marker.classList.add("btn-group");
    marker.classList.add("buttons-gutter");
    marker.classList.add("p-0");
    marker.classList.add("border-0");
    marker.classList.add("dropend");
    return marker;
}

let other_marker = () => {
    var marker = document.createElement("div");
    marker.innerHTML = `
  <button type="button" class="btn btn-info dropdown-toggle py-0 px-1 m-0" data-bs-toggle="dropdown" aria-expanded="false">
  </button>
  <ul class="dropdown-menu dropdown-menu-end text-success">
    <li><a class="dropdown-item" href="#">Execute code up to this line</a></li>
  </ul>
`;
    marker.classList.add("other-marker");
    marker.classList.add("btn-group");
    marker.classList.add("buttons-gutter");
    marker.classList.add("p-0");
    marker.classList.add("border-0");
    marker.classList.add("dropend");
    return marker;
}

