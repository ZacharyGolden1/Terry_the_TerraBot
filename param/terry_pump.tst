# Wait a bit before starting, to give agent a chance to initialize
DELAY FOR 60

# Create an environment with soil moisture below the threshold
BASELINE = cold_and_dry.bsl

# Ensure the water pump is activated when soil moisture is low
WHENEVER smoist[0] < 480 or smoist[1] < 480
  WAIT wpump FOR 1800
  PRINT "Water Pump ON at %s (soil moisture %d)" %(clock_time(time), smoist[0])
  ENSURE wpump FOR 60

# Simulate the water pump turning off after watering
WHENEVER wpump
  WAIT not wpump FOR 360
  PRINT "Water Pump OFF at %s" %(clock_time(time))

# Ensure that the water pump doesn't turn on if the moisture level is high
WHENEVER smoist[0] > 600 or smoist[1] > 600
  WAIT not wpump FOR 360

# Ensure that the water pump stays off when moisture levels are normal
WHENEVER smoist[0] >= 480 and smoist[0] <= 600 and smoist[1] >= 480 and smoist[1] <= 600
  ENSURE not wpump FOR 3600

QUIT AT 1-23:59:59 # Run the test and simulator for 1 day