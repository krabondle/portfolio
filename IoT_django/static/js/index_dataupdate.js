$(document).ready(function () {
    $("#buzzer_on").click(function () {
      console.log("#buzzer_on");
      var topic, value;
      topic = "Sensors/buzzer";
      value = "P";
      $.get("/mqtt_publisher/", { 'topic': topic, 'value': value }, function (ret) {
      })
    });
    $("#relay_on").click(function () {
      console.log("#relay_on");
      var topic, value;
      topic = "Sensors/SW_01";
      value = "O";
      $.get("/mqtt_publisher/", { 'topic': topic, 'value': value }, function (ret) {
      })
    });
    $("#relay_off").click(function () {
      console.log("#relay_off");
      var topic, value;
      topic = "Sensors/SW_01";
      value = "C";
      $.get("/mqtt_publisher/", { 'topic': topic, 'value': value }, function (ret) {
      })
    });
    function refresh() {
      //sensors.forEach(Update);
      $.get("/data_update/", { 'item': location.pathname.replace("/","").replace("/","") },function(ret) {
          
          for (i in ret){
            if (ret[i] == 404){
              //document.getElementById("div_"+i).style.display = "none";
              //document.getElementById("div_"+i).style.display = "";
              $('#'+i).html("Offline");
            }else{
              //document.getElementById("div_"+i).style.display = "";
              if (ret[i][0] instanceof Array){
                $('#'+i).html(ret[i][0].toString());
              }else{
                $('#'+i).html(ret[i][0]);
              }
            }
          }
            /*
          for (x in ret) {
            if (community_sensors.find(element => element == x) == x){
              document.getElementById("div_"+x).style.display = "";
              $('#'+x).html(ret[x][0][0]);
            }
            //document.getElementById("div_"+x).style.display = "";
            //console.log(typeof(x));
            //console.log(ret[x]);
            //console.log(ret[x][0]);
          }*/
        });
      /*function Update() {
        $.get("/data_update/",function(ret) {
          //console.log(ret.sensor[0]);
          //$('#'+item).html(ret.sensor[0])
          //console.log(ret);
        })
      }*/
    }
    setInterval(refresh, 1000)
  });