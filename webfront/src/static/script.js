window.onload = function()
{
	var new_note = document.getElementById("new_note");
	new_note.addEventListener('click', clicked_new_note, false);

	var notes_list = document.getElementById("notes_list");
        notes_list.addEventListener('click', clicked_notes_list, false);
	
	var logout = document.getElementById("logout");
	logout.addEventListener('click', clicked_logout, false);
	
	$("#dynamic_panel").on('click',"#note_list #single_note #title",open_note);
	$("#dynamic_panel").on('click',"#note_list #single_note #delete", delete_note);
	$("#dynamic_panel").on('click',"#opened_note #delete", delete_note);
	$("#dynamic_panel").on('click',"#opened_note #edit", edit_note);
	$("#dynamic_panel").on('click',"#search_options #search", search);
}



function search()
{
        var type = "x"
	var data = "x"
        $.ajax({
                type: "DELETE",
                url: "http://edi.iem.pw.edu.pl/makosak/notesclient/" + type.toString() + '/' + data.toString(),
                dataType: "text",
                success: function(response) {
                        var section = document.getElementById("dynamic_panel");
                        section.innerHTML = response;
                }
        });
}

	
function delete_note()
{
	var id = $(this).attr("name");
        $.ajax({
          	type: "DELETE",
               	url: "http://edi.iem.pw.edu.pl/makosak/notesclient/delete/" + id.toString(),
               	dataType: "text",
               	success: function(response) {
                       	var section = document.getElementById("dynamic_panel");
                       	section.innerHTML = response;
               	}
        });
}

function edit_note()
{
        var id = $(this).attr("name");
        $.ajax({
                type: "PUT",
                url: "http://edi.iem.pw.edu.pl/makosak/notesclient/edit/" + id.toString(),
                dataType: "text",
                success: function(response) {
                        var section = document.getElementById("dynamic_panel");
                        section.innerHTML = response;
                }
        });
}

function open_note()
{
	var id = $(this).attr("name");
	$.ajax({
		type: "GET",
		url: "http://edi.iem.pw.edu.pl/makosak/notesclient/display/" + id.toString(),
		dataType: "text",
		success: function(response) {
			var section = document.getElementById("dynamic_panel");
			section.innerHTML = response;
		}
	});
}
function clicked_new_note()
{
	$.ajax({
           	type: "GET",
              	url: "http://edi.iem.pw.edu.pl/makosak/notesclient/new_note",
      		dataType: "text",
              	success: function (response) {
			var section = document.getElementById("dynamic_panel");
			section.innerHTML = response;
		}
	});
}
function clicked_notes_list()
{
        $.ajax({
                type: "GET",
                url: "http://edi.iem.pw.edu.pl/makosak/notesclient/get_all_notes",
                dataType: "text",
                success: function (response) {
                        var section = document.getElementById("dynamic_panel");
                        section.innerHTML = response;
                }
        });
}
function clicked_logout()
{
	top.location.href="http://edi.iem.pw.edu.pl/makosak/notesclient/logout"
}

