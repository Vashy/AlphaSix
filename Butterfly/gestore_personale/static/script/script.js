function panel(request, url, method, formId, requestId, outputId){
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
                document.getElementById(outputId).innerHTML = request.responseText;
                addListener('adduser', function (){addUserPanel(request, 'adduser', 'html')});
                addListener('adduserpanel', function (){addUserPanel(request, 'adduserpanel', 'html')});
                addListener('removeuser', function (){removeUserPanel(request, 'removeuser', 'html')});
                addListener('removeuserpanel', function (){removeUserPanel(request, 'removeuserpanel', 'html')});
                addListener('showuser', function (){showUserPanel(request, 'showuser', 'html')});
                addListener('showuser', function (){showUserPanel(request, 'showuser', 'html')});
                addListener('modifyuser', function (){modifyUserPanel(request, 'modifyuser', 'html')});
                addListener('modifyuserpanel', function (){modifyUserPanel(request, 'modifyuserpanel', 'html')});
                addListener('preference', function (){modifyPreferencePanel(request, 'preference', 'html', 'data')});
                addListener('logout', function (){logout(request, 'logout', 'html')});
                addListener('back', function (){back(request, 'html')});
                addListener('modifytopics', function (){modifyPreferencePanel(request, 'modifytopics', 'topics', 'topics')});
                addListener('addproject', function (){modifyPreferencePanel(request, 'addproject', 'topics', 'projects')});
                addListener('removeproject', function (){modifyPreferencePanel(request, 'removeproject', 'topics', 'projects')});
                addListener('irreperibilita', function (){modifyPreferencePanel(request, 'irreperibilita', 'availability', 'availability')});
                addListener('previousmonth', function (){modifyPreferencePanel(request, 'previousmonth', 'availability', 'availability')});
                addListener('nextmonth', function (){modifyPreferencePanel(request, 'nextmonth', 'availability', 'availability')});
                addListener('piattaforma', function (){modifyPreferencePanel(request, 'piattaforma', 'platform', 'platform')});
            }
        }
    };
}

function addUserPanel(request, id, outputId){
    panel(request, 'web_user', 'POST', 'data', id, outputId)
}

function removeUserPanel(request, id, outputId){
    panel(request, 'web_user', 'DELETE', 'data', id, outputId)
}

function showUserPanel(request, id, outputId){
    panel(request, 'web_user', 'POST', 'data', id, outputId)
}

function modifyUserPanel(request, id, outputId){
    panel(request, 'web_user', 'PUT', 'data', id, outputId)
}

function logout(request, id, outputId){
    panel(request, 'web_user', 'POST', 'data', id, outputId)
}

function back(request, outputId){
    panel(request, 'web_user', 'GET', 'data', null, outputId)
}

function modifyPreferencePanel(request, requestId, outputId, formId){
    panel(request, 'web_preference', 'PUT', formId, requestId, outputId)
}

function addListener(id, listener) {
    var element = document.getElementById(id);
    if(element){
        element.onclick = listener;
    }
}

window.onload = function () {
    var request = new XMLHttpRequest();
    addListener('adduserpanel', function (){addUserPanel(request, null, 'html')});
    addListener('removeuserpanel', function (){removeUserPanel(request, null, 'html')});
    addListener('showuser', function (){showUserPanel(request, 'showuser', 'html')});
    addListener('modifyuserpanel', function (){modifyUserPanel(request, null, 'html', null)});
    addListener('preference', function (){modifyPreferencePanel(request, 'preference', 'html', 'data')});
    addListener('logout', function (){logout(request, 'logout', 'html', 'data')});
};
