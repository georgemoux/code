library(ggplot2)
library(dplyr)
library(plotrix)
library(tidyverse)

#read data file
BBB_data<-read.csv("C:\\Users\\George Moukarzel\\Desktop\\CB3\\BBB-CB2-CB3-raw.csv")
#rename week column because it seems weird for some reason
colnames(BBB_data)[1]<-"week"

#run t tests
t_BBB<-t.test(BBB_data$BBB ~ BBB_data$type)


#create summary variables
BBBtidy=group_by(BBB_data,week,type) %>% summarise(MBBB=mean(BBB),SEBBB=std.error(BBB))

#create bar plot variables
plot_BBB <-ggplot(BBBtidy, aes(x=week, y=MBBB, fill=type)) + geom_bar(position="dodge", stat="identity",width=0.8) + geom_errorbar(aes(ymin=MBBB-SEBBB,ymax=MBBB+SEBBB),width=0.2,position=position_dodge(0.8))