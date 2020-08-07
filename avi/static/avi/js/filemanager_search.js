/*
Copyright (C) 2016-2018 Quasar Science Resources, S.L.

This file is part of DEAVI.

DEAVI is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DEAVI is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with DEAVI.  If not, see <http://www.gnu.org/licenses/>.
*/
var all_files = [];
var search_array = [];

function enter_search() {
    var input = document.getElementById("search");
    input.addEventListener("keyup", function(event) {
        event.preventDefault();
        if (event.keyCode === 13) {
            document.getElementById("search_icon").click();
        }
    });
}

function auto_names() {
    for (let i = 0; i < all_files.length; i++) {
        search_array.push(all_files[i].file + " - " + all_files[i].id);
    }
    $(".search_bar").autocomplete({ source: search_array });
};

function take_all_files(id, file, size) {
    var obj = { id: id, file: file, size: size };
    all_files.push(obj);
}

function test() {
    //console.log(all_files);
}

function searchF() {
    var variable = document.getElementById('search').value;
    //console.log(variable);
    variable = variable.replace(/\s/g, '');
    var variable_parts = variable.split('-');
    var data_size;
    document.getElementById('modal-title').innerHTML = "";
    //console.log(variable_parts);
    if (document.getElementById('search').value) {
        /*let date = document.getElementById(variable_parts[2] + "_" + variable_parts[1]).getAttribute('data').split('_')[0];
        let status = document.getElementById(variable_parts[2] + "_" + variable_parts[1]).getAttribute('data').split('_')[1];
        variable_parts[0] = variable_parts[0].charAt(0).toUpperCase() + variable_parts[0].slice(1);*/
        if (variable_parts[0].includes('gaia')) {
            document.getElementById('modal-title').innerHTML = "Gaia file";
        } else if (variable_parts[0].includes('hsa')) {
            document.getElementById('modal-title').innerHTML = "HSA file";
        } else if (variable_parts[0].includes('res')) {
            document.getElementById('modal-title').innerHTML = "Result file";
        } else if (variable_parts[0].includes('user')) {
            document.getElementById('modal-title').innerHTML = "User file";
        }
        //'<a class="btn-group a-link" target="_blank" href="/avi/api/res/'+ variable_parts[1] +'" 
        //style="display: block; width: 100%; overflow: hidden;white-space: nowrap;text-overflow: ellipsis;"
        //data-toggle="tooltip" data-pacement="top" title="'+ variable_parts[0] +'">'+variable_parts[0]+'</a>'
        //document.getElementById('_file-container').innerHTML = variable_parts[0];
        document.getElementById('_file-container').innerHTML = '<a class="btn-group a-link" target="_blank" href="/avi/api/res/' + variable_parts[1] +
            '" style="display: block; width: 100%; overflow: hidden;white-space: nowrap;text-overflow: ellipsis;" data-toggle="tooltip" data-pacement="top" title="' +
            variable_parts[0] + '">' + variable_parts[0] + '</a>';
        for (let i = 0; i < all_files.length; i++) {
            if (all_files[i].id === variable_parts[1]) {
                data_size = all_files[i].size;
                break;
            }
        }
        document.getElementById('_size-container').innerHTML = data_size;
        document.getElementsByClassName('download_modal')[0].setAttribute('action', '/avi/api/resource/' + variable_parts[1]);
        document.getElementsByClassName('download_modal')[1].setAttribute('title', 'Download ' + variable_parts[0]);
        document.getElementsByClassName('samp_modal_button')[0].setAttribute('id', 'samp_button_' + variable_parts[1]);
        document.getElementsByClassName('samp_modal_button')[0].setAttribute('onclick', 'samp_send(' + variable_parts[1] + ',\'' + variable_parts[0] + '\')');
        //document.getElementsByClassName('delete_file_modal')[0].setAttribute('data-target', '#call_delete_file_'+variable_parts[1]);
        document.getElementsByClassName('delete_file_modal')[0].setAttribute('name', variable_parts[1]);
        document.getElementsByClassName('delete_file_modal')[0].setAttribute('title', 'Delete ' + variable_parts[1]);
        document.getElementsByClassName('delete_file_modal')[0].setAttribute('value', 'pre_delete_file_' + variable_parts[1]);
        document.getElementsByClassName('delete_file_modal')[0].setAttribute('id', 'pre_delete_file_button_' + variable_parts[1]);

        document.getElementsByClassName('delete_file_modal')[1].setAttribute('id', 'call_delete_file_' + variable_parts[1]);
        document.getElementsByClassName('delete_file_modal')[2].setAttribute('id', 'modal_confirmation_file_pop_up_' + variable_parts[1]);
        document.getElementsByClassName('delete_file_modal')[3].innerHTML = "\"" + variable_parts[0] + "\"";
        document.getElementsByClassName('delete_file_modal')[4].setAttribute('value', variable_parts[0]);
    }
}
$(document).ready(function() {

    $(".delete_file_modal:first").on("click", function() {
        $('#myModal').modal('hide');
        $(".delete_file_modal:eq(1)").modal('show');
    });
    $('#modal_btn_no_file').on("click", function() {
        $(".delete_file_modal:eq(1)").modal('hide');
        $('#myModal').modal('show');
    });
});
$(document).ready(function() {
    document.querySelector("#selectFile").addEventListener('change', function(ev) {
        //console.log(ev.target.files[0].name);
        document.querySelector("[for='selectFile']").innerHTML = ev.target.files[0].name;
    });
});