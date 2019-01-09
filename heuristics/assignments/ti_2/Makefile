# Copyright 2018 Matheus Nunes <mhnnunes@dcc.ufmg.br>
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


ALL = tp2
SRC = $(wildcard *.cpp)
OWNLIBS = $(wildcard ../lib/*.cpp)
OBJ = $(patsubst %.cpp, %.o, $(wildcard *.cpp))
LIBOBJS = $(patsubst %.cpp, %.o, $(wildcard ../lib/*.cpp))

CC = g++

# The flags below will be included in the implicit compilation rules
# 'make' infers that the code in the directory is in c++
# and looks for the CPPFLAGS variable
CPPFLAGS = -g -Wall -std=c++11 -O3

all: $(ALL)

$(ALL): $(OBJ) $(LIBOBJS)
	$(CC) $(CPPFLAGS) -c $(OWNLIBS)
	$(CC) $(CPPFLAGS) -c $(SRC)
	$(CC) $(CPPFLAGS) $(LIBOBJS) $(OBJ) -o $@ 

clean:
	rm $(ALL) *.o *.log ../lib/*.o

