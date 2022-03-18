library(ggplot2)
library(dplyr)
library(plotrix)
library(tidyverse)
library(nlme)
library(tidyr)
library(ggpubr)
library(car)
library(Hmisc)
library(rstatix)
library(emmeans)

theme_update(plot.title = element_text(hjust = 0.5))

#read data file
ladder_data<-read.csv("data/summary_ladder-cb2cb3.csv")
#rename week column because it seems weird for some reason
#colnames(ladder_data)[1]<-"week"

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

# run stats: let's make new df with percent normalized columns so we have all metadata too:
ldp <- ladder_data %>% mutate(hit_pct=hit/total,slip_pct=slip/total,miss_pct=miss/total)

# do a mixed effects model on hits:
hmod <- lme(hit_pct ~ type*week, random = ~1 | rat/week,na.action=na.omit,data=ldp)
anova(hmod)
# hmm. main effect of type not significant, nor interaction. are we allowed to do follow up tests? ah, why not.
hitaov <- anova_test(
  data = ldp, dv = hit_pct, wid = rat,
  between = type, within = week
)
get_anova_table(hitaov)

#d1a <- d1 %>%
#  group_by(Timepoint_Name) %>%
#  anova_test(dv = Mean_Asis_Toe_Height, wid = Rat, between = exptype) %>%
#  get_anova_table() %>%
#  adjust_pvalue(method = "bonferroni")
#d1a

# try with just weeks 678:
ldp678 <- ldp %>% filter(week %in% c("week6","week7","week8") )
hmod678 <- lme(hit_pct ~ type*week, random = ~1 | rat/week,na.action=na.omit,data=ldp678)
anova(hmod678)

# try with just experimentals (all we care about for withdrawal)
ldp678e <- ldp %>% filter(week %in% c("week6","week7","week8")) %>% filter(type=='exp')
hmod678e <- lme(hit_pct ~ week, random = ~1 | rat/week,na.action=na.omit,data=ldp678e)
anova(hmod678e)

ldp678es <- ldp678e %>% group_by(week) %>% summarise(hit_pct_mn=mean(hit_pct),hit_pct_sem=std.error(hit_pct))

# make bar plot with std error bars with just exp:
p<- ggplot(ldp678es, aes(x=week, y=hit_pct_mn)) + 
  geom_bar(stat="identity", color="black", 
           position=position_dodge()) +
  geom_errorbar(aes(ymin=hit_pct_mn-hit_pct_sem, ymax=hit_pct_mn+hit_pct_sem), width=.2,
                position=position_dodge(.9)) +
  theme_bw() + 
  coord_cartesian(ylim = c(0, 0.6)) +
  scale_x_discrete(labels = c("6", "7", "8")) +
  ylab('Hit Percentage') +
  ggtitle("CNO Withdrawal") +
  theme(plot.title = element_text(hjust = .5))
print(p)
ggsave("cnowithdraw.pdf")

# make bar plot from all data to get auto stats labels
# NO don't use this - it doesn't do the right anova...
p <- ldp678e %>% ggplot(aes(x=week, y=hit_pct)) + 
    stat_summary(fun.data = "mean_se", geom = "errorbar", width = bw, 
                 position = position_dodge(.3), color = "black") + 
    stat_summary(fun = "mean", geom = "line", size = ls, 
                 position = position_dodge(.3)) + 
    stat_summary(fun = "mean", geom = "point", size = ps, 
                 position = position_dodge(.3)) + 
    #scale_x_discrete(labels = c("Preinjury", "1w", "2w", "4w", "6w", "7w", "8w")) +
    #scale_fill_manual(values=c("#E1812C","#3274A1"),labels=c("Control","DREADDs"))+ # correct colors 
    #scale_color_manual(values = c("#E1812C","#3274A1"),labels=c("Control","DREADDs")) +
    #scale_y_continuous(limits=c(30, 70))+
    #labs(x = "") +
    #ylab(theunits) +
    #xlab("Time after SCI") +
    #ggtitle(thetitle) + 
    #facet_wrap(~Speed_Group,labeller = labeller(Speed_Group=speed_labelmap)) +
    # defaults to wilcoxon? UES
    stat_compare_means() +
    #stat_compare_means(aes(group = exptype), label =  "p.signif", 
    #                  hide.ns = TRUE, label.y=0.65 ) +
    #labs(color="Treatment:") +
    #coord_cartesian(ylim = c(0.4, 0.7))
    #stat_compare_means(aes(group = exptype), label =  "p.signif", 
    #                   method='t.test',  hide.ns = TRUE )
    theme_bw() + 
    theme(plot.title = element_text(hjust = .5,size=10))
p
# Finished bar plot
#p+labs(title="Tooth length per dose", x="Dose (mg)", y = "Length")+
#  theme_classic() +
#  scale_fill_manual(values=c('#999999','#E69F00'))


#
ldp678c <- ldp %>% filter(week %in% c("week6","week7","week8")) %>% filter(type=='ctrl')
hmod678c <- lme(hit_pct ~ week, random = ~1 | rat/week,na.action=na.omit,data=ldp678c)
anova(hmod678c)

ggplot(ldp,aes(x=week,y=hit_pct,fill=type)) + 
  geom_bar(position="dodge", stat="identity",width=0.8) +
  theme_bw()

# now run test on all data for miss for all weeks:
# do a mixed effects model on hits:
mmod <- lme(miss_pct ~ type*week, random = ~1 | rat/week,na.action=na.omit,data=ldp)
anova(mmod)
# hmm. main effect of type not significant, nor interaction. are we allowed to do follow up tests? ah, why not.
maov <- anova_test(
  data = ldp, dv = miss_pct, wid = rat,
  between = type, within = week
)
get_anova_table(maov)

mmod678 <- lme(miss_pct ~ type*week, random = ~1 | rat/week,na.action=na.omit,data=ldp678)
anova(mmod678)

mmod678e <- lme(miss_pct ~ week, random = ~1 | rat/week,na.action=na.omit,data=ldp678e)
anova(mmod678e)

mmod678c <- lme(miss_pct ~ week, random = ~1 | rat/week,na.action=na.omit,data=ldp678c)
anova(mmod678c)

# Now let's do slips:
smod <- lme(slip_pct ~ type*week, random = ~1 | rat/week,na.action=na.omit,data=ldp)
anova(smod)
# hmm. main effect of type not significant, nor interaction. are we allowed to do follow up tests? ah, why not.
saov <- anova_test(
  data = ldp, dv = slip_pct, wid = rat,
  between = type, within = week
)
get_anova_table(saov)

smod678 <- lme(slip_pct ~ type*week, random = ~1 | rat/week,na.action=na.omit,data=ldp678)
anova(smod678)

smod678e <- lme(slip_pct ~ week, random = ~1 | rat/week,na.action=na.omit,data=ldp678e)
anova(smod678e)

smod678c <- lme(slip_pct ~ week, random = ~1 | rat/week,na.action=na.omit,data=ldp678c)
anova(smod678c)

