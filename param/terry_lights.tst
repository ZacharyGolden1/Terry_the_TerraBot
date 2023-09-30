# Test file for Light Behavior
BASELINE = default_baseline.bsl

# Wait a minute before starting, to give agent a chance to initialize
DELAY FOR 60

# Ensure lights don't come on before 6 AM
WHENEVER 1-06:00:00
  ENSURE not led UNTIL 1-06:00:00

# Ensure lights turn off at 10 PM
WHENEVER 1-22:00:00
  WAIT not led FOR 360
  PRINT "Lights OFF at %s" %(clock_time(time))
  ENSURE not led UNTIL 2-06:59:59

QUIT AT 1-23:59:59 # Run the test and simulator for 1 day
