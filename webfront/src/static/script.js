window.onload = function(){
    var first_name = document.getElementById("first_name");
    first_name.addEventListener("blur", first_name_check);
    first_name.addEventListener("keyup", first_name_check);

    var last_name = document.getElementById("last_name");
    last_name.addEventListener("blur", last_name_check);
    last_name.addEventListener("keyup", last_name_check);

    var passwd = document.getElementById("password");
    passwd.addEventListener("blur", password_check);
    passwd.addEventListener("keyup", password_check);

    var confirm_passwd = document.getElementById("confirm_password");
    confirm_passwd.addEventListener("blur", confirm_password_check);
    confirm_passwd.addEventListener("keyup", confirm_password_check);

    var birth_date = document.getElementById("birth_date");
    birth_date.addEventListener("blur", birth_date_check);
    birth_date.addEventListener("keyup", birth_date_check);

    var login = document.getElementById("login");
    //login.addEventListener("blur", login_check);
    //login.addEventListener("keyup", login_check);
    //
    //var male = document.getElementById("male");
    //male.addEventListener("blur", sex_check);
    //var female = document.getElementById("female");
    //female.addEventListener("blur", sex_check);
    //
    //var id = document.getElementById("id");
    //id.addEventListener("blur", id_check);
    //id.addEventListener("keyup", id_check);
    //
    //var file = document.getElementById("file");
    //file.addEventListener("blur", file_check);
    //
    //var send = document.getElementById("submit");
    //send.addEventListener("mouseover", check_all);
    //send.addEventListener("click", send);
    //
function clicked_logout()
{
	top.location.href="http://edi.iem.pw.edu.pl/makosak/notesclient/logout"
}

