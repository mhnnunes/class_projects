ALL = tp1
SRC = $(wildcard *.cpp)
OBJ = $(patsubst %.cpp, %.o, $(wildcard *.cpp))

CC = g++

# The flags below will be included in the implicit compilation rules
# 'make' infers that the code in the directory is in c++
# and looks for the CPPFLAGS variable
CPPFLAGS = -g -Wall -std=c++11 -O3

all: $(ALL)

$(ALL): $(OBJ)
	$(CC) $(CPPFLAGS) -c $(SRC)
	$(CC) $(CPPFLAGS) $(OBJ) -o $@ 

clean:
	rm $(ALL) *.o

# all: main.cpp graph.cpp io.cpp algorithm.cpp
# 	g++ -std=c++11 -c -g graph.cpp
# 	g++ -std=c++11 -c -g main.cpp
# 	g++ -std=c++11 -c -g algorithm.cpp
# 	g++ -std=c++11 -c -g io.cpp
# 	g++ -std=c++11 -o tp1 graph.o main.o io.o algorithm.o

# clean:
# 	rm tp1 *.o
