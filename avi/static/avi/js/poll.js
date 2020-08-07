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
$(document).ready(
    function do_poll()
    {
        return;
        console.log("polling");
        /*$.post('avi/query_status.html', function(data){
          console.log("polling...");
          setTimeout(do_poll, 5000);
          });*/
        $.ajax({
            type:"POST",
            url:avi_url+"avi/queries/status",
            data:{'poll':'yes',
                  csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
            success: function(){
                setTimeout(do_poll, 5000);
                console.log("refresh");
                //window.location.reload();
            }
        });
    });

$(document).ready(
    function(){
        $(".query-info").click(
            function(){
                //console.log("click");
                var id = $(this).attr("qid");
                var mission = $(this).attr("mission");
                var res_id = "#div_qs-res_" +mission+"_"+id;
                if($(res_id).css('display') == 'none'){
                    $(res_id).show();
                    get_qinfo(id, mission);
                }else{
                    $(res_id).hide();
                }
            });
    });

$(document).ready(
    function(){
        $(".sort-by-date").click(
            function(){
                $.ajax({
                    type:"POST",
                    url:avi_url+"avi/queries/status",
                    data:{'sort_by':'date',
                          csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                    success: function(){
                        window.location.reload();
                    }
                });
            });
    });
$(document).ready(
    function(){
        $(".sort-by-status").click(
            function(){
                $.ajax({
                    type:"POST",
                    url:avi_url+"avi/queries/status",
                    data:{'sort_by':'status',
                          csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                    success: function(){
                        window.location.reload();
                    }
                });
            });
    });

$(document).ready(
    function(){
        $(".sort-by-name").click(
            function(){
                $.ajax({
                    type:"POST",
                    url:avi_url+"avi/queries/status",
                    data:{'sort_by':'name',
                          csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                    success: function(){
                        window.location.reload();
                    }
                });
            });
    });
