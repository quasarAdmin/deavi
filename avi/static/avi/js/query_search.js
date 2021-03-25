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
var search_array = [];
var all_queries = [];
var reload = false;

function search(id, mission) {
    var el = $("#_query-container");
    var content = "";
    var instrument = false;
    var entrar = true;
    if (entrar) {
        el.attr("loaded", "true");
        el.append('<p id="temp_p_' + id + '">Loading results for the query ' + id + "...</p>");
        $.ajax({
            type: "POST",
            url: avi_url + "avi/ajax/get_query_info",
            dataType: 'json',
            data: {
                'id': id,
                'mission': mission,
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
            },
            success: function(data) {
                content = '<div id="reluts_query" class="row">' + '<div class="col-sm-5 offset-sm-1 mt-3 query_parameters"><div class="card border-primary"><div class="card-body">' + '<h4 class="text-center">Query Parameters</h4>';
                for (var i = 0; i < data.length; i++) {
                    if (data[i][0] != 'nofile' && data[i][0] != 'files' && data[i][0] != 'params' && data[i][0] != 'instrument' && data[i][0] != 'table' && data[i][0] != 'positional_images') {
                        content += '<p class="card-text" style="text-transform: capitalize"><span class="font-weight-bold">' + data[i][0] + ':</span> ' + data[i][1] + '</br></p>';
                    }
                    if (data[i][0] === 'instrument') {
                        instrument = true;
                        content += '<p class="card-text" style="text-transform: capitalize"><span class="font-weight-bold">' + data[i][0] + ':</span> ' + data[i][1] + '</br></p>';
                    }
                    if (!instrument && data[i][0] === 'table') {
                        content += '<p class="card-text" style="text-transform: capitalize"><span class="font-weight-bold">' + data[i][0] + ':</span> ' + data[i][1] + '</br></p>';
                    }
                    if (data[i][0] === 'params' && data[i][1].length > 0) {
                        content += '<p class="card-text" style="text-transform: capitalize"><span class="font-weight-bold">' + data[i][0] + ':</span> ' + data[i][1] + '</br></p>';
                    }
                }
                content += '</div></div></div>';

                content += '<div class="col-sm-5 mt-3 mb-3 query_files"><div class="card border-primary"><div class="card-body"><h4 class="text-center">Files</h4>';
                if (data[data.length - 1][0] === 'files') {

                    $.each(data[data.length - 1][1], function(key, value) {
                        content += '<div id="file_btn_group_' + key + '">';
                        var e = $("#file_btn_group_" + key);


                        if (mission == "gaia") {
                            u = avi_url + "avi/api/res/" + key;
                        } else {
                            u = "#";
                        }
                        content += '<a class="btn-group a-link" target="_blank" href="' + u + '" style="display: block; width: 100%; overflow: hidden;white-space: nowrap;text-overflow: ellipsis;" data-toggle="tooltip" data-pacement="top" title="' + value + '">' + value + "</a></br>";
                        content += '</div>';
                    });

                } else {
                    content += '<p>This query has no files</p>';
                }
                content += '</div></div></div></div>';
                el.append(content);
                $("#temp_p_" + id).attr("style", "display: none");
            },
            error: function(xhr, textStatus, throwError) {
                $("#temp_p_" + id).attr("style", "display: none");
                el.append("<h4>An error occurred while retrieving the query information</h4>");
            }
        });
    }
}

function searchQ() {
    var variable = document.getElementById('search').value;
    variable = variable.replace(/\s/g, '');
    var variable_parts = variable.split('-');
    document.getElementById('modal-title').innerHTML = "";
    if (document.getElementById('reluts_query')) {
        document.getElementById('reluts_query').remove();
    }
    if (document.getElementById('search').value) {
        search(variable_parts[1], variable_parts[2]);
        let date = document.getElementById(variable_parts[2] + "_" + variable_parts[1]).getAttribute('data').split('_')[0];
        let status = document.getElementById(variable_parts[2] + "_" + variable_parts[1]).getAttribute('data').split('_')[1];
        variable_parts[0] = variable_parts[0].charAt(0).toUpperCase() + variable_parts[0].slice(1);
        document.getElementById('modal-title').innerHTML = variable_parts[0] + " " + variable_parts[1] + " - " + date;
        document.getElementById('form_launch_button').setAttribute('value', variable_parts[1] + "-" + variable_parts[2]);
    }
    if (document.getElementById('temp_p_' + variable_parts[1])) {
        document.getElementById('temp_p_' + variable_parts[1]).remove();
    }
}

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
    /*var elements = document.getElementsByClassName("name_search");
    var data_id = document.getElementsByClassName("qs-res");
    var aux = [];
    for(let j = 0; j < data_id.length; j++){
        aux.push(data_id[j].id.slice(11));
        aux[j] = aux[j].split('_')[0];
    }
    for(let i = 0; i < elements.length; i++){
        search_array.push(elements.item(i).textContent + "- " + aux[i]);
    }
    $(".search_bar").autocomplete({ source: search_array });*/
    for (let i = 0; i < all_queries.length; i++) {
        search_array.push(all_queries[i].name + " - " + all_queries[i].pk + " - " + all_queries[i].mission);
    }
    $(".search_bar").autocomplete({ source: search_array });
};

function take_all_queries(name, status, date, pk, mission) {
    var obj = { name: name, status: status, date: date, pk: pk, mission: mission };
    all_queries.push(obj);
}

function test() {
    console.log(all_queries);
}

function make_divs() {
    for (let i = 0; i < all_queries.length; i++) {
        if (!document.getElementById(all_queries[i].mission + "_" + all_queries[i].pk)) {
            var hidden_q = document.createElement("div");
            //all_queries[i] = data_parameters[i].replace(/&#39;/g, "'");
            hidden_q.setAttribute("id", all_queries[i].mission + "_" + all_queries[i].pk);
            hidden_q.setAttribute("mission", all_queries[i].mission);
            hidden_q.setAttribute("qid", all_queries[i].pk);
            hidden_q.setAttribute("data", all_queries[i].date + "_" + all_queries.status);
            document.getElementById('hidden_q').appendChild(hidden_q);
        }
    }
}
$(document).ready(
    function check_page() {
        for (let i = 0; i < all_queries.length; i++) {
            if (all_queries[i].status != 'SUCCESS' && all_queries[i].status != 'FAILURE') {
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
            url: avi_url + "avi/queries/status",
            data: {
                'poll': 'yes',
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
            },
            success: function(data) {
                //console.log(data.slice(data.indexOf('card-body'), data.indexOf('end_scripts')));
                var state = data.slice(data.indexOf('card-body'), data.indexOf('end_scripts'));
                if (state.includes('PENDING') || state.includes('STARTED')) {
                    let alert = '<div id="alert-info" class="alert alert-info" role="alert">Query started, the page will be reloaded when finished</div>';
                    if (document.getElementById('alert-info') == null) {
                        document.getElementById('alert').innerHTML = alert;
                    }
                    setTimeout(do_poll, 5000);
                } else if (reload) {
                    window.location.reload();
                    console.log("refresh");
                }
            }
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
    function() {
        var title_elements = $('.query-info');
        var title_elements_id_mission = [];
        for (let i = 0; i < title_elements.length; i++) {
            title_elements_id_mission.push({ id: title_elements[i].id, mission: title_elements[i].attributes[2].value });
        }
        for (let j = 0; j < title_elements_id_mission.length; j++) {
            $.ajax({
                type: "POST",
                url: avi_url + "avi/ajax/get_query_info",
                dataType: 'json',
                data: {
                    'id': title_elements_id_mission[j].id.split('_')[1],
                    'mission': title_elements_id_mission[j].mission,
                    csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
                },
                success: function(data) {

                    var instrument = false;
                    var title = '';
                    title = "Mission: " + title_elements_id_mission[j].mission + "\n" + "Params:\n";
                    for (let i = 0; i < data.length; i++) {
                        if (data[i][0] != 'nofile' && data[i][0] != 'files' && data[i][0] != 'params' && data[i][0] != 'instrument' && data[i][0] != 'table' && data[i][0] != 'positional_images') {
                            title += '\t' + data[i][0] + ': ' + data[i][1] + '\n';
                        }
                        if (data[i][0] === 'instrument') {
                            instrument = true;
                            title += '\t' + data[i][0] + ': ' + data[i][1] + '\n';
                        }
                        if (!instrument && data[i][0] === 'table') {
                            title += '\t' + data[i][0] + ': ' + data[i][1] + '\n';
                        }
                        if (data[i][0] === 'params' && data[i][1].length > 0) {
                            title += '\t' + data[i][0] + ': ' + data[i][1] + '\n';
                        }
                    }
                    if (data[data.length - 1][0] === 'files') {
                        title += 'Files:\n'
                        $.each(data[data.length - 1][1], function(key, value) {
                            title += '\t' + value + '\n'
                        })
                    }

                    var element = document.getElementById(title_elements_id_mission[j].id);
                    element.setAttribute("title", title);
                },
                error: function(xhr, textStatus, throwError) {
                    var element = document.getElementById(title_elements_id_mission[j].id);
                    element.setAttribute("title", 'Error');
                }
            })
        }
    });