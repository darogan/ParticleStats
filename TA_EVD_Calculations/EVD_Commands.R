

library(evd)

bestscores <- read.table("RandomScores_Random_1000_512_5_0_360_3_100_2_100.txt", header=TRUE)

#jpeg()

#plot(ecdf(bestscores$lscores), do.points=FALSE, verticals=TRUE)

#qqnorm(bestscores$lscores); qqline(bestscores$lscores)

bestsorted <- sort(bestscores$lscores)

#qqnorm(bestsorted)

data1 <- rgev(bestsorted)
fgev(data1)


#plot(data2)


#hist(bestsorted)
#plot(bestsorted)





#long <- bestscores$lscores[bestscores$lscores > 3]
#plot(ecdf(long), do.points=FALSE, verticals=TRUE)

#qqnorm(long); qqline(long)
