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
var get_plot = function(el, id){
    $.ajax({
            type:"POST",
            url:avi_url+"avi/ajax/get_plot",
            dataType:'json',
            data:{'id': id,
                 csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
            success: function(data){
                var content_plot = "";
                content_plot += '<div class="row"><div class="" style="margin:0 auto">';
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


function encode_utf8(s) {
    return unescape(encodeURIComponent(s));
}
var get_results = function(id){
    var el = $("#"+id+"_algorithm-container");
    if (el.attr("loaded") == "false"){
        el.attr("loaded", "true");
        el.append('<p id="temp_p_'+id+'">Loading results for the job '+id+"...</p>");
        
        $.ajax({
            type:"POST",
            url:avi_url+"avi/ajax/get_results",
            dataType:'json',
            data:{'id': id,
                 csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
            success: function(data){


                var element = document.getElementById(id);
                element = element.getAttribute('params');
                element = element.replace(/'/g,'"');
                console.log(element);
                //eval('var algorithm='+element);
                algorithm = JSON.parse(encode_utf8(element));
                var keys = Object.keys(algorithm.algorithm.params);
                var content = '<div class="row">'+'<div class="col-sm-5 offset-sm-1 mt-3 mb-3 query_parameters"><div class="card border-primary"><div class="card-body">'+'<h4 class="text-center">Parameters</h4>';
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
                            get_plot(el, k);
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
}
