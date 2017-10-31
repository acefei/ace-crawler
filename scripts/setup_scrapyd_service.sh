#!/usr/bin/bash
program=scrapyd

cd /etc/init.d/
cat > $program <<'EOF'
# chkconfig: 2345 95 05
PORT=6800
WORKSPACE=/tmp
CMD=/usr/bin/scrapyd
SERVICE=scrapyd

pid=`netstat -lnopt | grep :$PORT | awk '/python/{gsub(/\/python/,"",$7);print $7;}'`

start() {
   if [ -n "$pid" ]; then
      echo "$SERVICE already start..."
      return 0
   fi
   
   cd $WORKSPACE
   nohup $CMD &
   echo "start scrapy on port:$PORT"
}

stop() {
   if [ -z "$pid" ]; then
      echo "$SERVICE already down..."
      return 0
   fi

   kill -9 $pid
   echo "stop $SERVICE with pid:$pid"
}

status() {
   if [ -z "$pid" ]; then
      echo "$SERVICE already down..."
   else
      echo "$SERVICE is running with pid:$pid"
   fi
}

case $1 in
   start)
      start
   ;;
   stop)
      stop
   ;;
   status)
      status
   ;;
   *)
      echo "Usage: {start|stop|status}"
   ;;
esac

exit 0
EOF

chmod +x $program
chkconfig $program on
