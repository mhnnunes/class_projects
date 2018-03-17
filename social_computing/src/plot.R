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

# # Load each summarized file
week37 <- read.csv(file='/home/math/git/dmepd/result_week_37.csv',  
                   header = F, sep=',');
week38 <- read.csv(file='/home/math/git/dmepd/result_week_38.csv',  
                   header = F, sep=',');
week39 <- read.csv(file='/home/math/git/dmepd/result_week_39.csv',  
                   header = F, sep=',');
week40 <- read.csv(file='/home/math/git/dmepd/result_week_40.csv',  
                   header = F, sep=',');
week41 <- read.csv(file='/home/math/git/dmepd/result_week_41.csv',  
                   header = F, sep=',');
week42 <- read.csv(file='/home/math/git/dmepd/result_week_42.csv',  
                   header = F, sep=',');
week44 <- read.csv(file='/home/math/git/dmepd/result_week_44.csv',  
                   header = F, sep=',');

# Set names for each table
names(week37) <- c("mctweet", "ftweet", "mcnews", "fnews");
names(week38) <- c("mctweet", "ftweet", "mcnews", "fnews");
names(week39) <- c("mctweet", "ftweet", "mcnews", "fnews");
names(week40) <- c("mctweet", "ftweet", "mcnews", "fnews");
names(week41) <- c("mctweet", "ftweet", "mcnews", "fnews");
names(week42) <- c("mctweet", "ftweet", "mcnews", "fnews");
names(week44) <- c("mctweet", "ftweet", "mcnews", "fnews");

# counts <- table(c(week37$ftweet, week37$fnews),
#                 c(week38$ftweet, week38$fnews), 
#                 c(week39$ftweet, week39$fnews), 
#                 c(week40$ftweet, week40$fnews), 
#                 c(week41$ftweet, week41$fnews))
# counts <- table(week37$mctweet, week37$ftweet)
counts <- c(week37$ftweet[1], week38$ftweet[1], 
            week39$ftweet[1], week40$ftweet[1], 
            week41$ftweet[1], week42$ftweet[1], 
            week42$ftweet[1])
labels <- c(week37$mctweet[1], week38$mctweet[1], 
            week39$mctweet[1], week40$mctweet[1], 
            week41$mctweet[1], week42$mctweet[1], 
            week42$mctweet[1])
barplot(counts, main="Freq tweet vs. freq news",
  xlab="words", names.arg=labels)
# Get min and max for each table
# min37 <- apply(week37, 2, min)
# min38 <- apply(week38, 2, min)
# min39 <- apply(week39, 2, min)
# min40 <- apply(week40, 2, min)
# min41 <- apply(week41, 2, min)
# min42 <- apply(week42, 2, min)
# min44 <- apply(week44, 2, min)

# max37 <- apply(week37, 2, max)
# max38 <- apply(week38, 2, max)
# max39 <- apply(week39, 2, max)
# max40 <- apply(week40, 2, max)
# max41 <- apply(week41, 2, max)
# max42 <- apply(week42, 2, max)
# max44 <- apply(week44, 2, max)


# globalmin <- apply(t(cbind(min37, min38, min39, min40, min41, min42, min44)), 2, min)
# globalmax <- apply(t(cbind(max37, max38, max39, max40, max41, max42, max44)), 2, max)

# yrange <- range(c(globalmin["lbest"], globalmin["gbest"],
#                   globalmax["lbest"], globalmax["gbest"]))

# xrange <- range(c(1, 500))
# Create plot and add lines
# plot(seq(1, length(ants10$lbest), 1), ants10$gbest, 
#     type="o",
#     pch=19,
#     ylab="Melhor Solução", ylim=yrange,
#     xlab="Gerações", xlim=xrange,
#     main="Melhor solução global vs. Iterações (SJC1)",
#     col="red");
# text(500, ants10$gbest[500] + 150, ants10$gbest[500])
# lines(seq(1, length(ants30$lbest), 1), ants30$gbest,
#     type="o",
#     pch=19,
#     col="blue");
# text(500, ants30$gbest[500] + 150, ants30$gbest[500])
# lines(seq(1, length(ants60$lbest), 1), ants60$gbest,
#     type="o",
#     pch=19,
#     col="orange");
# text(500, ants60$gbest[500] + 150, ants60$gbest[500])
# lines(seq(1, length(ants90$lbest), 1), ants90$gbest,
#     type="o",
#     pch=19,
#     col="purple");
# lines(seq(1, length(antsnp$lbest), 1), antsnp$gbest,
#     type="o",
#     pch=19,
#     col="black");
# text(500, ants90$gbest[500] + 150, ants90$gbest[500])
# legend("topright",
#     c("10", "30", "60", "90", "n-p"),
#     pch=19,
#     col=c("red", "blue", "orange", "purple", "black"),
#     cex=1, text.width=25);