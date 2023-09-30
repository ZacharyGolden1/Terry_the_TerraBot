# Test file for Temperature Behavior
BASELINE = high_temp_baseline.bsl

# Wait a bit before starting, to give agent a chance to initialize
DELAY FOR 60

# Ensure that the fan turns on when temperature is high
WHENEVER temperature[0] > 29 or temperature[1] > 29
  WAIT fan FOR 1800
  PRINT "Fan ON at %s (temperature %d)" %(clock_time(time), temperature[0])
  ENSURE fan FOR 60

# Simulate the fan turning off after cooling
WHENEVER fan
  WAIT not fan FOR 360
  PRINT "Fan OFF at %s" %(clock_time(time))

# Ensure that the fan stays off when temperature levels are normal
WHENEVER temperature[0] >= 22 and temperature[0] <= 29 and temperature[1] >= 22 and temperature[1] <= 29
  ENSURE not fan FOR 3600

QUIT AT 1-23:59:59 # Run the test and simulator for 1 day
