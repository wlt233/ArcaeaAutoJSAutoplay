var ra = new RootAutomator();
events.on('exit', function(){
  ra.exit();
});

var slot = []

init = (new Date()).getTime();
i = 0

while(true){
  j = (new Date()).getTime()
  if(j> (slot[i][0] + init)) {
    executeFunc(slot[i]);
    i++;
  }
  if(j> (slot[i][0] + init)) {
    executeFunc(slot[i]);
    i++;
  }
}

function executeFunc(a) {
  switch(a[2]){
    case 0:
      ra.touchDown(a[4],a[3],a[1]);
      console.log('Touch Down at ' + String(a[4]) + '  ' + String(a[3]) + '  ' + String(a[1]));
      break
    case 1:
      ra.touchUp(a[1]);
      console.log('Touch Up at ' + String(a[4]) + '  ' + String(a[3]) + '  ' + String(a[1]));
      break
    case 2:
      ra.touchMove(a[4],a[3],a[1]);
      console.log('Touch Move at ' + String(a[4]) + '  ' + String(a[3]) + '  ' + String(a[1]));
      break
  }
} 