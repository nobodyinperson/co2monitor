#!/usr/bin/Rscript
# plot co2/temperature data
cat("Hint: select either 'all' or only the 'newest' file via command line argument.\n")

DATADIR <- "/var/lib/co2monitor/data"

ALLFILES <- Sys.glob(paste(DATADIR,"*.csv",sep="/"))
if(length(ALLFILES)<1) {
    stop(paste("no csv files in ",DATADIR))
    }
NEWESTFILE <- rev(ALLFILES)[1]

# read args
ARGS <- commandArgs(trailingOnly=TRUE)
ALL<-FALSE # default: plot only newest file
if(length(ARGS)>0) {
    if(grepl("all",ARGS))
        ALL <- TRUE
    if(grepl("newest",ARGS))
        ALL <- FALSE
    }



# settings
SETTINGS <- list()
SETTINGS$interval <- 10 # update interval

# plot
COLORS <- list()
COLORS$good   <- "darkgreen"
COLORS$middle <- "orange"
COLORS$bad    <- "red"


# open a window
X11()

# endless loop
while(TRUE) {
    print(dev.list())
    # read data
    if(ALL) { # read all files
        data <- as.data.frame(NULL)
        for(file in ALLFILES){
            cat(paste("reading file",file,"\n"))
            new <- read.csv(file,stringsAsFactors=F)
            data <- rbind(rbind(data,rep(NA,ncol(data))),new)
            }
        rm(new)
    } else { # only read newest file
        cat(paste("reading file",NEWESTFILE,"\n"))
        data <- read.csv(NEWESTFILE,stringsAsFactors=F)
        }
    # convert time
    data$time <- as.POSIXct(data$time)


    # adjust graphical parameters
    par(mfrow=c(2,1))
    par(mar=c(4,4,3,1)+0.3)
    plot(x=data$time,y=data$co2
         ,lwd=4,type="l",las=1
         ,main="co2 [ppm]"
         ,xlab="time"
         ,axes=F
         ,ylab="co2 [ppm]"
         ,ylim = c(0,min(3000,max(data$co2,na.rm=T)))
         ,panel.first=c(
            polygon(x=c(par("usr")[c(1,1,2,2)]),y=c(par("usr")[3],800,800,par("usr")[3]),col=COLORS$good)
            ,polygon(x=c(par("usr")[c(1,1,2,2)]),y=c(800,1200,1200,800),col=COLORS$middle)
            ,polygon(x=c(par("usr")[c(1,1,2,2)]),y=c(1200,par("usr")[4],par("usr")[4],1200),col=COLORS$bad)
            ,abline(v=axis.POSIXct(side=1,x=data$time),h=Axis(side=2,x=data$co2,las=1),lty=2,lwd=1,col="#000000aa")
            )
         )
    plot(x=data$time,y=data$temperature
         ,lwd=4,type="l",las=1
         ,main="temperature [°C]"
         ,xlab="time"
         ,axes=F
         ,ylab="temperature [°C]"
         ,panel.first=c(
            polygon(x=c(par("usr")[c(1,1,2,2)]),y=c(par("usr")[3],22,22,par("usr")[3]),col=COLORS$middle)
            ,polygon(x=c(par("usr")[c(1,1,2,2)]),y=c(22,26,26,22),col=COLORS$good)
            ,polygon(x=c(par("usr")[c(1,1,2,2)]),y=c(26,par("usr")[4],par("usr")[4],26),col=COLORS$middle)
            ,abline(v=axis.POSIXct(side=1,x=data$time),h=Axis(side=2,x=data$temperature,las=1),lty=2,lwd=1,col="#000000aa")
            )
         )

    # print time range
    mtext(side=3,line=2.5,text=paste(
            "(","time series from"
            ,strftime(min(data$time,na.rm=T),format="%d.%m.%Y %H:%M:%S")
            ,"to"
            ,strftime(max(data$time,na.rm=T),format="%d.%m.%Y %H:%M:%S")
            ,")"
            )
        )

    # sleep
    cat("sleeping...")
    for(sec in seq.int(SETTINGS$interval)) {
        if(is.null(dev.list())) {
            cat("window closed!\n")
            quit()
            }
        Sys.sleep(1)
        }
    cat("woke up!\n")

}
