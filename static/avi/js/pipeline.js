function popup_algorithm(url){
    console.log('popup');
    console.log(url);
    $.ajax({
        url: url,
        success: function(data){
            console.log(data);
            $("#dialog-form").load(data).dialog({modal:true});//.dialog('open');
            $("#dialog-form").html(data);
        }
    })
    return false;
}

$(document).ready(function(){
        var forms = document.getElementsByClassName("alg-button");
        for(var i = 0; i < forms.length; i++){
            var row_id = forms.item(i).id.substring(4);
            var el = document.getElementById(row_id);
            el.style.display = 'none';
        }
        $(".alg-button").click(
            function(){
                var row_id = this.id.substring(4);
                var el = document.getElementById(row_id);
                if (el.style.display == 'none'){
                    el.style.display = 'block';
                } else {
                    el.style.display = 'none';
                }
            }
        );
    }
);

$(document).ready(
    function(){
        $(".dropdown-menu li a").click(
            function(){
                var type = $(this).attr("type");
                var id = $(this).attr("id");
                var the_name = $(this).attr("the_name");
                var button_id = "#" +the_name+"_"+ id + "_dropdown";
                var input_id = the_name +"_"+ id;
                console.log(button_id);
                console.log(input_id);
                $(button_id).text($(this).text());
                $(button_id).val($(this).val());
                var element = document.getElementById(input_id);
                if (element === null){
                    var input = $("<input>")
                        .attr("type","hidden")
                        .attr("id", input_id)
                        .attr("name",input_id)
                        .val($(this).text());
                    $("#"+the_name+"_form").append($(input));
                } else {
                    $("#"+input_id).val($(this).text());
                }
            });
});

$(document).ready(
    function(){
        $(".alg-info").click(
            function(){
                //console.log("click");
                var id = $(this).attr("id");
                var res_id = "#div_alg-res_" + id;
                if($(res_id).css('display') == 'none'){
                    $(res_id).show();
                    get_results(id);
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
                    url:"/avi/status",
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
                    url:"/avi/status",
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
                    url:"/avi/status",
                    data:{'sort_by':'name',
                          csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
                    success: function(){
                        window.location.reload();
                    }
                });
            });
    });
