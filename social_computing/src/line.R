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
week <- read.csv(file='/home/math/git/dmepd/sentiment_analysis_weekly.csv',  header = T, sep=',');
# Set names for each table
names(week) <- c("week", "avgg1", "avgfolha", "avgtweet");
# Get min and max for each table

globalmin <- apply(week, 2, min)
globalmax <- apply(week, 2, max)

yrange <- range(c(globalmin["avgtweet"], globalmin["avgg1"], globalmin["avgfolha"],
                  globalmax["avgtweet"], globalmax["avgg1"], globalmax["avgfolha"]))
# yrange <- range(c(-1, 1))
xrange <- week$week
# xrange <- range(c(1, 500))
# Create plot and add lines
plot(week$week, week$avgg1, 
    type="o",
    pch=19,
    ylab="Polaridade", ylim=yrange,
    xlab="Semanas",
    main="Polaridade (Sentimento) Média por Semana",
    col="red");
# text(500, ants10$gbest[500] + 150, ants10$gbest[500])
lines(week$week, week$avgfolha,
    type="o",
    pch=19,
    col="blue");
lines(week$week, week$avgtweet,
    type="o",
    pch=19,
    col="orange");
legend("topright",
    c("Folha", "G1", "Tweets"),
    pch=19,
    col=c("blue", "red", "orange"),
    cex=0.9);