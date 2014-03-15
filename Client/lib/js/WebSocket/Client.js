function WebSocket_Client(config) 
{
  if (typeof config === 'object') {
    if (config.url) {
      this._url = config.url;
    }
    if (config.port) { 
      this._port = config.port;
    }
    if (config.roomId) {
      this._roomId = config.roomId;
    }
  }
}

WebSocket_Client.init = function(config) 
{
  if (typeof WebSocket === "undefined") {
    alert("Your browser doesnt support WebSockets!\nGet a new Browser!");
    return null;
  }
  
  return new WebSocket_Client(config);
};

WebSocket_Client.prototype = {
  _url    : "localhost",
  _port   : 4423,
  _roomId : "/",
  _socket : null,
  _messages : [],
  
  setUrl : function(url)
  {
    this._url = url;
    
    return this;
  },
  
  setPort : function(port)
  {
    this._port = port;
    
    return this;
  },
  
  setRoomId : function()
  {
    this._roomId = roomId;
    
    return this;
  },
  
  connect : function()
  {
    this._socket = new WebSocket("ws://" + window.location.hostname + ":4423/stuff");
    var self = this;
    
    this._socket.onopen = function(e) 
    {
      console.log('socket open');
      self._socket.send('{"cmd":"System|login","args":{"name":"' + Math.random() + '"}}');
    }
    
    this._socket.onclose = function(e) 
    {
      console.log('socket closed');
    }
    
    this._socket.onmessage = function(e) 
    {
      if (self._messages.unshift(JSON.parse(e.data)) > 10) {
        self._messages.pop();
      } 
      
      self._displayMessages();
    }
    
    this._socket.onmerror = function(e) 
    {
      console.log("error:")
      console.log(e);
    }
  },
  
  send : function(message) 
  {
    this._socket.send(JSON.stringify({msg:message}));
  },
  
  sendCommand : function(cmd, args)
  {
    this._socket.send(JSON.stringify({cmd:cmd,args:args}));
  },
  
  _displayMessages : function()
  {
    var st = '';
    
    for (var i in this._messages) {
      var m = this._messages[i]
      st += '<div class="' + (m.usr === "__system__" ? 'system_' : '') + 'message">';
      
      if (m.usr != "__system__") {
        st += '<span class="message_name">' + m.usr + '</span>';
      }
      var d = new Date(m.tme)
      st += '<span class="message_date">' + tdt(d.getHours()) + ':' + tdt(d.getMinutes()) + ':' + tdt(d.getSeconds()) + '</span>';
      
      st += '<span class="message_text">' + m.msg + '</span>\
        </div>';
    }
    
    $('div#messages').html(st);
  }
};

function tdt(time)
{
  if (time > 10) 
    return time;
  return "0" + time;
}