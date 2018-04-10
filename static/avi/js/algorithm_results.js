var get_plot = function(el, id){
    console.log(id);
    $.ajax({
            type:"POST",
            url:"/avi/ajax/get_plot",
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
        el.append("<p>Loading results for the job "+id+"...</p>");
        $.ajax({
            type:"POST",
            url:"/avi/ajax/get_results",
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
                            u = "/avi/api/res/"+k;
                            el.append('<a href="'+u+'">'+v+"</a>")
                                //.attr("href", "avi/api/res/"+k);
                        });
                    }
                });
            },
            error: function(xhr, textStatus, throwError){
                console.log(xhr);
            }
        });
    }
}
