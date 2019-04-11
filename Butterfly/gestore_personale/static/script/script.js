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

function modifyUserPanel(request){
    panel(request, 'web_user', 'POST')
}

function modifyPreferencePanel(request){
    panel(request, 'web_preference', 'POST')
}

window.onload = function () {
    var request = new XMLHttpRequest();
    document.getElementById('adduser').onclick = function () {
        addUserPanel(request);
    };
    document.getElementById('removeuser').onclick = function () {
        removeUserPanel(request);
    };
    document.getElementById('modifyuser').onclick = function () {
        modifyUserPanel(request);
    };
    document.getElementById('preference').onclick = function () {
        modifyPreferencePanel(request);
    };
};
