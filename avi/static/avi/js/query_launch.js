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
var gaia_array = [];
var hsa_array = [];
var res_array = [];
var user_array = [];
var query_files;
var create_form = function(el, id, data, files) {
  eval('var algorithm='+files);
  var cont = 1;
  for (var key in algorithm.files){
  }
  console.log(el);
  console.log(id);
  console.log(data);
  console.log(files);
  var view_name = data['view_name'];
  var form = $('<form></form>', {
      method: 'post',
      id: 'alg_info_form'
  });
  var token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
  document.getElementById("div_alg_info").className = "text-center col-sm-12 mt-3";
  document.getElementById("div_alg_info").setAttribute("style", "width:100%");
  form.append('<input name="csrfmiddlewaretoken" value="' +
      token + '" type="hidden">');
  form.append('<hr/>');
  form.append('<h3>' + view_name + '</h3>');
  $.each(data['input'], function(k, v) {
      var div2 = $('<div class="row"></div>');
      var div = $('<div class="col-sm-12"></div>');
      var inp_id = id + "_" + v['name'];
      if (v['type'] == "bool") {
          div.append("<label>" + v['view_name'] + "</label>");
          div.append('<input name="' + id + "_" + v['name'] +
              '" type="checkbox" value="true">');
          form.append(div);
      } else if (v['type'] == "string" ||
          v['type'] == "float" ||
          v['type'] == "integer") {
          var adiv = $('<div class="row" style="width:100%; margin-top:5px"></div>');
          adiv.append('<label class = "col-sm-5 col-form-label" style="padding: 5px 0px 0px 0px">' + v['view_name'] + "</label>");
          var ainput = $('<input name="' + id + "_" + v['name'] +
              '" type="text" value="" class="col-sm-7 form-control">');
          adiv.append(ainput);
          div.append(adiv);
          div2.append(div);
          form.append(div2);
      } else if (v['type'] == "gaia_table") {
          var adiv = $('<div class="autocomplete row" style="width:100%; margin-top:5px"></div>');
          if(algorithm.mission === 'gaia'){


            var swt= $('<div class="custom-control custom-switch"></div>');
            swt.append('<input type="checkbox" class="custom-control-input switch_1" id="customSwitch'+ cont +'" for_select="'+ id + "__" + v['name'] +'" for_no_select="' + inp_id +'" onchange="changeForm(this.value, '+ cont +')" value="off">');
            var swtinput = $('<label class="custom-control-label" for="customSwitch'+ cont +'">Use query files</label>');
            swt.append(swtinput);



            /*var adiv = $('<div class="autocomplete" style="width:100%; margin-top:5px"></div>');
            var aux = "";
            aux = '<div class="form-group row" style="width: 100%"><label class="col-sm-5 col-form-label" for="from_table">Gaia</label>'+
            '<div class="col-sm-7" style="padding: 0px"><select class="form-control" id="from_table" name="' + id + "_" + v['name'] +
            '" id="' + inp_id +'"><option selected>Choose Gaia Table</option>';
            for (var key in algorithm.files){
                aux +='<option value="'+ algorithm.files[key] +'">'+ algorithm.files[key] +'</option>';
            }
            {input: {input_1: {view_name: "Gaia", type: "gaia_table", name: "gaia_file"}, input_2: {view_name: "number of stars", type: "float", name: "n_stars"}, input_3: {view_name: "HSA", type: "hsa_table", name: "hsa_file"}
            }, view_name: "Graph 2Dim", name: "simple_algorithm"}
            

            aux +='</select></div></div>';
            adiv.append(aux);*/
          }else{
              /* <div class="custom-control custom-switch">
          <input type="checkbox" class="custom-control-input switch_1" id="customSwitch1" onchange="test(this.value)" value="off">
          <label class="custom-control-label" for="customSwitch1">Use query - X table</label>
        </div>
        */  


            /*var adiv = $('<div id="testt" class="autocomplete row" style="width:100%; margin-top:5px"></div>');
            adiv.append('<label class = "col-sm-5 col-form-label" for="' + inp_id +'">' + v['view_name'] + "</label>");
            var ainput = $('<input name="' + id + "_" + v['name'] +
                '" id="' + inp_id +
                '" class="gaia_table col-sm-7 form-control"' +
                ' type="text" placeholder="Gaia Table">');*/
          }
          var adiv = $('<div class="autocomplete row" style="width:100%; margin-top:5px"></div>');
            adiv.append('<label class = "col-sm-5 col-form-label" for="' + inp_id +'">' + v['view_name'] + "</label>");
            var ainput = $('<input name="' + id + "_" + v['name'] +
                '" id="' + inp_id +
                '" class="gaia_table col-sm-7 form-control"' +
                ' type="text" placeholder="Gaia Table">');
          adiv.append(ainput);
          div.append(swt);
          div.append(adiv);
          div2.append(div);
          form.append(div2);
      } else if (v['type'] == "hsa_table") {
          if(algorithm.mission === 'hsa'){

            var swt= $('<div class="custom-control custom-switch"></div>');
            swt.append('<input type="checkbox" class="custom-control-input switch_1" id="customSwitch'+ cont +'" for_select="'+ id + "__" + v['name'] +'" for_no_select="' + inp_id +'" onchange="changeForm(this.value, '+ cont +')" value="off">');
            var swtinput = $('<label class="custom-control-label" for="customSwitch'+ cont +'">Use query files</label>');
            swt.append(swtinput);

            /*var adiv = $('<div class="autocomplete" style="width:100%; margin-top:5px"></div>');
            var aux = "";
            aux = '<div id="' + id + "__" + v['name']+'" class="form-group row mt-3" style="width: 100%"><label class="col-sm-5 col-form-label" for="from_table">Hsa</label>'+
            '<div class="col-sm-7" style="padding: 0px"><select class="form-control" id="from_table" name="' + id + "_" + v['name'] +
            '" id="' + inp_id +'"><option selected>Choose HSA Table</option>';
            for (var key in algorithm.files){
                aux +='<option value="'+ algorithm.files[key] +'">'+ algorithm.files[key] +'</option>';
            }
            aux +='</select></div></div>';
            adiv.append(aux);*/
          }else{
            /*var adiv = $('<div class="autocomplete row mb-3" style="width:100%; margin-top:5px"></div>');
            adiv.append('<label class = "col-sm-5 col-form-label">' + v['view_name'] + "</label>");
            adiv.append('<input name="' + id + "_" + v['name'] +
                '" id="' + inp_id +
                '" class="hsa_table col-sm-7 form-control"' +
                ' type="text" placeholder="HSA Table">');*/
          }
          var adiv = $('<div class="autocomplete row" style="width:100%; margin-top:5px"></div>');
            adiv.append('<label class = "col-sm-5 col-form-label">' + v['view_name'] + "</label>");
            adiv.append('<input name="' + id + "_" + v['name'] +
                '" id="' + inp_id +
                '" class="hsa_table col-sm-7 form-control"' +
                ' type="text" placeholder="HSA Table">');
          div.append(swt);
          div.append(adiv);
          div2.append(div);
          form.append(div2);
      } else if (v['type'] == "results_data") {
          var adiv = $('<div class="autocomplete" style="width:300px;"></div>');
          adiv.append("<label>" + v['view_name'] + "</label>");
          adiv.append('<input name="' + id + "_" + v['name'] +
              '" id="' + inp_id +
              '" class="results_data"' +
              ' type="text" placeholder="Results Data">');
          div.append(adiv);
          form.append(div);
      } else if (v['type'] == "user_data") {
          var adiv = $('<div class="autocomplete" style="width:300px;"></div>');
          adiv.append("<label>" + v['view_name'] + "</label>");
          adiv.append('<input name="' + id + "_" + v['name'] +
              '" id="' + inp_id +
              '" class="user_data"' +
              ' type="text" placeholder="User Data">');
          div.append(adiv);
          form.append(div);
      }
      cont++;
  });
  form.append('<button name="algorithm_id" class="btn btn-outline-primary" style="margin-top:5px; margin-bottom: 5px" type="submit" value="' +
      id + '">Run</button>');
  el.append(form);
}

var get_algorithm_info = function(el, id, files) {
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
          create_form(el, id, data['algorithm'], files);
      },
      error: function(xhr, textStatus, throwError) {
          console.log(xhr);
      },
      headers: {
          'X-Requested-With': 'XMLHttpRequest'
      }
  });
}

/*function launch(){
  $(".alg-button").click(function() {
      var id = $(this).attr("id");
      var files = $(this).attr("params");
      var info_id = "div_alg_info";
      var node = document.getElementById(info_id);
      while (node.firstChild) {
          node.removeChild(node.firstChild);
      }
      get_algorithm_info($("#" + info_id), id, files);
  });
};*/

function launch(element){
    var elmnt = document.getElementById(element);
    var id = $(elmnt).attr("id");
    var files = $(elmnt).attr("params");
    query_files = $(elmnt).attr("params");
    var info_id = "div_alg_info";
    var node = document.getElementById(info_id);
    while (node.firstChild) {
        node.removeChild(node.firstChild);
    }
    get_algorithm_info($("#" + info_id), id, files);
  };

function changeForm(val, num){
    if(val === "off"){
        if(document.getElementById('customSwitch'+ num ).getAttribute('for_select').includes("gaia")){
            var table_name = "gaia";
            var name_view = "Gaia";
        }else if(document.getElementById('customSwitch'+ num ).getAttribute('for_select').includes("hsa")){
            var table_name = "hsa";
            var name_view = "HSA";
        }
        document.getElementById('customSwitch'+ num ).setAttribute('value', 'on');
        var parent = $('#'+document.getElementById('customSwitch'+ num ).getAttribute('for_no_select')).parents()[0];
        $('#'+document.getElementById('customSwitch'+ num ).getAttribute('for_no_select')).prev()[0].remove();
        document.getElementById(document.getElementById('customSwitch'+ num ).getAttribute('for_no_select')).remove();


        eval('var algorithm='+query_files);
        var aux = "";
        aux = '<div id="'+ document.getElementById('customSwitch'+ num ).getAttribute('for_select') +'" class="form-group row" style="width: 100%; margin-bottom: 0"><label class="col-sm-5 col-form-label" for="from_table">' + name_view + '</label>'+
        '<div class="col-sm-7" style="padding: 0px"><select class="form-control" id="from_table" name="'+ document.getElementById('customSwitch'+ num ).getAttribute('for_no_select') +'" id="'+ document.getElementById('customSwitch'+ num ).getAttribute('for_no_select') +'"><option selected>Choose ' + name_view + ' Table</option>';
            for (var key in algorithm.files){
                aux +='<option value="'+ algorithm.files[key] +'">'+ algorithm.files[key] +'</option>';
            }
        
        aux +='</select></div></div>';
        parent.innerHTML= aux;
        parent.className = "autocomplete";

    }else{
        if(document.getElementById('customSwitch'+ num ).getAttribute('for_select').includes("gaia")){
            var table_name = "gaia";
            var name_view = "Gaia";
        }else if(document.getElementById('customSwitch'+ num ).getAttribute('for_select').includes("hsa")){
            var table_name = "hsa";
            var name_view = "HSA";
        }
        document.getElementById('customSwitch'+ num ).setAttribute('value', 'off');
        var parent = $('#'+document.getElementById('customSwitch'+ num ).getAttribute('for_select')).parents()[0];
        document.getElementById(document.getElementById('customSwitch'+ num ).getAttribute('for_select')).remove();

        var adiv = '<label class = "col-sm-5 col-form-label">' + name_view + ' </label><input name="' + document.getElementById('customSwitch'+ num ).getAttribute('for_no_select') +
        '" id="' + document.getElementById('customSwitch'+ num ).getAttribute('for_no_select') +
        '" class="'+ table_name +'_table col-sm-7 form-control"' +
        ' type="text" placeholder="' + name_view + ' Table">';
        parent.innerHTML= adiv;
        parent.className = "autocomplete row";
    }
}

function autocomp(){
  var info_id = "#div_alg_info";
  var node = $(info_id);
  node.on("DOMSubtreeModified",
      function() {
          $(".gaia_table").autocomplete({ source: gaia_array });
          $(".hsa_table").autocomplete({ source: hsa_array });
          $(".results_data").autocomplete({ source: res_array });
          $(".user_data").autocomplete({ source: user_array });
      }
  );
};

function autocomplete(inp, arr) {
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

