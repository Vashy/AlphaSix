function panel(request, url, method, formId, requestId){
    var form = document.getElementById(formId)
    var formData = new FormData(form);
    if(requestId){
        formData.append(requestId, requestId)
    }
    request.open(method, url);
    request.send(formData);
    request.onreadystatechange = function(){
        if (request.readyState == 4 && request.status == 200){
            if (request.responseText){
                document.getElementById('html').innerHTML = request.responseText;
                addListener('adduser', function (){addUserPanel(request, 'adduser')});
                addListener('removeuser', function (){removeUserPanel(request, 'removeuser')});
                addListener('modifyuser', function (){modifyUserPanel(request, 'modifyuser')});
                addListener('preference', function (){modifyPreferencePanel(request, 'preference')});
            }
        }
    };
}

function addUserPanel(request, id){
    panel(request, 'web_user', 'POST', 'data', id)
}

function removeUserPanel(request, id){
    panel(request, 'web_user', 'DELETE', 'data', id)
}

function modifyUserPanel(request, id){
    panel(request, 'web_user', 'PUT', 'data', id)
}

function modifyPreferencePanel(request, id){
    panel(request, 'web_preference', 'PUT', 'data', id)
}

function addListener(id, listener) {
    var element = document.getElementById(id);
    if(element){
        element.onclick = listener;
    }
}

window.onload = function () {
    var request = new XMLHttpRequest();
    addListener('adduser', function (){addUserPanel(request, null)});
    addListener('removeuser', function (){removeUserPanel(request, null)});
    addListener('modifyuser', function (){modifyUserPanel(request, null)});
    addListener('preference', function (){modifyPreferencePanel(request, null)});
};
