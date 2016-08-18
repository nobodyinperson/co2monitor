#!/usr/bin/Rscript
# plot co2/temperature data

DATADIR <- "/var/lib/co2monitor/data"

ALLFILES <- Sys.glob(paste(DATADIR,"*.csv",sep="/"))
if(length(ALLFILES)<1) {
    stop(paste("no csv files in ",DATADIR))
    }
NEWESTFILE <- rev(ALLFILES)[1]

# read data
data <- read.csv(NEWESTFILE)
# convert time
data$time <- as.POSIXct(data$time)


# plot
X11()
par(mfrow=c(2,1))
plot(data$time,data$co2,lwd=2,type="l",main="co2 [ppm]")
plot(data$time,data$temperature,lwd=2,type="l",main="temperature [deg C]")

locator(1)

