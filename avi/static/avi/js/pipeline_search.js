var search_array = [];
var data_array = [];
var pk2 = [];
var data_parameters = [];
var date_array = [];
var alldata = [];
var get_plot_search = function(el, id){
    $.ajax({
            type:"POST",
            url:avi_url+"avi/ajax/get_plot",
            dataType:'json',
            data:{'id': id,
                 csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
            success: function(data){
                var content_plot = "";
                content_plot += '<div id="reluts_alg_plot" class="row"><div class="" style="margin:0 auto">';
                content_plot += data['html'];
                content_plot += data['sc'];
                content_plot += '</div></div>';
                el.append(content_plot);
            },
            error: function(xhr, textStatus, throwError){
                console.log(xhr);
            }
        });
}

var search_results = function(id){
    var el = $("#_algorithm-container");
        
        $.ajax({
            type:"POST",
            url:avi_url+"avi/ajax/get_results",
            dataType:'json',
            data:{'id': id,
                 csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
            success: function(data){


                var element = document.getElementById(id);
                element = element.getAttribute('params');
                eval('var algorithm='+element);
                var keys = Object.keys(algorithm.algorithm.params);
                var content = '<div id="reluts_alg" class="row">'+'<div class="col-sm-5 offset-sm-1 mt-3 mb-3 query_parameters"><div class="card border-primary"><div class="card-body">'+'<h4 class="text-center">Parameters</h4>';
                for(var i = 0; i < keys.length; i++){
                    if(algorithm.algorithm.params[keys[i]].toString().includes("/")){
                        if(algorithm.algorithm.params[keys[i]].charAt(algorithm.algorithm.params[keys[i]].length-1) != "/"){
                            content += '<p><span class="font-weight-bold" style="text-transform: capitalize">'+keys[i]+':</span> '+ algorithm.algorithm.params[keys[i]].slice(algorithm.algorithm.params[keys[i]].lastIndexOf("/")+1,algorithm.algorithm.params[keys[i]].length) + '</p>';
                        }
                    }else{
                        content += '<p><span class="font-weight-bold" style="text-transform: capitalize">' + keys[i] + ':</span> ' + algorithm.algorithm.params[keys[i]] + '</p>';
                    }
                }
                content +='</div></div></div>';
                

                $.each(data, function(key, value){
                    if (key == 'plots'){
                        $.each(value, function(k,v){
                            get_plot_search(el, k);
                        });
                    } else {
                        content+='<div class="col-sm-5 mt-3 mb-3 query_files"><div class="card border-primary"><div class="card-body"><h4 class="text-center">Output</h4>';
                        
                        $.each(value, function(k,v){
                            
                            u = avi_url+"avi/api/res/"+k;
                            content += '<a class="btn-group a-link" target="_blank" href="'+u+'" style="display: block; width: 100%; overflow: hidden;white-space: nowrap;text-overflow: ellipsis;" data-toggle="tooltip" data-pacement="top" title="' + v + '">'+v+"</a>";
                        });
                        if($.isEmptyObject(value)){
                            content += "<p>This algorithm has no output</p>";
                        }
                        content +='</div></div></div>';
                        el.append(content);
                    }
                });
                $("#temp_p_"+id).attr("style","display: none");
            },
            error: function(xhr, textStatus, throwError){
                $("#temp_p_"+id).attr("style","display: none");
                el.append("<h4>An error occurred while retrieving the execution results</h4>");
            }
        });
}
function searchP() {
    var variable = document.getElementById('search').value;
    variable = variable.replace(/\s/g,'');
    var variable_parts = variable.split('-');
    document.getElementById('modal-title').innerHTML = "";
    if(document.getElementById('reluts_alg')){
        document.getElementById('reluts_alg').remove();
    }
    if(document.getElementById('reluts_alg_plot')){
        document.getElementById('reluts_alg_plot').remove();
    }
    if(document.getElementById('search').value){
        search_results(variable_parts[1]);
        let date = document.getElementById(variable_parts[1]).getAttribute('data').split('_')[0];
        variable_parts[0] = variable_parts[0].charAt(0).toUpperCase() + variable_parts[0].slice(1);
        document.getElementById('modal-title').innerHTML = variable_parts[0] + " " + variable_parts[1] + " - " + date;
        document.getElementById('form_relaunch_button').setAttribute('value', document.getElementById(variable_parts[1]).getAttribute('params'));
    }
    if(document.getElementById('temp_p_'+variable_parts[1])){
        document.getElementById('temp_p_'+variable_parts[1]).remove();
    }
}
function enter_search(){
    var input = document.getElementById("search");
    input.addEventListener("keyup", function(event) {
      event.preventDefault();
      if (event.keyCode === 13) {
        document.getElementById("search_icon").click();
      }
    });
}
function auto_names() {
    for(let i = 0; i < alldata.length; i++){
        search_array.push(alldata[i].name + " - " + alldata[i].pk);
    }
    $(".search_bar").autocomplete({ source: search_array });
  };
function take_all_algorithms(name, pk, parameter, date, status){
    var obj = {name:name, pk:pk, parameter:parameter, date:date, status:status};
    alldata.push(obj);
}
function make_divs(){
    for(let i = 0; i < alldata.length; i++){
        if(!document.getElementById(alldata[i].pk)){
            var hidden_alg = document.createElement("div");
            alldata[i].parameter = alldata[i].parameter.replace(/&#39;/g, "'");
            hidden_alg.setAttribute("id", alldata[i].pk);
            hidden_alg.setAttribute("params", alldata[i].parameter);
            hidden_alg.setAttribute("data", alldata[i].date);
            document.getElementById('hidden_alg').appendChild(hidden_alg);
        }
    }
}
