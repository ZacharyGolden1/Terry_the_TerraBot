# Humidity Test
BASELINE = high_humid_baseline.bsl

# Wait a minute before starting, to give agent a chance to initialize
DELAY FOR 60

# Whenever humidity is high, ensure the fan turns on for at least a minute
WHENEVER humidity[0] > 80 or humidity[1] > 80
  WAIT fan FOR 1800
  PRINT "Fan ON at %s (humidity %d)" %(clock_time(time), humidity[0])
  ENSURE fan FOR 60
  WAIT not fan FOR 1800
  PRINT "Fan OFF at %s" %(clock_time(time))
  WAIT humidity[0] < 87 FOR 1800

# Ensure the fan doesn't turn on when humidity is normal
WHENEVER humidity[0] <= 80 and humidity[1] <= 80
  ENSURE not fan FOR 3600

QUIT AT 2-23:59:59 # Run the test and simulator for 2 days
