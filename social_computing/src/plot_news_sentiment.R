#! /usr/bin/Rscript

# Copyright 2017 Matheus Nunes <mhnnunes@dcc.ufmg.br>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


library(ggplot2);
data <- read.csv(file='/home/math/git/dmepd/news_twitter_sentiment.csv', 
                  header=T, sep=',');

# data$X..date <- factor(data$X..date)
# dat.c <- cast(data)
data$X..date <- factor(data$X..date, levels=unique(data$X..date))


lc <- ggplot(data=data, aes(x=factor(X..date), y=value, labels=data$X..date, group=1)) +
      # ylim(0,1) + 
      # geom_label() + 
      geom_line(size=1.5, aes(y=G1, color='aG1')) + 
      geom_point(size=2.5, aes(y=G1, color='aG1')) + 
      geom_line(size=1.5, aes(y=Folha, color='Folha')) + 
      geom_point(size=2.5, aes(y=Folha, color='Folha')) +
      geom_line(size=1.5, aes(y=Twitter, color='Twitter')) + 
      geom_point(size=2.5, aes(y=Twitter, color='Twitter')) +
      geom_hline(yintercept=0) +
      theme(
            legend.title=element_blank(),
            legend.text=element_text(size=14),
            axis.title.x=element_blank(), 
            axis.text.x = element_text(size=14, angle=80, hjust=0.55, vjust=0.55),
            axis.title.y=element_blank(), 
            axis.text.y = element_text(size=14)) + 
      scale_color_brewer(type="qual", palette=6, direction=1, labels=c('G1', 'Folha', 'Twitter')) +
      # scale_linetype_discrete(name="Type", labels=c("Same Week", "Next Week")) +
      scale_x_discrete(name="Days", limits=levels(data$X..datedelta)) +
      scale_y_continuous(name="Similarity", breaks=seq(-1, 1, 0.02))      

lc


# lc <- ggplot(data=week, aes(x=factor(X..date), y=value, labels=week$X..date, group=1)) +
#       # ylim(0,1) + 
#       # geom_label() + 
#       geom_line(size=1.5, aes(y = folha.tweet.cur, linetype="dashed")) + 
#       geom_point(size=2.5, aes(y = folha.tweet.cur)) + 
#       geom_line(size=1.5, aes(y = folha.tweet.next, linetype="dotted")) + 
#       geom_point(size=2.5, aes(y = folha.tweet.next)) +
#       theme(
#             legend.title=element_blank(),
#             legend.text=element_text(size=14),
#             axis.title.x=element_blank(), 
#             axis.text.x = element_text(size=14),
#             axis.title.y=element_blank(), 
#             axis.text.y = element_text(size=14)) +
#       scale_linetype_discrete(name="Type", labels=c("Same Week", "Next Week")) +
#       scale_x_discrete(name="Weeks", labels=c(
#                         "Set-17",
#                         "Set-24",
#                         "Oct-01",
#                         "Oct-08",
#                         "Oct-15",
#                         "Oct-22")) + 
#       scale_y_continuous(name="Similarity", breaks=seq(0, 1, 0.05))      

# lc