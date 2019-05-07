function source(){
    function myFunction(x) {

        if (x.matches) { // If media query matches
            let sources_buttons = document.getElementsByClassName("filesource-element-buttons");
            let sources_icons = document.getElementsByClassName("fa-file");
            for(let i = 0; i < sources_icons.length; i++){
                sources_icons[i].className = "fas fa-file fa-2x";
            }
            //console.log(sources_buttons);
            //let get_button = sources_buttons[0].getElementsByTagName("button");
            //console.log(get_button);
            let get_button;
            for(let i = 0; i < sources_buttons.length; i++){
                get_button = sources_buttons[i].getElementsByTagName("button");
                for(let j = 0; j < get_button.length; j++){
                    get_button[j].className += " btn-sm";
                }
            }
            
        } else {
            let sources_buttons = document.getElementsByClassName("filesource-element-buttons");
            let sources_icons = document.getElementsByClassName("fa-file");
            for(let i = 0; i < sources_icons.length; i++){
                sources_icons[i].className = "fas fa-file fa-4x";
            }
            //console.log(sources_buttons);
            let get_button;
            for(let i = 0; i < sources_buttons.length; i++){
                get_button = sources_buttons[i].getElementsByTagName("button");
                for(let j = 0; j < get_button.length; j++){
                    if(j === 0){
                        get_button[j].className = "btn btn-danger";
                    }else if(j === 1){
                        get_button[j].className = "btn btn-success";
                    }else if(j === 2){
                        get_button[j].className = "btn btn-warning";
                    }
                }
            }
        }

    }

    var x = window.matchMedia("(max-width: 475px)")
    myFunction(x) // Call listener function at run time
    x.addListener(myFunction);
}

function file(){
    function myFunction(x) {

        if (x.matches) { // If media query matches
            let sources_icons = document.getElementsByClassName("fa-folder");
            for(let i = 0; i < sources_icons.length; i++){
                sources_icons[i].className = "fas fa-folder fa-2x";
            }
            
        } else {
            let sources_icons = document.getElementsByClassName("fa-folder");
            for(let i = 0; i < sources_icons.length; i++){
                sources_icons[i].className = "fas fa-folder fa-4x";
            }
        }

    }

    var x = window.matchMedia("(max-width: 400px)")
    myFunction(x) // Call listener function at run time
    x.addListener(myFunction);
}

function order(value){
    if(value === "name") { 
        $.ajax({
            type:"POST",
            url:avi_url+"avi/resources/filemanager",
            data:{'sort_by':'name',
                    csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
            success: function(){
                window.location.reload();
            }
        });
    }else{
        $.ajax({
            type:"POST",
            url:avi_url+"avi/resources/filemanager",
            data:{'sort_by':'size',
                    csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
            success: function(){
                window.location.reload();
            }
        });
    }
}


/*function data_names(){
    var data_elements = document.getElementsByClassName("data_name");
    var width = [];
    var max_width = 0;
    var winWidth  = 0; 
    var first = true;
    var previous_width = 0; //--- prev window
    var row_width = 0; //--- window
    var row_board = 0;
    var original_text = 0;
    //console.log(data_elements[1].clientWidth);
    for(let i = 0; i < data_elements.length; i++){
        //elemento = data_elements[i]
        //console.log(elemento.offsetWidth);
        width.push((data_elements[i].offsetWidth));
    }
    //console.log(width);
    width.sort();
    //console.log(width);
    max_width = width[width.length - 1];
    original_text = max_width;
    winWidth = $( ".file-element" ).width();
    winWidth = winWidth - 115;
    row_width = $(window).width();
    //console.log(row_width);
    if(row_width > 644){
        if(winWidth < max_width+25){
            for(let i = 0; i < data_elements.length; i++){
                data_elements[i].setAttribute("data-toggle", "tooltip");
                data_elements[i].setAttribute("data-placement", "top");
                data_elements[i].setAttribute("title", data_elements[i].textContent);
                data_elements[i].style.display = 'block';
                data_elements[i].style.width = (winWidth-((max_width+25)-winWidth))+"px";
                data_elements[i].style.overflow = 'hidden';
                data_elements[i].style.whiteSpace = 'nowrap';
                data_elements[i].style.textOverflow = 'ellipsis';
            }
        }
    }else{
        if(winWidth < max_width+25){
            for(let i = 0; i < data_elements.length; i++){
                data_elements[i].setAttribute("data-toggle", "tooltip");
                data_elements[i].setAttribute("data-placement", "top");
                data_elements[i].setAttribute("title", data_elements[i].textContent);
                data_elements[i].style.display = 'block';
                data_elements[i].style.width = (winWidth-(((max_width+25)-winWidth))/4)+"px";
                data_elements[i].style.overflow = 'hidden';
                data_elements[i].style.whiteSpace = 'nowrap';
                data_elements[i].style.textOverflow = 'ellipsis';
            }
        }
    }
    //console.log(max_width);
//console.log(data_elements);
    $(window).resize(function() {
        for(let i = 0; i < data_elements.length; i++){
            //elemento = data_elements[i]
            //console.log(elemento.offsetWidth);
            width.push((data_elements[i].offsetWidth));
        }
        //console.log(width);
        width.sort();
        //console.log(width);
        max_width = width[width.length - 1];
        winWidth = $(window).width();
        winWidth = $( ".file-element" ).width();
        row_width = $(window).width();
        row_board = $( "#row-board" ).width();
        winWidth = winWidth - 115;
        //console.log(winWidth);
        //Sconsole.log(max_width+10);
        if(first){
            if(winWidth < max_width+25){
                for(let i = 0; i < data_elements.length; i++){
                    data_elements[i].setAttribute("data-toggle", "tooltip");
                    data_elements[i].setAttribute("data-placement", "top");
                    data_elements[i].setAttribute("title", data_elements[i].textContent);
                    data_elements[i].style.display = 'block';
                    data_elements[i].style.width = (winWidth-25)+"px";
                    data_elements[i].style.overflow = 'hidden';
                    data_elements[i].style.whiteSpace = 'nowrap';
                    data_elements[i].style.textOverflow = 'ellipsis';
                }
            }
            previous_width = row_width;
            first = false;
        }else if(row_width != 644){//(winWidth < max_width+25)
            //console.log(Math.abs( winWidth - row_board ));
            //console.log(original_text);
            //console.log(winWidth);
            if(Math.abs( winWidth - row_board ) < 161 && previous_width > row_width){
                width_set = (max_width-10) + "px";
                //console.log("restando");
                for(let i = 0; i < data_elements.length; i++){
                    data_elements[i].setAttribute("data-toggle", "tooltip");
                    data_elements[i].setAttribute("data-placement", "top");
                    data_elements[i].setAttribute("title", data_elements[i].textContent);
                    data_elements[i].style.display = 'block';
                    data_elements[i].style.width = (winWidth-25)+"px";
                    data_elements[i].style.overflow = 'hidden';
                    data_elements[i].style.whiteSpace = 'nowrap';
                    data_elements[i].style.textOverflow = 'ellipsis';
                }
                
                //console.log(previous_width);
                //console.log(winWidth);
                previous_width = row_width;
            
            }else if(Math.abs( winWidth - row_board ) === 161 && previous_width > row_width){
                for(let i = 0; i < data_elements.length; i++){
                    data_elements[i].setAttribute("data-toggle", "tooltip");
                    data_elements[i].setAttribute("data-placement", "top");
                    data_elements[i].setAttribute("title", data_elements[i].textContent);
                    data_elements[i].style.display = 'block';
                    data_elements[i].style.width = (winWidth-25)+"px";
                    data_elements[i].style.overflow = 'hidden';
                    data_elements[i].style.whiteSpace = 'nowrap';
                    data_elements[i].style.textOverflow = 'ellipsis';
                }*/
                /*
                display: block; overflow: hidden; whitespace: nowrap: textOverflow: ellipsis;
                */
                //console.log(previous_width);
                //console.log(winWidth);
                /*previous_width = row_width;*/
            /*}else if(original_text > winWidth){
                for(let i = 0; i < data_elements.length; i++){
                    
                    data_elements[i].style.width = (winWidth+10) + "px";
                    //data_elements[i].style.width = (winWidth-25)+"px";
                }
                //console.log("sumando");
                previous_width = row_width;
            }
        }
    });
}*/

