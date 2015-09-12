(function () {

  "use strict"

  window.socket_handler = {
    socket: null,
    start: function () {
      var url = "ws://" + location.host + "/socket";
      socket_handler.socket = new WebSocket(url);
      socket_handler.socket.onmessage = socket_handler.showMessage;
    },
    showMessage: function (e) {
      var msg = JSON.parse(e.data);
      if (msg.action == "countdown") {
        var counter = 3,
            interval = setInterval(function () {
              if (counter == 0) {
                $("#counter").text("Smile!");
                clearInterval(interval);
              } else $("#counter").text(counter);
              counter--;
            }, 1000);
      } else if (msg.action == "single") {
        $("#photo").css("background-image", "url('"+msg.filename+"')");
      }
    },
    sendMessage: function (action) {
      var state = socket_handler.socket.readyState;
      if (state == 2 || state == 3) socket_handler.start();
      state = socket_handler.socket.readyState;
      if (state != 1) {
        console.log("Reconnecting: " + state);
        setTimeout(socket_handler.sendMessage(action), 10);
        return;
      }
      socket_handler.socket.send(JSON.stringify({"action": action}));
    }
  };

  window.go = function () {
    socket_handler.sendMessage('go');
    $("#go-button").hide();
    $("#counter").show();
  }

  $(function () {
    socket_handler.start();
  });

})();
