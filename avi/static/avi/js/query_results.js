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
var get_qinfo = function(id, mission) {
    console.log("id: " + id + ", mission: " + mission);
    var el = $("#" + mission + "_" + id + "_query-container");
    var content = "";
    var instrument = false;

    if (el.attr("loaded") == "false") {
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
                console.log(data);
                content = '<div class="row">' + '<div class="col-sm-5 offset-sm-1 mt-3 query_parameters"><div class="card border-primary"><div class="card-body">' + '<h4 class="text-center">Query Parameters</h4>';
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



                //el.append('<div class="row">'+'<div class="col-sm-6">'+'<h4>Query Parameters</h4>'+'RA: '+ data['ra']+'</br>'+'DEC: '+ data['dec']+'</br>'+'Radius: '+data['radius']+'</br>');

                //el.append('<h4>Query Parameters</h4>');
                //el.append('RA: '+ data['ra']+'</br>');
                //el.append('DEC: '+ data['dec']+'</br>');
                //el.append('Radius: '+data['radius']+'</br>');
                //console.log(data);
                //if(data['files']){
                content += '<div class="col-sm-5 mt-3 mb-3 query_files"><div class="card border-primary"><div class="card-body"><h4 class="text-center">Files</h4>';
                if (data[data.length - 1][0] === 'files') {

                    //el.append('<h4>Files</h4>');
                    $.each(data[data.length - 1][1], function(key, value) {
                        //console.log(key+" "+value);
                        content += '<div id="file_btn_group_' + key + '">';
                        //el.append('<div id="file_btn_group_'+key+'">');
                        var e = $("#file_btn_group_" + key);
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

                        if (mission == "gaia") {
                            u = avi_url + "avi/api/res/" + key;
                        } else {
                            u = "#";
                        }
                        //e.append('    <a class="btn-group" href="'+u+'">'+value+"</a></br>");
                        content += '<a class="btn-group a-link" target="_blank" href="' + u + '" style="display: block; width: 100%; overflow: hidden;white-space: nowrap;text-overflow: ellipsis;" data-toggle="tooltip" data-pacement="top" title="' + value + '">' + value + "</a></br>";
                        content += '</div>';
                        //el.append('</div>');
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






//------------------------------------------