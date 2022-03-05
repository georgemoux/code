library(ggplot2)
library(dplyr)
library(plotrix)
library(tidyverse)

#read data file
ladder_data<-read.csv("C:\\Users\\George Moukarzel\\Desktop\\CB3\\summary_ladder-cb2cb3-678.csv")
#rename week column because it seems weird for some reason
colnames(ladder_data)[1]<-"week"

#assign new variables for percentage slip, miss and hit
slip_data <-data.frame(ladder_data[1],ladder_data["type"],ladder_data["slip"]/ladder_data["total"])
hit_data  <-data.frame(ladder_data[1],ladder_data["type"],ladder_data["hit"]/ladder_data["total"])
miss_data <-data.frame(ladder_data[1],ladder_data["type"],ladder_data["miss"]/ladder_data["total"])

#run t tests
t_hit<-t.test(hit_data$hit ~ hit_data$type)
t_miss<-t.test(miss_data$miss ~ miss_data$type)
t_slip<-t.test(slip_data$slip ~ slip_data$type)

#create summary variables
slips=group_by(slip_data,week,type) %>% summarise(Mslip=mean(slip),SEslip=std.error(slip))
hits=group_by(hit_data,week,type) %>% summarise(Mhit=mean(hit),SEhit=std.error(hit))
missS=group_by(miss_data,week,type) %>% summarise(Mmiss=mean(miss),SEmiss=std.error(miss))


#create bar plot variables
plot_slip <-ggplot(slips, aes(x=week, y=Mslip, fill=type)) + geom_bar(position="dodge", stat="identity",width=0.8) + geom_errorbar(aes(ymin=Mslip-SEslip,ymax=Mslip+SEslip),width=0.2,position=position_dodge(0.8))
plot_hit  <-ggplot(hits, aes(x=week, y=Mhit, fill=type)) + geom_bar(position="dodge", stat="identity",width=0.8)   + geom_errorbar(aes(ymin=Mhit-SEhit,ymax=Mhit+SEhit),width=0.2,position=position_dodge(0.8))
plot_miss <-ggplot(missS, aes(x=week, y=Mmiss, fill=type)) + geom_bar(position="dodge", stat="identity",width=0.8) + geom_errorbar(aes(ymin=Mmiss-SEmiss,ymax=Mmiss+SEmiss),width=0.2,position=position_dodge(0.8))