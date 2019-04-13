function panel(request, url, method, formId){
    var form = document.getElementById(formId)
    var formData = new FormData(form);
    request.open(method, url);
    request.send(formData);
    request.onreadystatechange = function(){
        if (request.readyState == 4 && request.status == 200){
            if (request.responseText){
                document.getElementById('html').innerHTML = request.responseText;
                addListener('adduser', function (){addUserPanel(request)});
                addListener('removeuser', function (){removeUserPanel(request)});
                addListener('modifyuser', function (){modifyUserPanel(request)});
                addListener('preference', function (){modifyPreferencePanel(request)});
            }
        }
    };
}

function addUserPanel(request){
    panel(request, 'web_user', 'POST', 'data')
}

function removeUserPanel(request){
    panel(request, 'web_user', 'DELETE', 'data')
}

function modifyUserPanel(request){
    panel(request, 'web_user', 'PUT', 'data')
}

function modifyPreferencePanel(request){
    panel(request, 'web_preference', 'PUT', 'data')
}

function addListener(id, listener) {
    var element = document.getElementById(id);
    if(element){
        element.onclick = listener;
    }
}

window.onload = function () {
    var request = new XMLHttpRequest();
    addListener('adduser', function (){addUserPanel(request)});
    addListener('removeuser', function (){removeUserPanel(request)});
    addListener('modifyuser', function (){modifyUserPanel(request)});
    addListener('preference', function (){modifyPreferencePanel(request)});
};
