function moveUp() {
  webSocket.send("M106 G1 Y10");
  
  $.ajax({
    type: 'POST',
    contentType: 'application/json',
    url: '/post/data',
    dataType: 'json',
    data: JSON.stringify(data),
    success: function(result) {
      jQuery("#clash").html(result);
    },error: function(result) {
      console.log(result);
    }
  });
}

function moveDown() {
  webSocket.send("M106 G1 -Y10");
}

function moveLeft() {
  webSocket.send("M106 G1 X10");
}

function moveRight() {
  webSocket.send("M106 G1 -X10");
}