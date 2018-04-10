

// URL of table to send.
var baseUrl = window.location.href.toString().replace(new RegExp("[^/]*$"), "");
//var tableUrl = baseUrl + "file_to_send ";
var tableUrl = "http://andromeda.star.bris.ac.uk/data/messier.xml"
		console.log(tableUrl);

// Broadcasts a table given a hub connection.
var send = function(connection) {
    var msg = new samp.Message("table.load.votable", {"url": tableUrl});
    connection.notifyAll([msg]);
};
var connector = new samp.Connector("Sender");

// Adjusts page content depending on whether the hub exists or not.
var configureSampEnabled = function(isHubRunning) {
    document.getElementById("sendButt").disabled = !isHubRunning;
    document.getElementById('sendButt').title = 'The hub is not running';
};

// Arrange for document to be adjusted for presence of hub every 2 sec.
var connector = new samp.Connector("Sender");
onload = function() {
    connector.onHubAvailability(configureSampEnabled, 2000);
};
onunload = function() {
    connector.unregister();
};




// Checkbox function and counter
/*
$(document).ready(function() {
	//select all checkboxes
		$("#select_all").change(function(){  //"select all" change
			 //change all ".checkbox" checked status
		    $(".checkbox").prop('checked', $(this).prop("checked"));
		    if ($('.checkbox:checked').length == 0){
		        count = 0;
		    }
		    else {
		    	count = $('.checkbox').length;
		    }
		    $("#selected_items").html(count);
		});

		//".checkbox" change
		$('.checkbox').change(function(){
		    //uncheck "select all", if one of the listed checkbox item is 
			// unchecked
		    if(false == $(this).prop("checked")){ //if this item is unchecked
		    	//change "select all" checked status to false
		        $("#select_all").prop('checked', false); 
		       count = $('.checkbox:checked').length;
		    }
		    //check "select all" if all checkbox items are checked
		    if ($('.checkbox:checked').length == $('.checkbox').length ){
		        $("#select_all").prop('checked', true);
		        count = $('.checkbox:checked').length;
		    }

		    if ($('.checkbox:checked').length != $('.checkbox').length ){
		        count = $('.checkbox:checked').length;
		    }
		    
		    $("#selected_items").html(count);
		});
	    

	});

// Set unchecked checkboxes at startup
$(document).ready(function()
		{
			var checkboxes = document.getElementsByTagName('input');	
			for (var i=0; i<checkboxes.length; i++)  {
				if (checkboxes[i].type == 'checkbox')   {
					checkboxes[i].checked = false;
				}
			}
		});

// Delete button function
$(function(){
	
    $('[type=checkbox]').change(function ()
    {
    	var checkedChbx = $('[type=checkbox]:checked');

        if ( $("#checkAll").is(':checked') || checkedChbx.length > 0)
        {
            $('#delete_button_check').show();
        }
        else
        {
        	$('#delete_button_check').hide();
        }
     });
});

// Alert delete file and get array of values checkboxes
$(function(){
	$('#delete_button_check').click(function() {
		if (confirm("Are you sure you want to delete this?")) {
	        // your deletion code
			var values_checkboxes = $('input[type=checkbox]:checked')
				.map(function(_, el) {
				return $(el).val();
			}).get();
			//console.log(values_checkboxes); 
	    }
	})
});
*/
//----------------------------------------------------
/*
$(document).ready(function() {
	$('#call_create_directory_button').on('hide.bs.modal', function (e) {
		})	
		$('#close_create_directory').click(function() {
			//alert("The 'Close' button was pressed.");
			console.log($("#message_text_directory").val())
		});
		
		$('#create_directory_pop_up').click(function() { 
		  var value_new_directory = $("#message_text_directory").val()
		  console.log(value_new_directory)
		  if (value_new_directory === '') { 
			  alert("You must introduce a name directory");
			  console.log(value_new_directory)
			  // fix close dialog without name directory
		  }
		  else {
			  console.log($("#message_text_directory").val())
			 // alert("Create button");
		  }/*
		  
		  //$('#call_create_directory_button').modal('hide');
		  $('#message_text_directory').val('');	*/	  
		//})	
//});*/

