function panel(request, url, method){
    request.open(method, url);
    request.send();
    request.onreadystatechange = function(){
        if (request.readyState == 4 && request.status == 200){
            if (request.responseText){
                document.write(request.responseText);
            }
        }
    };
}

function addUserPanel(request){
    panel(request, 'web_user', 'PUT')
}

function removeUserPanel(request){
    panel(request, 'web_user', 'DELETE')
}

window.onload = function () {
    var request = new XMLHttpRequest();
    var adduser = document.getElementById('adduser');
    adduser.onclick = function () {
        addUserPanel(request);
    };
};
