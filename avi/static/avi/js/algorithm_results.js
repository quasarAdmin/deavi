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
    console.log(id);
    $.ajax({
            type:"POST",
            url:avi_url+"avi/ajax/get_plot",
            dataType:'json',
            data:{'id': id,
                 csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
            success: function(data){           
                el.append(data['html']);
                el.append(data['sc']);
                //console.log(data['html']);
                //$.each(data, function(key, value){
                    //console.log(key);
                    //el.append(value);
                //});
            },
            error: function(xhr, textStatus, throwError){
                console.log(xhr);
            }
        });
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
                //el.append("<p>hola</p>");
                //console.log(data);
                $.each(data, function(key, value){
                    //console.log(key);
                    if (key == 'plots'){
                        $.each(value, function(k,v){
                            //console.log(v);
                            get_plot(el, k);
                        });
                    } else {
                        $.each(value, function(k,v){
                            //console.log(v);
                            u = avi_url+"avi/api/res/"+k;
                            el.append('<a href="'+u+'">'+v+"</a>");
                                //.attr("href", "avi/api/res/"+k);
                        });
                    }
                });
                $("#temp_p_"+id).attr("style","display: none");
            },
            error: function(xhr, textStatus, throwError){
                //console.log(xhr);
                $("#temp_p_"+id).attr("style","display: none");
                el.append("<h4>An error occurred while retrieving the execution results</h4>");
            }
        });
    }
}
