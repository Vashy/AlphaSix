function panelUser(request){
    var url='/user';
    request.open("PUT", url);
    request.send();
    request.onreadystatechange = function(){
        document.write(request.responseText);
    };
}

window.onload = function () {
    var request = new XMLHttpRequest();
    var adduser = document.getElementById('adduser');
    adduser.onclick = function () {
        panelUser(request);
    };
};
