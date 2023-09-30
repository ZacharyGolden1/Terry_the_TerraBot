BASELINE = default_baseline.bsl

# Wait a minute before starting, to give agent a chance to initialize
DELAY FOR 60

# Simulate high temperature to trigger the fan
SET temperature[0] TO 30
SET temperature[1] TO 31

# Ensure the fan turns on when temperature is high
WHENEVER temperature[0] > 29 or temperature[1] > 29
  WAIT fan FOR 1800
  PRINT "FAN ON at %s (temperature %d)" %(clock_time(time), temperature[0])
  ENSURE fan FOR 60

# Simulate normal temperature to turn off the fan
SET temperature[0] TO 25
SET temperature[1] TO 26

# Ensure the fan stays off when temperature is normal
WHENEVER temperature[0] < 30 and temperature[1] < 30
  ENSURE not fan FOR 3600

QUIT AT 1-00:00:00 # End the test after 1 day