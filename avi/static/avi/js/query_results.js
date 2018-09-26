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
var get_qinfo = function(id, mission){
    var el = $("#"+mission+"_"+id+"_query-container");
    if (el.attr("loaded") == "false"){
        el.attr("loaded", "true");
        el.append('<p id="temp_p_'+id+'">Loading results for the query '+id+"...</p>");
        $.ajax({
            type:"POST",
            url:avi_url+"avi/ajax/get_query_info",
            dataType:'json',
            data:{'id': id,
                  'mission': mission,
                  csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
            success: function(data){
                el.append('<h4>Query Parameters</h4>');
                el.append('RA: '+ data['ra']+'</br>');
                el.append('DEC: '+ data['dec']+'</br>');
                el.append('Radius: '+data['radius']+'</br>');
                if(data['files']){
                    el.append('<h4>Files</h4>');
                    $.each(data['files'], function(key, value){
                        console.log(key+" "+value);
                        el.append('<div id="file_btn_group_'+key+'">');
                        var e = $("#file_btn_group_"+key);
                        //e.append('<form class="col-inline-button btn-group"  action="'+ avi_url +'avi/api/resource/'+key+'"><div class="col-inline-button"><button class="btn btn-success"type="submit" value="download"title="Download '+value+'"><span class="glyphicon glyphicon-cloud-download"></span></button></div></form>');
                        //e.append('<form class="col-inline-button">'+
                          //       '<div class="col-inline-button">'+
                            //     '<button '+
                              //   'type="button" '+
                                // 'class="btn btn-danger" '+
                  //data-toggle="modal"
                  //data-target="#call_delete_file_{{ file|cut:"." }}" 
                  //id="pre_delete_file_button_{{ file|cut:" " }}" 
                  //name="{{files_list|getkey:file}}"
                  //title="Delete {{ data.0 }}" 
                  //value="pre_delete_file_{{ file|cut:" " }}"
                  //data-whatever="@fat">
                  //<span class="glyphicon glyphicon-trash"></span>
                //</button>
                //<!-- End Delete file button -->
              //</div>
              //<!-- Start Delete file button pop up -->
              //<div class="modal fade" tabindex="-1" role="dialog"
               // aria-labelledby="confirmation_file_modal" aria-hidden="true"
                //id="call_delete_file_{{ file|cut:"." }}">
                //<div class="modal-dialog">
                  //<div class="modal-content">
                    //<div class="modal-header">
                      //<button type="button"
                        //class="close" 
                        //data-dismiss="modal" 
                        //aria-label="Close">
                          //<span aria-hidden="true">&times;</span>
                      //</button>
                      //<div class="alert alert-warning alert-white rounded">
                        //<h4 class="modal-title"
                          //id="modal_confirmation_file_pop_up_{{files_list|getkey:file}}">
                          //<img src="https://vignette.wikia.nocookie.net/lego/images/c/cd/Warning_sign.png/revision/latest/scale-to-width-down/1000?cb=20110705195119" width="42" height="42">
                          //Are you sure you want to permanently delete 
                          //<strong>"{{ data.0 }}" </strong>?
                       // </h4>
                      //</div>
                      //<div class="modal-footer">
                        //<button
                          //type="submit"
                          //formmethod="POST" 
                          //type="button"
                          //name="delete_file" 
                          //class="btn btn-default"
                          //value="{{ data.0 }}"
                          //title="Click to delete the file" 
                          //id="modal_btn__delete_yes_file">Yes
                        //</button>
                        //<button 
                          //type="button"
                          //data-dismiss="modal" 
                          //class="btn btn-primary"
                          //title="Click to close" 
                          //id="modal_btn_no_file">No
                        //</button>     
                      //</div>     
                    //</div>
                  //</div>
                //</div>
                //<div class="alert" role="alert" id="result"></div>
              //</div>                 
           // </form>');
                                  
                        if(mission=="gaia"){
                            u = avi_url+"avi/api/res/"+key;
                        }else{
                            u = "#";
                        }
                        e.append('    <a class="btn-group" href="'+u+'">'+value+"</a></br>");
                        //el.append('</div>');
                    });
                }
                $("#temp_p_"+id).attr("style","display: none");
            },
            error: function(xhr, textStatus, throwError){
                $("#temp_p_"+id).attr("style","display: none");
                el.append("<h4>An error occurred while retrieving the query information</h4>");
                console.log(xhr);
            }
        });
    }
}
