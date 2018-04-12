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
