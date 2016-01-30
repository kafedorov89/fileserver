#!/bin/bash

#
# This script is copied into the guest with the 32 and 64 bit upgrader binaries.
# It selects one of the binaries based on the userland bitness of the guest and
# runs it.
#

BINDIR=`dirname $0`
DBPATH="/etc/vmware-tools/locations"
LOGFILE='/var/log/vmware-tools-upgrader.log'
UPGRADER64="$BINDIR/vmware-tools-upgrader-64"
UPGRADER32="$BINDIR/vmware-tools-upgrader-32"

# Close all the inherited FDs. See bug 138500 for details.
MAXFD=$(expr `ulimit -n` - 1)
for fd in `seq 3 $MAXFD`; do
   eval "exec $fd>&-"
done

# Check userland bitness.
if LANG=C file -- "$SHELL" | grep 64-bit >& /dev/null;
then
   UPGRADER=$UPGRADER64;
else
   UPGRADER=$UPGRADER32;
fi

# Construct argument list based on whether Tools is
# already installed or not. If user passes args, though,
# use them blindly.
# (-s checks to see if a file exists and has nonzero length.)

if [ ! -s "$DBPATH" ] && [ -z "$@" ];
then
   UPGRADERARGS="-p --default"
else
   # Has no effect if $@ is empty
   UPGRADERARGS="$@"
fi

# Setup the logfile in a spot that avoids SElinux errors and allows for
# better debugging of upgrader errors.  Add the date as the first line
# so we can get a better handle on the situation.  This also effectively
# deletes any prvious log file that may have been there.
date >$LOGFILE

chmod +x $UPGRADER
# Run the upgrader.
# Delay starting the upgrader till rhgb-client (if present and running) has
# quit.
RHGBCLNT=/usr/bin/rhgb-client
if [ -x $RHGBCLNT ]; then
   while true ; do
      if ! $RHGBCLNT --ping ; then
         break
      fi
      echo "Waiting for rhgb to exit, will sleep for 30 seconds..." >> $LOGFILE
      sleep 30
   done
fi

echo "Executing \"$UPGRADER $UPGRADERARGS\"" >>$LOGFILE 2>&1
exec $UPGRADER $UPGRADERARGS >>$LOGFILE 2>&1

# If here then the exec failed.
echo "Exec call failed!" >>$LOGFILE 2>&1
exit 1

