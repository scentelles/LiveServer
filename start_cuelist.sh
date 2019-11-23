echo $1
OSC_PATH="/start_cuelist/$1"
FULL_COMMAND="10.3.141.1 5005 ${OSC_PATH} i 255"
echo "sendosc"$FULL_COMMAND
sendosc $FULL_COMMAND
