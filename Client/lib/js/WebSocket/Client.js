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
      self._socket.send('{"cmd":"login","name":"' + Math.random() + '"}');
    }
    
    this._socket.onclose = function(e) 
    {
      console.log('socket closed');
    }
    
    this._socket.onmessage = function(e) 
    {
      console.log(e);
    }
    
    this._socket.onmerror = function(e) 
    {
      console.log(e);
    }
  },
  
  send : function(message) 
  {
    this._socket.send(message);
  }
};