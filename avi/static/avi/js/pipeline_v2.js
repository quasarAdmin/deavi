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
along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
*/
var text_array = ["hola", "Hola 2", "asdf", "qwerty"];
var gaia_array = [];
var hsa_array = [];
var res_array = [];
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
var create_form = function(el, id, data){
    //console.log(data);
    var view_name = data['view_name'];
    var form = $('<form></form>',{method: 'post',
                                  id:'alg_info_form'});//,autocomplete: 'off'});
    var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    console.log(token);
    form.append('<input name="csrfmiddlewaretoken" value="'+
                token+'" type="hidden">');
    form.append('<h3>'+view_name+'</h3>');
    $.each(data['input'], function(k,v){
        var div = $('<div class="row"></div>');
        var inp_id = id+"_"+v['name'];
        //console.log(inp_id);
        if (v['type'] == "bool"){
            div.append("<label>"+v['view_name']+"</label>");
            div.append('<input name="'+id+"_"+v['name']+
                       '" type="checkbox" value="true">');
            form.append(div);
        }else if (v['type'] == "string" 
                  || v['type'] == "float" 
                  || v['type'] == "integer"){
            div.append("<label>"+v['view_name']+"</label>");
            div.append('<input name="'+id+"_"+v['name']+
                       '" type="text" value="">');
            form.append(div);
        }else if (v['type'] == "gaia_table"){
            var adiv = $('<div class="autocomplete" style="width:300px;"></div>');
            adiv.append("<label>"+v['view_name']+"</label>");
            var ainput = $('<input name="'+id+"_"+v['name']+
                           '" id="'+inp_id+
                           '" class="gaia_table"'+
                           ' type="text" placeholder="Gaia Table">'); 
            //ainput.autocomplete();
            //ainput.autocomplete({source:text_array});
            adiv.append(ainput);
            div.append(adiv);
            form.append(div);
            //get_files_list("gaia");
            //autocomplete(ainput[0], text_array);
        }else if (v['type'] == "hsa_table"){
            var adiv = $('<div class="autocomplete" style="width:300px;"></div>');
            adiv.append("<label>"+v['view_name']+"</label>");
            adiv.append('<input name="'+id+"_"+v['name']+
                        '" id="'+inp_id+
                        '" class="hsa_table"'+
                        ' type="text" placeholder="HSA Table">');
            div.append(adiv);
            form.append(div);
            //get_files_list("hsa");
            //document.getElementById(inp_id)
            //autocomplete(adiv[0], text_array);
        }
    });
//form.append('
    form.append('<button name="algorithm_id" type="submit" value="'+
                id+'">Run</button>');
    el.append(form);
}

var get_algorithm_info = function(el, id){//, name){
    $.ajax({
        type:"POST",
        url:avi_url+"avi/ajax/get_alg_info",
        dataType:'json',
        data:{'id': id,
              //'name': name,
              csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
        success: function(data){
            //console.log(data);
            if ('hsa' in data){
                hsa_array = data['hsa'];
            }
            if ('gaia' in data) {
                gaia_array = data['gaia'];
            }
            create_form(el, id, data['algorithm']);
        },
        error: function(xhr, textStatus, throwError){
            console.log(xhr);
        },
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    });
}

$(document).ready(function(){
    $(".alg-button").click(function(){
        var id = $(this).attr("id");
        //var name = $(this).attr("name");
        var info_id = "div_alg_info";//_" + id;
        var node = document.getElementById(info_id);
        while (node.firstChild){
            node.removeChild(node.firstChild);
        }
        get_algorithm_info($("#"+info_id), id);//, name);
    });
});

$(document).ready(function(){
    var info_id = "#div_alg_info";
    var node = $(info_id);
    node.on("DOMSubtreeModified",
        function(){
            //console.log("onChange");
            //$("#alg_info_form").attr("autocomplete","off");
            $(".gaia_table").autocomplete({source:gaia_array});
            $(".hsa_table").autocomplete({source:hsa_array});
            $(".res_table").autocomplete({source:res_array});
        }
    );
});

function autocomplete(inp, arr){
     /*the autocomplete function takes two arguments,
       the text field element and an array of possible autocompleted values:*/
    console.log(inp);
    console.log(arr);
    var currentFocus;
    /*execute a function when someone writes in the text field:*/
    inp.addEventListener("input", function(e) {
        var a, b, i, val = this.value;
        /*close any already open lists of autocompleted values*/
        closeAllLists();
        if (!val) { return false;}
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
    document.addEventListener("click", function (e) {
        closeAllLists(e.target);
    });
}
