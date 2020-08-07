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
var text_array = ["hola", "Hola 2", "asdf", "qwerty"];
var gaia_array = [];
var hsa_array = [];
var res_array = [];
var user_array = [];
//var avi_url = "/";
var id_selected = 0;
/*
var get_files_list = function(type){
    $.ajax({
        type:"POST",
        url:"/avi/ajax/get_files_list",
        dataType:'json',
        data:{'type': type,
              csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
        success: function(data){
            console.log(data);            
        },
        error: function(xhr, textStatus, throwError){
            console.log(xhr);
        },
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    });
}
*/
/*$(document).ready(
    function do_poll()
    {
        //return;
        console.log("polling");
        $.ajax({
            type:"POST",
            url:avi_url+"avi/queries/status",
            data:{'poll':'yes',
                  csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
            success: function(data){
                console.log(data.slice(data.indexOf('card-body'), data.indexOf('end_scripts')));
                var state = data.slice(data.indexOf('card-body'), data.indexOf('end_scripts'));
                if(state.includes('PENDING') || state.includes('STARTED')){
                    setTimeout(do_poll, 5000);
                }else{
                    document.getElementById('gaia_load_icon').remove();
                }
                console.log("refresh");
                //window.location.reload();
            }
        });
    });*/

$(document).ready(
    function do_poll() {
        //return;
        setTimeout(function() {
        console.log();
        var query = document.getElementById('query_loading').getAttribute('state');
        query = query.replace(/ /g, '');
        query = query.replace(/'/g, '"');
        var obj = JSON.parse(query);
        // console.log(obj.algorithm_flag[0]);
        var state = document.getElementById(document.querySelector('[id^="div_alg_info'+obj.algorithm_flag[0]+'"]').id).getAttribute('state');
        state = state.replace(/ /g, '');
        state = state.replace(/'/g, '"');
        // console.log(state);
        obj = JSON.parse(state);
        // console.log(obj);
        // console.log("polling");
        $.ajax({
            type: "POST",
            url: avi_url + "avi/ajax/get_query_status",
            dataType: 'json',
            data: {
                'id': obj['pk'],
                'mission': obj['table'],
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
            },
            success: function(data) {
                // console.log(data)


                if (data == 'PENDING' || data == 'STARTED') {
                    let alert = '<div id="alert-info" class="alert alert-info" role="alert">Loading query please wait</div>';
                    document.getElementById('alert').innerHTML = alert;
                    setTimeout(do_poll, 5000);
                } else {
                    let length = document.getElementsByClassName('load_icon').length;
                    for (let i = 0; i < length; i++) {
                        let tick_icon = '<div class="tick_icon mt-2 ml-1"><i class="fas fa-check fa-w-16 fa-lg"></i></div>';
                        document.getElementsByClassName('load_icon')[0].remove();
                        document.getElementsByClassName('icon')[i].innerHTML = tick_icon;
                    }
                    state = document.getElementById(document.querySelector('[id^="div_alg_info'+obj.algorithm_flag[0]+'"]').id).getAttribute('state');
                    state = state.replace('True', 'False');
                    document.getElementById(document.querySelector('[id^="div_alg_info'+obj.algorithm_flag[0]+'"]').id).setAttribute('state', state);
                    let alert = '<div id="alert-info" class="alert alert-info" role="alert">Query ready</div>';
                    document.getElementById('alert').innerHTML = alert;

                    $.ajax({
                        type: "POST",
                        url: avi_url + "avi/ajax/get_alg_info",
                        dataType: 'json',
                        data: {
                            'id': id_selected,
                            //'name': name,
                            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
                        },
                        success: function(data) {
                            console.log("algorithm info not function");
                            if ('hsa' in data) {
                                hsa_array = data['hsa'];
                                $(".hsa_table").autocomplete({ source: hsa_array });
                            }
                            if ('gaia' in data) {
                                gaia_array = data['gaia'];
                                $(".gaia_table").autocomplete({ source: gaia_array });
                            }
                            if ('res' in data) {
                                res_array = data['res'];
                                $(".results_data").autocomplete({ source: res_array });
                            }
                            if ('user' in data) {
                                user_array = data['user'];
                                $(".user_data").autocomplete({ source: user_array });
                            }
                        },
                        error: function(xhr, textStatus, throwError){
                            console.log("error 2");
                        }
                    });
                    setTimeout(function() {
                        document.getElementById('alert-info').remove();


                    }, 5000);
                    //window.location = window.location.href;
                }
                console.log("refresh");
                //window.location.reload();
            }
        });

    }, 2000);
    });

var create_form = function(el, id, data, state, description) {
    var desc_id = "#div_description"+id;
    desc = $(desc_id);
    desc.html('');
    if (!description["description"]) {
        description["description"] = "No description";
    }
    desc.append("<p>" + description["description"] + "</p>");
    $(desc_id).show();

    var desc_div = "#alg_description"+id;
    $(desc_div).css("display", "block");

    var x = document.getElementById("div_description"+id).querySelectorAll("p");
    for(let i = 0; i < x.length; i++){
        x[i].className = "text";
    }
    // console.log(id_selected);

    var view_name = data['view_name'];
    var form = $('<form></form>', {
        method: 'post',
        id: 'alg_info_form'
    }); //,autocomplete: 'off'});
    var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    document.getElementById("div_alg_info"+id).className = "text-center col-sm-12";
    document.getElementById("div_alg_info"+id).setAttribute("style", "width:100%");
    form.append('<input name="csrfmiddlewaretoken" value="' +
        token + '" type="hidden">');
    // form.append('<h3>' + view_name + '</h3>');
    // console.log(description);
    // console.log(el[0].id);
    $.each(data, function(k, v) {
        var div_row = $('<div class="row"></div>');
        var div = $('<div class="col-sm-12"></div>');
        var inp_id = id + "_" + v['name'];
        //console.log(inp_id);
        if (v['type'] == "bool") {
            if ("info" in v) {
                adiv.append('<label class="text-left" for="' + id + "_" + v['name'] + ' title="' + v["info"] + '">' + v['view_name'] + "</label>");
            } else {
                div.append('<label class="text-left" for="' + id + "_" + v['name'] + '>' + v['view_name'] + '</label>');
            }
            div.append('<input id="' + id + "_" + v['name'] + '" name="' + id + "_" + v['name'] +
                '" type="checkbox" value="true">');
            form.append(div);
        } else if (v['type'] == "string" ||
            v['type'] == "float" ||
            v['type'] == "integer" ||
            v['type'] == "long" ||
            v['type'] == "complex") {
            var adiv = $('<div class="row" style="width:100%; margin-top:5px"></div>');
            if ("info" in v) {
                adiv.append('<label for="' + id + "_" + v['name'] + '" class = "col-sm-5 col-form-label text-left" title="' + v["info"] + '">' + v['view_name'] + "</label>");
            } else {
                adiv.append('<label for="' + id + "_" + v['name'] + '" class = "col-sm-5 col-form-label text-left">' + v['view_name'] + "</label>");
            }
            var ainput = $('<input id="' + id + "_" + v['name'] + '" name="' + id + "_" + v['name'] +
                '" type="text" value="" class="col-sm-7 form-control">');
            adiv.append(ainput);
            div.append(adiv);
            div_row.append(div);
            /*div.append('<label class = "col-sm-4 col-form-label">' + v['view_name'] + "</label>");
            div.append('<input name="' + id + "_" + v['name'] +
                '" type="text" value="" class="col-sm-7 form-control">');*/
            form.append(div_row);
        } else if (v['type'] == "gaia_table") {
            // console.log("gaia");
            var adiv = $('<div class="autocomplete row" style="width:100%; margin-top:5px"></div>');
            if ("info" in v) {
                adiv.append('<label for="' + inp_id +'" class = "col-sm-5 col-form-label text-left" title="' + v["info"] + '">' + v['view_name'] + "</label>");
            } else {
                adiv.append('<label for="' + inp_id +'" class = "col-sm-5 col-form-label text-left">' + v['view_name'] + "</label>");
            }
            var ainput = $('<input name="' + id + "_" + v['name'] +
                '" id="' + inp_id +
                '" class="gaia_table col-sm-7 form-control"' +
                ' type="text" placeholder="Gaia Table">');
            //ainput.autocomplete();
            //ainput.autocomplete({source:text_array});
            if (state.includes('gaia')) {
                if (state.includes('True')) {
                    var icon = '<div class="icon"><div class="load_icon mt-2 ml-1"><i class="fa fa-spinner fa-w-16 fa-spin fa-lg"></i></div></div>';
                }
            }
            var gbutton = '<button type="button" class="btn btn-info text-left" data-toggle="modal" data-target="#myModal">Launch Gaia query</button>';
            //var gbutton = '<form id="asdfff" method="post"><input type="hidden" name="csrfmiddlewaretoken" value="DVzic7x1JNw5RZN6aEP1SKP5Z9ym8X6Z"><button type="submit" formmethod="POST" title="gaia_query" value="1" name="gaia_query" class="btn btn-info" data-toggle="modal" data-target="#myModal">Launch gaia query</button></form>';
            /*
            <button type="button" class="btn btn-info">Info</button>
            */
            adiv.append(ainput);
            adiv.append(gbutton);
            adiv.append(icon);
            div.append(adiv);
            div_row.append(div);
            form.append(div_row);
            //get_files_list("gaia");
            //autocomplete(ainput[0], text_array);
        } else if (v['type'] == "hsa_table") {
            var adiv = $('<div class="autocomplete row" style="width:100%; margin-top:5px"></div>');
            if ("info" in v) {
                adiv.append('<label for="' + inp_id +'" class = "col-sm-5 col-form-label text-left" title="' + v["info"] + '">' + v['view_name'] + "</label>");
            } else {
                adiv.append('<label for="' + inp_id +'" class = "col-sm-5 col-form-label text-left">' + v['view_name'] + "</label>");
            }
            adiv.append('<input name="' + id + "_" + v['name'] +
                '" id="' + inp_id +
                '" class="hsa_table col-sm-7 form-control"' +
                ' type="text" placeholder="HSA Table">');
            if (state.includes('hsa')) {
                if (state.includes('True')) {
                    var icon = '<div class="icon"><div class="load_icon mt-2 ml-1"><i class="fa fa-spinner fa-w-16 fa-spin fa-lg"></i></div></div>';
                }
            }
            var gbutton = '<button type="button" class="btn btn-info text-left" data-toggle="modal" data-target="#myModal2">Launch HSA query</button>';

            adiv.append(gbutton);
            adiv.append(icon);
            div.append(adiv);
            div_row.append(div);
            form.append(div_row);
            //get_files_list("hsa");
            //document.getElementById(inp_id)
            //autocomplete(adiv[0], text_array);
        } else if (v['type'] == "results_data") {
            var adiv = $('<div class="autocomplete row" style="width:100%; margin-top:5px"></div>');
            if ("info" in v) {
                adiv.append('<label for="' + inp_id +'" class = "col-sm-5 col-form-label text-left" title="' + v["info"] + '">' + v['view_name'] + "</label>");
            } else {
                adiv.append('<label for="' + inp_id +'" class = "col-sm-5 col-form-label text-left">' + v['view_name'] + "</label>");
            }
            adiv.append('<input name="' + id + "_" + v['name'] +
                '" id="' + inp_id +
                '" class="results_data col-sm-7 form-control"' +
                ' type="text" placeholder="Results Data">');
            div.append(adiv);
            div_row.append(div);
            form.append(div_row);
            //get_files_list("hsa");
            //document.getElementById(inp_id)
            //autocomplete(adiv[0], text_array);
        } else if (v['type'] == "user_data") {
            var adiv = $('<div class="autocomplete row" style="width:100%; margin-top:5px"></div>');
            if ("info" in v) {
                adiv.append('<label for="' + inp_id +'" class = "col-sm-5 col-form-label text-left" title="' + v["info"] + '">' + v['view_name'] + "</label>");
            } else {
                adiv.append('<label for="' + inp_id +'" class = "col-sm-5 col-form-label text-left">' + v['view_name'] + "</label>");
            }
            adiv.append('<input name="' + id + "_" + v['name'] +
                '" id="' + inp_id +
                '" class="user_data col-sm-7 form-control"' +
                ' type="text" placeholder="User Data">');
            div.append(adiv);
            div_row.append(div);
            form.append(div_row);
            //get_files_list("hsa");
            //document.getElementById(inp_id)
            //autocomplete(adiv[0], text_array);
        }
    });
    //form.append('
    form.append('<button name="algorithm_id" class="btn btn-outline-primary" style="margin-top:5px; margin-bottom: 5px" type="submit" value="' +
        id + '">Run</button>');
    el.append(form);
    autocomplete_input(id);
    $("#alg_parameters").show();
    if (state.includes('True') && document.getElementById('query_loading').getAttribute('flag') == 'true'){
        var alg_group = document.getElementById(id).getAttribute('alg_group');
        for(let x = 0; x < document.getElementsByClassName("text-capitalize nav-item nav-link active").length; x++){
            document.getElementsByClassName("text-capitalize nav-item nav-link active")[x].setAttribute("aria-selected","false");
            document.getElementsByClassName("text-capitalize nav-item nav-link active")[x].className = "text-capitalize nav-item nav-link";
        }
        document.getElementById('nav-'+alg_group+'-tab').className = "text-capitalize nav-item nav-link active";
        document.getElementById('nav-'+alg_group+'-tab').setAttribute("aria-selected","true");
        document.getElementsByClassName("tab-pane fade show active")[0].className = "tab-pane fade";
        document.getElementById('nav-'+alg_group).className = "tab-pane fade show active";
        document.getElementById(id).setAttribute("aria-expanded","true");
        document.getElementById(id).className = "btn btn-link alg-button";
        document.getElementById("collapse-"+id).className = "collapse show";
        document.getElementById('query_loading').setAttribute("flag","false");
    }
    

}

var get_algorithm_info = function(el, id, state) { //, name){

    // console.log(state)
    $.ajax({
        type: "POST",
        url: avi_url + "avi/ajax/get_alg_info",
        dataType: 'json',
        data: {
            'id': id,
            //'name': name,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success: function(data) {
            console.log(data);
            if ('hsa' in data) {
                hsa_array = data['hsa'];
            }
            if ('gaia' in data) {
                gaia_array = data['gaia'];
            }
            if ('res' in data) {
                res_array = data['res'];
            }
            if ('user' in data) {
                user_array = data['user'];
            }
            // create_form($("#" +el[0].id+id), id, data['algorithm_input'], state, data['algorithm']);
            create_form(el, id, data['algorithm_input'], state, data['algorithm']);
        },
        error: function(xhr, textStatus, throwError) {
            console.log(xhr);
        },
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    });
}

$(document).ready(function() {
    $(".alg-button").click(function() {
        if($(this).hasClass('collapsed')){
            var id = $(this).attr("id");
            id_selected = id;
            document.getElementById("algorithm_pk_gaia_form").setAttribute('value', id_selected);
            document.getElementById("algorithm_pk_hsa_form").setAttribute('value', id_selected);
            //var name = $(this).attr("name");
            var info_id = "div_alg_info"+id; //_" + id;
            var state = document.getElementById('div_alg_info'+id).getAttribute('state');
            var node = document.getElementById(info_id);
            while (node.firstChild) {
                node.removeChild(node.firstChild);
            }
            get_algorithm_info($("#" + info_id), id, state); //, name);
        }
    });
});


$(document).ready(function() {
    var query = document.getElementById('query_loading').getAttribute('state');
    query = query.replace(/ /g, '');
    query = query.replace(/'/g, '"');
    var obj = JSON.parse(query);
    var state = document.getElementById(document.querySelector('[id^="div_alg_info'+obj.algorithm_flag[0]+'"]').id).getAttribute('state');
    state = state.replace(/ /g, '');
    state = state.replace(/'/g, '"');
    // console.log(state);
    var obj = JSON.parse(state);
    // console.log(obj);
    if (state.includes('algorithm_flag')) {
        var id = obj.algorithm_flag;
        // console.log(id[0]);
        id_selected = id[0];
        document.getElementById("algorithm_pk_gaia_form").setAttribute('value', id_selected);
        document.getElementById("algorithm_pk_hsa_form").setAttribute('value', id_selected);
        //var name = $(this).attr("name");
        var info_id = "div_alg_info"+obj.algorithm_flag[0]; //_" + id;
        var node = document.getElementById(info_id);
        while (node.firstChild) {
            node.removeChild(node.firstChild);
        }
        state = document.getElementById('div_alg_info'+obj.algorithm_flag[0]+'').getAttribute('state');
        get_algorithm_info($("#" + info_id), obj.algorithm_flag[0], state); //, name);
    }
});

$(document).ready(function() {
    var desc_id = "#div_description";
    $(desc_id).hide();
    var info_id = "#div_alg_info";
    var node = $(info_id);
    node.on("DOMSubtreeModified",
        function() {
            //console.log("onChange");
            //$("#alg_info_form").attr("autocomplete","off");
            $(".gaia_table").autocomplete({ source: gaia_array });
            $(".hsa_table").autocomplete({ source: hsa_array });
            $(".results_data").autocomplete({ source: res_array });
            $(".user_data").autocomplete({ source: user_array });
        }
    );
});

function autocomplete_input(id){
    // var desc_id = "#div_description"+id;
    // $(desc_id).hide();
    var info_id = "#div_alg_info"+id;
    var node = $(info_id);
    $(".gaia_table").autocomplete({ source: gaia_array });
    $(".hsa_table").autocomplete({ source: hsa_array });
    $(".results_data").autocomplete({ source: res_array });
    $(".user_data").autocomplete({ source: user_array });
    node.on("DOMSubtreeModified",
    function() {
        //console.log("onChange");
        //$("#alg_info_form").attr("autocomplete","off");
        // $(".gaia_table").autocomplete({ source: gaia_array });
        // $(".hsa_table").autocomplete({ source: hsa_array });
        // $(".results_data").autocomplete({ source: res_array });
        // $(".user_data").autocomplete({ source: user_array });
    }
);
}

function autocomplete(inp, arr) {
    /*the autocomplete function takes two arguments,
      the text field element and an array of possible autocompleted values:*/
    // console.log(inp);
    // console.log(arr);
    var currentFocus;
    /*execute a function when someone writes in the text field:*/
    inp.addEventListener("input", function(e) {
        var a, b, i, val = this.value;
        /*close any already open lists of autocompleted values*/
        closeAllLists();
        if (!val) { return false; }
        currentFocus = -1;
        /*create a DIV element that will contain the items (values):*/
        a = document.createElement("DIV");
        a.setAttribute("id", this.id + "autocomplete-list");
        a.setAttribute("class", "autocomplete-items");
        /*append the DIV element as a child of the autocomplete container:*/
        this.parentNode.appendChild(a);
        /*for each item in the array...*/
        for (i = 0; i < arr.length; i++) {
            /*check if the item starts with the same letters as the text field value:*/
            if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                /*create a DIV element for each matching element:*/
                b = document.createElement("DIV");
                /*make the matching letters bold:*/
                b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
                b.innerHTML += arr[i].substr(val.length);
                /*insert a input field that will hold the current array item's value:*/
                b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                /*execute a function when someone clicks on the item value (DIV element):*/
                b.addEventListener("click", function(e) {
                    /*insert the value for the autocomplete text field:*/
                    inp.value = this.getElementsByTagName("input")[0].value;
                    /*close the list of autocompleted values,
                      (or any other open lists of autocompleted values:*/
                    closeAllLists();
                });
                a.appendChild(b);
            }
        }
    });
    /*execute a function presses a key on the keyboard:*/
    inp.addEventListener("keydown", function(e) {
        var x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
            /*If the arrow DOWN key is pressed,
              increase the currentFocus variable:*/
            currentFocus++;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 38) { //up
            /*If the arrow UP key is pressed,
              decrease the currentFocus variable:*/
            currentFocus--;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode == 13) {
            /*If the ENTER key is pressed, prevent the form from being submitted,*/
            e.preventDefault();
            if (currentFocus > -1) {
                /*and simulate a click on the "active" item:*/
                if (x) x[currentFocus].click();
            }
        }
    });

    function addActive(x) {
        /*a function to classify an item as "active":*/
        if (!x) return false;
        /*start by removing the "active" class on all items:*/
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        /*add class "autocomplete-active":*/
        x[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) {
        /*a function to remove the "active" class from all autocomplete items:*/
        for (var i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(elmnt) {
        /*close all autocomplete lists in the document,
          except the one passed as an argument:*/
        var x = document.getElementsByClassName("autocomplete-items");
        for (var i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }
    /*execute a function when someone clicks in the document:*/
    document.addEventListener("click", function(e) {
        closeAllLists(e.target);
    });
}




function query_form() {
    for (let i = 0; i < document.getElementById('myModal2').getElementsByTagName('label').length; i++) {

        document.getElementById('myModal2').getElementsByTagName('label')[i].setAttribute("for", document.getElementById('myModal2').getElementsByTagName('label')[i].getAttribute("for") + "2")
            //console.log(document.getElementById('myModal2').getElementsByTagName('label')[i].getAttribute('for'))
    }

    for (let i = 0; i < document.getElementById('myModal2').querySelectorAll("[id*=id_]").length; i++) {
        document.getElementById('myModal2').querySelectorAll("[id*=id_]")[i].id += '2';
    }

}

function click(value) {
    // console.log(value);
    //alert(value);
    /*if(value.textContent === "Launch Gaia query"){
        if(document.getElementById('myModal2')){
            //document.getElementById('myModal2').remove();
        }
        document.getElementById('modals').appendChild(asdf);
        //var x = '<script>if(document.getElementById(\'id_shape_0\').checked){$(\"#div_id_radius\").show();$("#div_id_width").hide();$("#div_id_height").hide();$("#div_id_polygon").hide();} else if(document.getElementById(\'id_shape_1\').checked){$("#div_id_radius").hide();$("#div_id_width").show();$("#div_id_height").show();$("#div_id_polygon").hide();} else {$("#div_id_radius").hide();$("#div_id_width").hide();$("#div_id_height").hide();$("#div_id_polygon").show();}if(document.getElementById(\'id_name_coord_0\').checked){$("#div_id_name").show();$("#div_id_ra").hide();$("#div_id_dec").hide();$("#div_id_input_file").hide();$("#div_id_adql").hide()$("#data-form").show();}else if (document.getElementById(\'id_name_coord_1\').checked){$("#div_id_name").hide();$("#div_id_ra").show();$("#div_id_dec").show();$("#div_id_input_file").hide();$("#div_id_adql").hide()$("#data-form").show();}else if (document.getElementById(\'id_name_coord_2\').checked){$("#div_id_name").hide();$("#div_id_ra").hide();$("#div_id_dec").hide();$("#div_id_input_file").show();$("#div_id_adql").hide()$("#data-form").hide();}else if (document.getElementById(\'id_name_coord_3\').checked){$("#div_id_name").hide();$("#div_id_ra").hide();$("#div_id_dec").hide();$("#div_id_input_file").hide();$("#div_id_adql").show();$("#data-form").hide();}var positional = document.getElementById(\'id_positional_images_0\');if (positional != null){if(positional.checked){$("#div_id_instrument").hide();$("#div_id_level").hide();$("#div_id_table").show();}else{$("#div_id_instrument").show();$("#div_id_level").show();$("#div_id_table").hide();}}}</script>';
         //                                       document.getElementById('script').innerHTML = x;
    }else{
        if(document.getElementById('myModal')){
            //document.getElementById('myModal').remove();
        }
        document.getElementById('modals').appendChild(asdf2);
    }*/

}

function set_gaia_titles(name_coord_titles, shape_titles, data_release_titles, positional_images_titles, instrument_titles) {
    let array_name_coord_titles = name_coord_titles.split(",");
    let array_shape_titles = shape_titles.split(",");
    let array_data_release_titles = data_release_titles.split(",");

    document.querySelector("label[for='id_name_coord_0']").setAttribute('title', array_name_coord_titles[0]);
    document.querySelector("label[for='id_name_coord_1']").setAttribute('title', array_name_coord_titles[1]);
    document.querySelector("label[for='id_name_coord_2']").setAttribute('title', array_name_coord_titles[2]);
    document.querySelector("label[for='id_name_coord_3']").setAttribute('title', array_name_coord_titles[3]);

    document.querySelector("label[for='id_shape_0']").setAttribute('title', array_shape_titles[0]);
    document.querySelector("label[for='id_shape_1']").setAttribute('title', array_shape_titles[1]);
    document.querySelector("label[for='id_shape_2']").setAttribute('title', array_shape_titles[2]);

    document.querySelector("label[for='id_data_release_0']").setAttribute('title', array_data_release_titles[0]);
    document.querySelector("label[for='id_data_release_1']").setAttribute('title', array_data_release_titles[1]);

}

function set_hsa_titles(name_coord_titles, shape_titles, positional_images_titles, instrument_titles) {
    let array_name_coord_titles = name_coord_titles.split(",");
    let array_shape_titles = shape_titles.split(",");
    let array_positional_images_titles = positional_images_titles.split(",");
    let array_instrument_titles = instrument_titles.split(",");

    document.querySelector("label[for='id_name_coord_02']").setAttribute('title', array_name_coord_titles[0]);
    document.querySelector("label[for='id_name_coord_12']").setAttribute('title', array_name_coord_titles[1]);
    document.querySelector("label[for='id_name_coord_22']").setAttribute('title', array_name_coord_titles[2]);
    document.querySelector("label[for='id_name_coord_32']").setAttribute('title', array_name_coord_titles[3]);

    document.querySelector("label[for='id_shape_02']").setAttribute('title', array_shape_titles[0]);
    document.querySelector("label[for='id_shape_12']").setAttribute('title', array_shape_titles[1]);
    document.querySelector("label[for='id_shape_22']").setAttribute('title', array_shape_titles[2]);

    document.querySelector("label[for='id_positional_images_02']").setAttribute('title', array_positional_images_titles[0]);
    document.querySelector("label[for='id_positional_images_12']").setAttribute('title', array_positional_images_titles[1]);

    document.querySelector("label[for='id_instrument_02']").setAttribute('title', array_instrument_titles[0]);
    document.querySelector("label[for='id_instrument_12']").setAttribute('title', array_instrument_titles[1]);
    document.querySelector("label[for='id_instrument_22']").setAttribute('title', array_instrument_titles[2]);

}

$(document).ready(
    $(function() {
        var temp = "gaiadr2.gaia_source";
        $("#id_table_dr2").val(temp);
    }));

$(document).ready(
    function() {
        // init
        if (document.getElementById('id_shape_0').checked) {
            $("#div_id_radius").show();
            $("#div_id_width").hide();
            $("#div_id_height").hide();
            $("#div_id_polygon").hide();
        } else if (document.getElementById('id_shape_1').checked) {
            $("#div_id_radius").hide();
            $("#div_id_width").show();
            $("#div_id_height").show();
            $("#div_id_polygon").hide();
        } else {
            $("#div_id_radius").hide();
            $("#div_id_width").hide();
            $("#div_id_height").hide();
            $("#div_id_polygon").show();
        }
        if (document.getElementById('id_name_coord_0').checked) {
            $("#div_id_name").show();
            $("#div_id_ra").hide();
            $("#div_id_dec").hide();
            $("#div_id_input_file").hide();
            $("#div_id_adql").hide()
            $("#data-form").show();
        } else if (document.getElementById('id_name_coord_1').checked) {
            $("#div_id_name").hide();
            $("#div_id_ra").show();
            $("#div_id_dec").show();
            $("#div_id_input_file").hide();
            $("#div_id_adql").hide()
            $("#data-form").show();
        } else if (document.getElementById('id_name_coord_2').checked) {
            $("#div_id_name").hide();
            $("#div_id_ra").hide();
            $("#div_id_dec").hide();
            $("#div_id_input_file").show();
            $("#div_id_adql").hide()
            $("#data-form").hide();
        } else if (document.getElementById('id_name_coord_3').checked) {
            $("#div_id_name").hide();
            $("#div_id_ra").hide();
            $("#div_id_dec").hide();
            $("#div_id_input_file").hide();
            $("#div_id_adql").show();
            $("#data-form").hide();
        }
        var positional = document.getElementById('id_positional_images_0');
        if (positional != null) {
            if (positional.checked) {
                $("#div_id_instrument").hide();
                $("#div_id_level").hide();
                $("#div_id_table").show();
            } else {
                $("#div_id_instrument").show();
                $("#div_id_level").show();
                $("#div_id_table").hide();
            }
        }
        var dr = document.getElementById('id_data_release_0');
        if (dr != null) {
            if (dr.checked) {
                $("#div_id_table").show();
                $("#div_id_table_dr2").hide();
            } else {
                $("#div_id_table").hide();
                $("#div_id_table_dr2").show();
            }
        }
        // on change
        $("#id_shape_0").change(
            function() {
                //$('label[for=id_ra], input#id_ra').hide()
                $("#div_id_radius").show();
                $("#div_id_width").hide();
                $("#div_id_height").hide();
                $("#div_id_polygon").hide();
            });
        $("#id_shape_1").change(
            function() {
                $("#div_id_radius").hide();
                $("#div_id_width").show();
                $("#div_id_height").show();
                $("#div_id_polygon").hide();
            });
        $("#id_shape_2").change(
            function() {
                $("#div_id_radius").hide();
                $("#div_id_width").hide();
                $("#div_id_height").hide();
                $("#div_id_polygon").show();
            });
        $("#id_name_coord_0").change(
            function() {
                $("#div_id_name").show();
                $("#div_id_ra").hide();
                $("#div_id_dec").hide();
                $("#div_id_input_file").hide();
                $("#div_id_adql").hide();
                $("#data-form").show();
            });
        $("#id_name_coord_1").change(
            function() {
                $("#div_id_name").hide();
                $("#div_id_ra").show();
                $("#div_id_dec").show();
                $("#div_id_input_file").hide();
                $("#div_id_adql").hide();
                $("#data-form").show();
            });
        $("#id_name_coord_2").change(
            function() {
                $("#div_id_name").hide();
                $("#div_id_ra").hide();
                $("#div_id_dec").hide();
                $("#div_id_input_file").show();
                $("#div_id_adql").hide();
                $("#data-form").hide();
            });
        $("#id_name_coord_3").change(
            function() {
                $("#div_id_name").hide();
                $("#div_id_ra").hide();
                $("#div_id_dec").hide();
                $("#div_id_input_file").hide();
                $("#div_id_adql").show();
                $("#data-form").hide();
            });
        $("#id_positional_images_0").change(
            function() {
                $("#div_id_instrument").hide();
                $("#div_id_level").hide();
                $("#div_id_table").show();
            }
        );
        $("#id_positional_images_1").change(
            function() {
                $("#div_id_instrument").show();
                $("#div_id_level").show();
                $("#div_id_table").hide();
            }
        );
        $("#id_data_release_0").change(
            function() {
                $("#div_id_table").show();
                $("#div_id_table_dr2").hide();
            }
        );
        $("#id_data_release_1").change(
            function() {
                $("#div_id_table").hide();
                $("#div_id_table_dr2").show();
            }
        );
    });

$(document).ready(
    function() {
        $(".radio-circle").change(
            function() {
                $(".row-radius-input").show();
                $(".row-rectangle-input").hide();
                $(".row-polygon-input").hide();
            });
    });
$(document).ready(
    function() {
        $(".radio-rectangle").change(
            function() {
                $(".row-radius-input").hide();
                $(".row-rectangle-input").show();
                $(".row-polygon-input").hide();
            });
    });
$(document).ready(
    function() {
        $(".radio-polygon").change(
            function() {
                $(".row-radius-input").hide();
                $(".row-rectangle-input").hide();
                $(".row-polygon-input").show();
            });
    });

$(document).ready(
    function() {
        $("#gaia-tables-dropdown-menu li a").click(
            function() {
                $("#gaia-table-dropdown").text($(this).text());
                $("#gaia-table-dropdown").val($(this).val());
                var element = document.getElementById('gaia-table-input');
                if (element === null) {
                    var input = $("<input>")
                        .attr("type", "hidden")
                        .attr("id", "gaia-table-input")
                        .attr("name", "gaia-table-input").val($(this).text());
                    $("#gaia_query_form").append($(input));
                } else {
                    $("#gaia-table-input").val($(this).text());
                }
            });
    });






$(document).ready(
    function() {
        // init
        if (document.getElementById('id_shape_02').checked) {
            $("#div_id_radius2").show();
            $("#div_id_width2").hide();
            $("#div_id_height2").hide();
            $("#div_id_polygon2").hide();
        } else if (document.getElementById('id_shape_12').checked) {
            $("#div_id_radius2").hide();
            $("#div_id_width2").show();
            $("#div_id_height2").show();
            $("#div_id_polygon2").hide();
        } else {
            $("#div_id_radius2").hide();
            $("#div_id_width2").hide();
            $("#div_id_height2").hide();
            $("#div_id_polygon2").show();
        }
        if (document.getElementById('id_name_coord_02').checked) {
            $("#div_id_name2").show();
            $("#div_id_ra2").hide();
            $("#div_id_dec2").hide();
            $("#div_id_input_file2").hide();
            $("#div_id_adql2").hide()
            $("#data-form2").show();
        } else if (document.getElementById('id_name_coord_12').checked) {
            $("#div_id_name2").hide();
            $("#div_id_ra2").show();
            $("#div_id_dec2").show();
            $("#div_id_input_file2").hide();
            $("#div_id_adql2").hide()
            $("#data-form2").show();
        } else if (document.getElementById('id_name_coord_22').checked) {
            $("#div_id_name2").hide();
            $("#div_id_ra2").hide();
            $("#div_id_dec2").hide();
            $("#div_id_input_file2").show();
            $("#div_id_adql2").hide()
            $("#data-form2").hide();
        } else if (document.getElementById('id_name_coord_32').checked) {
            $("#div_id_name2").hide();
            $("#div_id_ra2").hide();
            $("#div_id_dec2").hide();
            $("#div_id_input_file2").hide();
            $("#div_id_adql2").show();
            $("#data-form2").hide();
        }
        var positional = document.getElementById('id_positional_images_02');
        if (positional != null) {
            if (positional.checked) {
                $("#div_id_instrument2").hide();
                $("#div_id_level2").hide();
                $("#div_id_table2").show();
            } else {
                $("#div_id_instrument2").show();
                $("#div_id_level2").show();
                $("#div_id_table2").hide();
            }
        }
        var dr = document.getElementById('id_data_release_02');
        if (dr != null) {
            if (dr.checked) {
                $("#div_id_table2").show();
                $("#div_id_table_dr22").hide();
            } else {
                $("#div_id_table2").hide();
                $("#div_id_table_dr22").show();
            }
        }
        // on change
        $("#id_shape_02").change(
            function() {
                //$('label[for=id_ra], input#id_ra').hide()
                $("#div_id_radius2").show();
                $("#div_id_width2").hide();
                $("#div_id_height2").hide();
                $("#div_id_polygon2").hide();
            });
        $("#id_shape_12").change(
            function() {
                $("#div_id_radius2").hide();
                $("#div_id_width2").show();
                $("#div_id_height2").show();
                $("#div_id_polygon2").hide();
            });
        $("#id_shape_22").change(
            function() {
                $("#div_id_radius2").hide();
                $("#div_id_width2").hide();
                $("#div_id_height2").hide();
                $("#div_id_polygon2").show();
            });
        $("#id_name_coord_02").change(
            function() {
                $("#div_id_name2").show();
                $("#div_id_ra2").hide();
                $("#div_id_dec2").hide();
                $("#div_id_input_file2").hide();
                $("#div_id_adql2").hide();
                $("#data-form2").show();
            });
        $("#id_name_coord_12").change(
            function() {
                $("#div_id_name2").hide();
                $("#div_id_ra2").show();
                $("#div_id_dec2").show();
                $("#div_id_input_file2").hide();
                $("#div_id_adql2").hide();
                $("#data-form2").show();
            });
        $("#id_name_coord_22").change(
            function() {
                $("#div_id_name2").hide();
                $("#div_id_ra2").hide();
                $("#div_id_dec2").hide();
                $("#div_id_input_file2").show();
                $("#div_id_adql2").hide();
                $("#data-form2").hide();
            });
        $("#id_name_coord_32").change(
            function() {
                $("#div_id_name2").hide();
                $("#div_id_ra2").hide();
                $("#div_id_dec2").hide();
                $("#div_id_input_file2").hide();
                $("#div_id_adql2").show();
                $("#data-form2").hide();
            });
        $("#id_positional_images_02").change(
            function() {
                $("#div_id_instrument2").hide();
                $("#div_id_level2").hide();
                $("#div_id_table2").show();
            }
        );
        $("#id_positional_images_12").change(
            function() {
                $("#div_id_instrument2").show();
                $("#div_id_level2").show();
                $("#div_id_table2").hide();
            }
        );
        $("#id_data_release_02").change(
            function() {
                $("#div_id_table2").show();
                $("#div_id_table_dr22").hide();
            }
        );
        $("#id_data_release_12").change(
            function() {
                $("#div_id_table2").hide();
                $("#div_id_table_dr22").show();
            }
        );
    });

$(document).ready(
    function() {
        $(".radio-circle").change(
            function() {
                $(".row-radius-input").show();
                $(".row-rectangle-input").hide();
                $(".row-polygon-input").hide();
            });
    });
$(document).ready(
    function() {
        $(".radio-rectangle").change(
            function() {
                $(".row-radius-input").hide();
                $(".row-rectangle-input").show();
                $(".row-polygon-input").hide();
            });
    });
$(document).ready(
    function() {
        $(".radio-polygon").change(
            function() {
                $(".row-radius-input").hide();
                $(".row-rectangle-input").hide();
                $(".row-polygon-input").show();
            });
    });

$(document).ready(
    function() {
        $("#gaia-tables-dropdown-menu li a").click(
            function() {
                $("#gaia-table-dropdown").text($(this).text());
                $("#gaia-table-dropdown").val($(this).val());
                var element = document.getElementById('gaia-table-input');
                if (element === null) {
                    var input = $("<input>")
                        .attr("type", "hidden")
                        .attr("id", "gaia-table-input")
                        .attr("name", "gaia-table-input").val($(this).text());
                    $("#gaia_query_form").append($(input));
                } else {
                    $("#gaia-table-input").val($(this).text());
                }
            });
    });