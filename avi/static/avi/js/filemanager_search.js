/*
Copyright (C) 2016-2020 Quasar Science Resources, S.L.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
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