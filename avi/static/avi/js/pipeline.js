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

var gaia_array = [];
var hsa_array = [];
var res_array = [];
var user_array = [];
var reload = false;

function popup_algorithm(url) {
    console.log('popup');
    console.log(url);
    $.ajax({
        url: url,
        success: function(data) {
            console.log(data);
            $("#dialog-form").load(data).dialog({ modal: true }); //.dialog('open');
            $("#dialog-form").html(data);
        }
    })
    return false;
}

$(document).ready(function() {
    var forms = document.getElementsByClassName("alg-button");
    for (var i = 0; i < forms.length; i++) {
        var row_id = forms.item(i).id.substring(4);
        var el = document.getElementById(row_id);
        el.style.display = 'none';
    }
    $(".alg-button").click(
        function() {
            var row_id = this.id.substring(4);
            var el = document.getElementById(row_id);
            if (el.style.display == 'none') {
                el.style.display = 'block';
            } else {
                el.style.display = 'none';
            }
        }
    );
});

$(document).ready(
    function() {
        $(".dropdown-menu li a").click(
            function() {
                var type = $(this).attr("type");
                var id = $(this).attr("id");
                var the_name = $(this).attr("the_name");
                var button_id = "#" + the_name + "_" + id + "_dropdown";
                var input_id = the_name + "_" + id;
                console.log(button_id);
                console.log(input_id);
                $(button_id).text($(this).text());
                $(button_id).val($(this).val());
                var element = document.getElementById(input_id);
                if (element === null) {
                    var input = $("<input>")
                        .attr("type", "hidden")
                        .attr("id", input_id)
                        .attr("name", input_id)
                        .val($(this).text());
                    $("#" + the_name + "_form").append($(input));
                } else {
                    $("#" + input_id).val($(this).text());
                }
            });
    });

$(document).ready(
    function() {
        $(".alg-info").click(
            function() {
                //console.log("click");
                var id = $(this).attr("id");
                var res_id = "#div_alg-res_" + id;
                if ($(res_id).css('display') == 'none') {
                    $(res_id).show();
                    get_results(id);
                } else {
                    $(res_id).hide();
                }
            });
    });
$(document).ready(
    function() {
        $(".sort-by-date").click(
            function() {
                $.ajax({
                    type: "POST",
                    url: avi_url + "avi/status",
                    data: {
                        'sort_by': 'date',
                        csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
                    },
                    success: function() {
                        window.location.reload();
                    }
                });
            });
    });
$(document).ready(
    function() {
        $(".sort-by-status").click(
            function() {
                $.ajax({
                    type: "POST",
                    url: avi_url + "avi/status",
                    data: {
                        'sort_by': 'status',
                        csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
                    },
                    success: function() {
                        window.location.reload();
                    }
                });
            });
    });

$(document).ready(
    function() {
        $(".sort-by-name").click(
            function() {
                $.ajax({
                    type: "POST",
                    url: avi_url + "avi/status",
                    data: {
                        'sort_by': 'name',
                        csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
                    },
                    success: function() {
                        window.location.reload();
                    }
                });
            });
    });

function check_order(ordby) {
    if (ordby === 'name') {
        document.getElementsByClassName('name-sort')[0].className = 'fas fa-sort-up name-sort';
    } else if (ordby === '-name') {
        document.getElementsByClassName('name-sort')[0].className = 'fas fa-sort-down name-sort';
    } else if (ordby === 'date') {
        document.getElementsByClassName('date-sort')[0].className = 'fas fa-sort-up date-sort';
    } else if (ordby === '-date') {
        document.getElementsByClassName('date-sort')[0].className = 'fas fa-sort-down date-sort';
    } else if (ordby === 'status') {
        document.getElementsByClassName('status-sort')[0].className = 'fas fa-sort-up status-sort';
    } else if (ordby === '-status') {
        document.getElementsByClassName('status-sort')[0].className = 'fas fa-sort-down status-sort';
    }
}
$(document).ready(
    function check_page() {
        for (let i = 0; i < alldata.length; i++) {
            console.log(alldata[i].status);
            if (alldata[i].status != 'SUCCESS' && alldata[i].status != 'FAILURE') {
                reload = true;
                break;
            } else {
                reload = false;
            }
        }
    });
$(document).ready(
    function do_poll() {
        //return;
        console.log("polling");
        $.ajax({
            type: "POST",
            url: avi_url + "avi/status",
            data: {
                'poll': 'yes',
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
            },
            success: function(data) {
                //console.log(data.slice(data.indexOf('card-body'), data.indexOf('end_scripts')));
                var state = data.slice(data.indexOf('card-body'), data.indexOf('end_scripts'));
                if (state.includes('PENDING') || state.includes('STARTED')) {
                    let alert = '<div id="alert-info" class="alert alert-info" role="alert">Algorithm started, the page will be reloaded when finished</div>';
                    if (document.getElementById('alert-info') == null) {
                        document.getElementById('alert').innerHTML = alert;
                    }
                    setTimeout(do_poll, 5000);
                } else if (reload) {
                    //window.location.reload();
                    window.location = window.location.href;
                    console.log("refresh");
                }
            }
        });
    });
//----- function title for the title of the algorithm -----
function title(id) {
    var parameters = document.getElementById(id);
    parameters = parameters.getAttribute('params');
    console.log(parameters);
    eval('var algorithm=' + parameters);
    var title = "Name: " + algorithm.algorithm.name + "\n" + "Params:\n";
    var keys = Object.keys(algorithm.algorithm.params);
    for (var i = 0; i < keys.length; i++) {
        if (algorithm.algorithm.params[keys[i]].toString().includes("/")) {
            if (algorithm.algorithm.params[keys[i]].charAt(algorithm.algorithm.params[keys[i]].length - 1) != "/") {
                title += "\t" + keys[i] + ": " + algorithm.algorithm.params[keys[i]].slice(algorithm.algorithm.params[keys[i]].lastIndexOf("/") + 1, algorithm.algorithm.params[keys[i]].length) + "\n";
            }
        } else {
            title += "\t" + keys[i] + ": " + algorithm.algorithm.params[keys[i]] + "\n";
        }
    }
    var element = document.getElementById(id);
    element.setAttribute("title", title);
};
//----- function relaunch for the relaunch of the algorithm -----
var create_form = function(el, id, data, params) {
    var view_name = data['view_name'];
    var form = $('<form></form>', {
        method: 'post',
        id: 'alg_info_form'
    });
    console.log(params)
    var token = document.getElementsByName('csrfmiddlewaretoken')[1].value;
    document.getElementById("div_alg_info").className = "text-center col-sm-12";
    document.getElementById("div_alg_info").setAttribute("style", "width:100%");
    form.append('<input name="csrfmiddlewaretoken" value="' +
        token + '" type="hidden">');
    form.append('<h3>Relaunch of ' + view_name + '</h3>');
    $.each(data['input'], function(k, v) {
        var div_row = $('<div class="row"></div>');
        var div = $('<div class="col-sm-12"></div>');
        var inp_id = id + "_" + v['name'];
        if (v['type'] == "bool") {
            div.append("<label>" + v['view_name'] + "</label>");
            div.append('<input name="' + id + "_" + v['name'] +
                '" type="checkbox" value="true">');
            form.append(div);
        } else if (v['type'] == "string" ||
            v['type'] == "float" ||
            v['type'] == "integer" ||
            v['type'] == "long" ||
            v['type'] == "complex") {
            var adiv = $('<div class="row" style="width:100%; margin-top:5px"></div>');
            adiv.append('<label class = "col-sm-5 col-form-label" style="padding: 5px 0px 0px 0px">' + v['view_name'] + "</label>");
            var ainput = $('<input name="' + id + "_" + v['name'] +
                '" type="text" class="col-sm-7 form-control" value="' + params[v['view_name']] + '">');
            adiv.append(ainput);
            div.append(adiv);
            div_row.append(div);
            form.append(div_row);
        } else if (v['type'] == "gaia_table") {
            var adiv = $('<div class="autocomplete row" style="width:100%; margin-top:5px"></div>');
            adiv.append('<label class = "col-sm-5 col-form-label">' + v['view_name'] + "</label>");
            var ainput = $('<input name="' + id + "_" + v['name'] +
                '" id="' + inp_id +
                '" class="gaia_table col-sm-7 form-control ui-autocomplete-input"' +
                ' type="text" placeholder="Gaia Table" value="' + params[v['view_name']].slice(params[v['view_name']].lastIndexOf("/") + 1, params[v['view_name']].length) + '" autocomplete="off">');
            adiv.append(ainput);
            div.append(adiv);
            div_row.append(div);
            form.append(div_row);
        } else if (v['type'] == "hsa_table") {
            var adiv = $('<div class="autocomplete row" style="width:100%; margin-top:5px"></div>');
            adiv.append('<label class = "col-sm-5 col-form-label">' + v['view_name'] + "</label>");
            adiv.append('<input name="' + id + "_" + v['name'] +
                '" id="' + inp_id +
                '" class="hsa_table col-sm-7 form-control"' +
                ' type="text" placeholder="HSA Table" value="' + params[v['view_name']].slice(params[v['view_name']].lastIndexOf("/") + 1, params[v['view_name']].length) + '">');
            div.append(adiv);
            div_row.append(div);
            form.append(div_row);
        } else if (v['type'] == "results_data") {
            var adiv = $('<div class="autocomplete row" style="width:100%; margin-top:5px"></div>');
            if ("info" in v) {
                adiv.append('<label class = "col-sm-5 col-form-label" title="' + v["info"] + '">' + v['view_name'] + "</label>");
            } else {
                adiv.append('<label class = "col-sm-5 col-form-label">' + v['view_name'] + "</label>");
            }
            adiv.append('<input name="' + id + "_" + v['name'] +
                '" id="' + inp_id +
                '" class="results_data col-sm-7 form-control"' +
                ' type="text" placeholder="Results Data" value="' + params[v['view_name']].slice(params[v['view_name']].lastIndexOf("/") + 1, params[v['view_name']].length) + '">');
            div.append(adiv);
            div_row.append(div);
            form.append(div_row);
            //get_files_list("hsa");
            //document.getElementById(inp_id)
            //autocomplete(adiv[0], text_array);
        } else if (v['type'] == "user_data") {
            var adiv = $('<div class="autocomplete row" style="width:100%; margin-top:5px"></div>');
            if ("info" in v) {
                adiv.append('<label class = "col-sm-5 col-form-label" title="' + v["info"] + '">' + v['view_name'] + "</label>");
            } else {
                adiv.append('<label class = "col-sm-5 col-form-label">' + v['view_name'] + "</label>");
            }
            adiv.append('<input name="' + id + "_" + v['name'] +
                '" id="' + inp_id +
                '" class="user_data col-sm-7 form-control"' +
                ' type="text" placeholder="User Data" value="' + params[v['view_name']].slice(params[v['view_name']].lastIndexOf("/") + 1, params[v['view_name']].length) + '">');
            div.append(adiv);
            div_row.append(div);
            form.append(div_row);
            //get_files_list("hsa");
            //document.getElementById(inp_id)
            //autocomplete(adiv[0], text_array);
        }
    });
    form.append('<button name="algorithm_id" class="btn btn-outline-primary" style="margin-top:5px; margin-bottom: 5px" type="submit" value="' +
        id + '">Run</button>');

    el.append(form);
}
var get_algorithm_info = function(el, id, params) { //, name){
    setTimeout(2000);
    $.ajax({
        type: "POST",
        url: avi_url + "avi/ajax/get_alg_info",
        dataType: 'json',
        data: {
            'id': id,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success: function(data) {
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
            create_form(el, id, data['algorithm'], params);
        },
        error: function(xhr, textStatus, throwError) {
            console.log(xhr);
        },
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    });
}

function relaunch() {
    var element = document.getElementById('relaunch');
    element = element.getAttribute('params');
    eval('var algorithm=' + element);
    var info_id = "div_alg_info";
    var node = document.getElementById(info_id);
    while (node.firstChild) {
        node.removeChild(node.firstChild);
    }
    get_algorithm_info($("#" + info_id), algorithm.pk, algorithm.params);

};

function autocomp() {
    var info_id = "#div_alg_info";
    var node = $(info_id);
    console.log("here" + gaia_array);
    node.on("DOMSubtreeModified",
        function() {
            console.log(gaia_array);
            $(".gaia_table").autocomplete({ source: gaia_array });
            $(".hsa_table").autocomplete({ source: hsa_array });
            $(".results_data").autocomplete({ source: res_array });
            $(".user_data").autocomplete({ source: user_array });
        }
    );
};