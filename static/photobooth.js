(function () {

  "use strict"

  var interval, counter, nphotos, final_filename;

  function process_response (data) {
    if (typeof data.next_url !== "undefined") {
      $("#counter").hide();
      $("#photo").show();
      $("#photo").css("background-image", "url('"+data.filename+"')");
      setTimeout(function () {
        countdown(data.next_url);
      }, 3000);
    } else {
      $("#counter").hide();
      $("#photo").show();
      $("#photo").css("background-image", "url('"+data.final+"')");
      $("#buttons").show();
      final_filename = data.final;
    }
  }

  function countdown (url) {
    $("#photo").hide();
    $("#counter").show().text("");
    counter = 3;
    interval = setInterval(function () {
      if (counter == 0) {
        $("#counter").text("Smile!");
        clearInterval(interval);
        $.getJSON(url, process_response);
      } else $("#counter").text(counter);
      counter--;
    }, 1000);
  }

  window.go = function () {
    $("#go-button").hide();
    countdown("/take");
  }

  window.try_again = function () {
    $("#buttons").hide();
    $("#photo").hide();
    $("#go-button").show();
  }

  window.print = function () {
    $.getJSON(final_filename + "/print", function () {
      $("#buttons").hide();
      $("#photo").hide();
      $("#go-button").show();
    });
  }

  window.print_and_tweet = function () {
    $.getJSON(final_filename + "/print?tweet=yes", function () {
      $("#buttons").hide();
      $("#photo").hide();
      $("#go-button").show();
    });
  }

})();
