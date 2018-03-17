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
library(reshape2);
days <- read.csv(file='/home/math/git/dmepd/news_daily.csv', header=T, sep=',');

# ggplot(data=week, aes(x=X..date, y=g1.tweet.cur, group=1)) +
#     geom_line() + 
#     geom_point()


dat.m <- melt(days, id="X..datedelta");

dat.m$X..datedelta <- factor(dat.m$X..datedelta, levels=unique(dat.m$X..datedelta))

# dat.m <- rename(dat.m, c("days","newssource","qtd");

# positions <- c(dat.m$X..datedelta)
bc <- ggplot(data=dat.m, aes(x=X..datedelta, y=value, fill=variable)) +
      geom_bar(stat="identity", position="stack") + 
      theme(
            legend.title=element_blank(),
            legend.text=element_text(size=14),
            axis.title.x=element_text(size=14), 
            # axis.ticks.x=element_blank(),
            axis.text.x = element_text(size=14, angle=80, hjust=0.65, vjust=0.55),
            axis.title.y=element_blank(), 
            axis.text.y = element_text(size=14)) +
      scale_fill_brewer(type="qual", palette=6, direction=-1,
                        label=c("Folha", "G1")) +
      # scale_x_reverse() +
      # scale_fill_distiller(direction=1) +
      scale_x_discrete(name="Days", limits=levels(dat.m$X..datedelta));
# bc <- bc + geom_text(data=dat.m, aes(label=X..datedelta, angle=25), 
#                   hjust=0,
#                   vjust=0,
#                   position="stack",
#                   size=4);
      # scale_y_log10()

plot(bc)
