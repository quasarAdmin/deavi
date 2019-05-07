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
var base_url = window.location.href.toString().replace(new RegExp("[^/]*$"), "");
var origin = new URL(base_url).origin;
var url = origin + "avi/api/samp_resource/";
var src_url = "";
var hub_connection = false;

function get_cookie(cname){
    var cname = cname + "=";
    var dcookie = decodeURIComponent(document.cookie);
    var ca = dcookie.split(';');
    for (var i = 0; i < ca.length; i++){
        var c = ca[i];
        while (c.charAt(0) == ' '){
            c = c.substring(1);
        }
        if (c.indexOf(cname) == 0){
            return c.substring(cname.length, c.length);
        }
    }
    return "";
}

var send_data = function(name, xml){
    //escape(xml);
    div = $("#samp-status");
    div.html('');
    div.append($("<p>Uploading file...</p>"));
    $.ajax({
        type: "POST",
        url: avi_url + "avi/ajax/send_samp_data",
        //contentType: 'application/json',
        dataType: 'json',
        data: {
            'name': name,
            'data': escape(xml),
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        success: function(data) { 
            var status = data["samp"]["status"];
            div = $("#samp-status");
            div.html('');
            if (status == "success"){
                div.append($("<p>Success</p>"));
            } else if (status == "error") {
                div.append($("<p>Error</p>"));
            }
        },
        error: function(xhr, textStatus, throwError) {
             console.log(textStatus); 
        },
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    });
}

var cc = new samp.ClientTracker();
var call_handler = cc.callHandler;

// callers
call_handler["samp.app.ping"] = function(sender_id, message, is_call){
    if (is_call){
        return { text: "ping to you, " + cc.getName(sender_id)};
    }
};

call_handler["table.load.votable"] = function(sender_id, message, is_call) {
    var params = message["samp.params"];
    var origin_url = params["url"];
    var proxy_url = cc.connection.translateUrl(origin_url);
    var xhr = samp.XmlRpcClient.createXHR();
    xhr.open("GET", proxy_url);
    xhr.onload = function(){
        var data = xhr.responseText;
        var xml = xhr.responseXML;
        var name = proxy_url.substring(proxy_url.lastIndexOf('/')+1);
        if(xml){
            send_data(name, data);
        }
        /*
        var xhr_send = new XMLHttpRequest();
        xhr_send.open("POST", avi_url+"avi/ajax/send_samp_data",true);
        xhr_send.send({'data':xml,
                      csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value});
                      */
    };
    xhr.onerror = function() {

    };
    xhr.send(null);
};

var meta = {
    "samp.name": "SFM_Handler",
    "samp.description": "Callback handler",
    "samp.icon.url": "http://astrojs.github.io/sampjs/examples/clientIcon.gif"
};

var subs = cc.calculateSubscriptions();
var connection_handler = new samp.Connector("Handler", meta, cc, subs);

connection_handler.onreg = function(){
    if (get_cookie("samp_handler_session") == "true"){
        console.log("cookie");
        this.unregister();
        return;
    }
    hub_connection = true;
    documet.cookie = "samp_handler_session=true";
}

connection_handler.onunreg = function(){
    hub_connection = false;
    document.cookie = "samp_handler_session=false";
}

var send = function(connection) {
    var msg = new samp.Message("table.load.votable", { "url": src_url });
    connection.notifyAll([msg]);
};

var send_fits = function(connection) {
    //var msg = new samp.Message("image.load.fits",{"url": src_url});
    var msg = new samp.Message("table.load.fits", { "url": src_url });
    connection.notifyAll([msg]);
};

var is_samp_enabled = function(is_hub_running)
{
    $(".samp_button").each(function(){
        this.disabled = !is_hub_running;
        if (!is_hub_running) {
            this.title = 'The hub is not running';
        } else {
            this.title = 'Send to SAMP';
        }
    });
}
var connection = new samp.Connector("Sender");
connection.onreg = function(){
    if (get_cookie("samp_sender_session") == "true"){
        this.unregister();
        return;
    }
    documet.cookie = "samp_sender_session=true";
}

connection.onunreg = function(){
    document.cookie = "samp_sender_session=false";
}

onload = function()
{
    connection.unregister();
    connection_handler.unregister(); 
    connection.onHubAvailability(is_samp_enabled, 2000);
    document.getElementById("samp-test").
    appendChild(connection_handler.createRegButtons());
};
onunload = function() {
    connection.unregister();
    connection_handler.unregister();
}

function samp_send(id, name){
    var re = /(?:\.([^.]+))?$/;
    var ext = re.exec(name)[1];
    src_url = url + id;
    if (ext === "vot" || ext === "xml") {
        connection.runWithConnection(send);
        connection.unregister();
    } else {
        connection.runWithConnection(send_fits);
    }
}

$(document).ready(function() {
    url = origin + avi_url + "avi/api/samp_resource/";
});

$(window).on("unload", function(e){
    if (hub_connection && !confirm('You are currently connected to a SAMP Hub. If you continue you will be disconnected. Are you sure?')){
        e.preventDefault();
    } else {
        connection.unregister();
        connection_handler.unregister();
    }
});

$(document).ready(function() {
    els = $(".samp_confirmation");
    var confirmation_function = function(e) {
        if (hub_connection){
            if (!confirm('You are currently connected to a SAMP Hub. If you continue you will be disconnected. Are you sure?')) {
                e.preventDefault();
            } else {
                connection_handler.unregister();
            }
        }
    };

    for (var i = 0; i < els.length; i++){
        els[i].addEventListener('click', confirmation_function, false);
    }
});
