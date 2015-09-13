(function () {

  "use strict"

  var interval, counter, nphotos, final_filename, timeout;

  function process_response (data) {
    clearTimeout(timeout);
    if (typeof data.next_url !== "undefined") {
      $("#counter").hide();
      $("#working").hide();
      $("#photo").show();
      $("#photo").css("background-image", "url('"+data.filename+"')");
      setTimeout(function () {
        countdown(data.next_url);
      }, 3000);
    } else {
      $("#counter").hide();
      $("#working").hide();
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
        timeout = setTimeout(function () {
          $("#counter").hide();
          $("#working").show();
        }, 1000);
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
    $("#error").hide();
    $("#go-button").show();
    $.ajax({
      url: "/setup",
      dataType: "json",
      error: handle_error
    });
  }

  window.tweet = function () {
    $.getJSON(final_filename + "/print?tweet=yes", function () {
      $("#buttons").hide();
      $("#photo").hide();
      $("#go-button").show();
    });
  }

  window.print = function () {
    $.getJSON(final_filename + "/print?print=yes", function () {
      $("#buttons").hide();
      $("#photo").hide();
      $("#go-button").show();
    });
  }

  window.print_and_tweet = function () {
    $.getJSON(final_filename + "/print?tweet=yes&print=yes", function () {
      $("#buttons").hide();
      $("#photo").hide();
      $("#go-button").show();
    });
  }

  function handle_error (jqXHR, textStatus, errorThrown) {
    clearInterval(interval);
    clearTimeout(timeout);
    $("#buttons").hide();
    $("#photo").hide();
    $("#counter").hide();
    $("#working").hide();
    $("#go-button").hide();
    $("#error").show();
    $("#error-inner").text(jqXHR.responseText);
  }

  $(function () {
    $.ajax({
      url: "/setup",
      dataType: "json",
      error: handle_error
    });
  });

})();
