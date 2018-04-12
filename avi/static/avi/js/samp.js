
var base_url = window.location.href.toString().replace(new RegExp("[^/]*$"),"");
var origin = new URL(base_url).origin;
//console.log(origin);
//console.log(avi_url);
var url = origin + "avi/api/samp_resource/";
var src_url = "";

var cc = new samp.ClientTracker();
var call_handler = cc.callHandler;

// callers
call_handler["table.load.votable"] =  function(sender_id, message, is_call){
    console.log("callback");
    var params = message["samp.params"];
    var origin_url = params["url"];
    var proxy_url = cc.connection.translateUrl(origin_url);
    var xhr = samp.XmlRpcClient.createXHR();
    //console.log(params);
    console.log(xhr);
    xhr.open("GET", proxy_url);
    console.log(xhr);
    xhr.onload = function(){
        var xml = xhr.responseXML;
        console.log(xml);
    };
    xhr.onerror = function(){
        
    };
    xhr.send(null);
    console.log(proxy_url);
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
