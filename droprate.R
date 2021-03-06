calcCI <- function(p,n,reps=40000) {
    quantile(sapply(1:reps,function(i) { sum(runif(n) <= p) }),c(0.025,0.975))
}
reps=40000
runs <- c(1:1000)
ps <- c(0.012,0.025,0.034,0.0375,0.057,0.075,0.067,0.069,0.093,0.1,0.15,0.132,0.15,0.165,0.22,0.25,0.3,1.0/3.0,0.5)
rates <- c(1.20 ,2.50 ,3.4 ,3.75 ,5.7 ,6.70 ,6.90 ,7.5 ,9.3 ,10 ,11.40 ,12.50 ,13.20 ,13.5 ,14 ,15 ,16.50 ,20 ,22 ,25.00 ,29 ,30 ,33 ,33.30 ,35 ,50 ,100)

rrGen <- function() {
    rr <- lappy(rates, function(rate) {
        ranges <- sapply(c(1:1000),function(i) { calcCI(rate/100.0,i) })
        data.frame(t(ranges))
    })
}


p = 10.00 / 100.0
trials = 10
n = 50
x <- sapply(1:n,function(i) { sum(runif(trials) <= p) })
png("ci95-example.png",width=1024,height=768,pointsize = 20)
par(mar=c(5.1, 4.1, 4.1, 5.1),mfrow=c(3,1)) 
q <- quantile(x,c(0.025,0.975))
paramTitle = paste("Droprate ",p," and ",trials," trials repeated ",n,"times") 
plot(x,main=paramTitle,xlab="Trials",ylab="Number of drops")
hist(x,xlab="Count of Trials with # Drops",main="Histogram of # of Drops")
ciTitle = paste("95% CI",": [",q[1],", ",q[2],"]")
plot(sort(x),main=ciTitle,xlab="Trials sorted by Drops",ylab="Number of drops")
abline(v=c(1+0.025*n),col=c("orange"))
abline(v=c(0.975*n),col=c("blue"))
#mtext(myTitle, side = 3, outer=TRUE)
mtext(paste(paramTitle,ciTitle), outer=TRUE, cex=1, line=-1.5)
dev.off()
