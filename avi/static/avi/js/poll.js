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
$(document).ready(
    function do_poll()
    {
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
