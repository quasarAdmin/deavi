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
var base_url = window.location.href.toString().replace(new RegExp("[^/]*$"),"");
var origin = new URL(base_url).origin;
//console.log(origin);
//console.log(avi_url);
var url = origin + "avi/api/samp_resource/";
var src_url = "";

var cc = new samp.ClientTracker();
var call_handler = cc.callHandler;

var send_data = function(name, xml){
    //console.log(xml);
    //escape(xml);
    $.ajax({
        type:"POST",
        url:avi_url+"avi/ajax/send_samp_data",
        //contentType: 'application/json',
        dataType:'json',
        data:{'name':name, 'data':escape(xml),
              csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
        success:function(data){console.log("ok");},
        error:function(xhr, textStatus, throwError){console.log(textStatus);},
        headers:{'X-Requested-With': 'XMLHttpRequest'}
    });
}

// callers
call_handler["table.load.votable"] =  function(sender_id, message, is_call){
    //console.log("callback");
    //console.log(avi_url);
    var params = message["samp.params"];
    var origin_url = params["url"];
    var proxy_url = cc.connection.translateUrl(origin_url);
    var xhr = samp.XmlRpcClient.createXHR();
    //console.log(params);
    //console.log(xhr);
    xhr.open("GET", proxy_url);
    //console.log(xhr);
    xhr.onload = function(){
        var data = xhr.responseText;
        var xml = xhr.responseXML;
        var name = proxy_url.substring(proxy_url.lastIndexOf('/')+1);
        //console.log(name);
        //console.log(xml);
        //console.log(avi_url);
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
    xhr.onerror = function(){
        
    };
    xhr.send(null);
    //console.log(proxy_url);
};

var meta = {"samp.name": "Handler",
            "samp.description": "Callback handler",
            "samp.icon.url": 
            "http://astrojs.github.io/sampjs/examples/clientIcon.gif"};

var subs = cc.calculateSubscriptions();
var connection_handler = new samp.Connector("Handler", meta, cc, subs);

connection_handler.onreg = function(){
    
}

var send = function(connection)
{
    var msg = new samp.Message("table.load.votable",{"url": src_url});
    connection.notifyAll([msg]);
};

var send_fits = function(connection)
{
    //var msg = new samp.Message("image.load.fits",{"url": src_url});
    var msg = new samp.Message("table.load.fits",{"url": src_url});
    connection.notifyAll([msg]);
};

var is_samp_enabled = function(is_hub_running)
{
    $(".samp_button").each(function(){
        //console.log("is_samp_enabled");
        this.disabled = !is_hub_running;
        if (!is_hub_running){
            this.title = 'The hub is not running';
        }else{
            this.title = 'Send to SAMP';
        }
    });
}
var connection = new samp.Connector("Sender");
onload = function()
{
    //console.log("onload");
    connection.onHubAvailability(is_samp_enabled, 2000);
    document.getElementById("samp-test").
        appendChild(connection_handler.createRegButtons());
};
onunload = function()
{
    connection.unregister();
    connection_handler.unregister();
}

//console.log(connection);

function samp_send(id, name)
{
    var re = /(?:\.([^.]+))?$/;
    var ext = re.exec(name)[1];
    src_url = url + id;
    if (ext === "vot" || ext === "xml"){
        connection.runWithConnection(send);
    }else{
        connection.runWithConnection(send_fits);
    }
}

$(document).ready(function(){
    url = origin + avi_url + "avi/api/samp_resource/";
    console.log(url);
});
