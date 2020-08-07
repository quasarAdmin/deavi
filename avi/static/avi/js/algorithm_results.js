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
