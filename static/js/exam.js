

function makeTimer(expiration_time) {
    var endTime=new Date(expiration_time * 1000);
     endTime = (Date.parse(endTime) / 1000);
 
         var now = new Date();
         now = (Date.parse(now) / 1000);
 
         var timeLeft = endTime - now;
 
         var hours = Math.floor(timeLeft / 3600);
         var minutes = Math.floor((timeLeft - (hours * 3600 )) / 60);
         var seconds = Math.floor((timeLeft - (hours * 3600) - (minutes * 60)));

         if (hours==0 && minutes==0 && seconds==0){
             alert('TIME EXPIRED')
             window.location.reload();
         }

         if (hours < "10") { hours = "0" + hours; }
         if (minutes < "10") { minutes = "0" + minutes; }
         if (seconds < "10") { seconds = "0" + seconds; }

         $("#remaining_time").html('Remaining Time: '+hours+':'+minutes+':'+seconds);
         $("#hours").html(hours);
         $("#minutes").html(minutes);
         $("#seconds").html(seconds);
 
 }