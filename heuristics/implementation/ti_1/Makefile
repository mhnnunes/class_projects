# ALL = tsp
# SRC = $(wildcard *.cpp)
# OBJ = $(patsubst %.cpp, %.o, $(wildcard *.cpp))

# CC = g++
# CFLAGS = -g -Wall -std=c++11 -O3

# all: $(ALL)

# $(ALL): $(OBJ)
# 	$(CC) $(CFLAGS) -c $(SRC)
# 	$(CC) $(CFLAGS) $(OBJ) -o $@ 

# clean:
# 	rm tsp *.o

all: main.cpp graph.cpp io.cpp algorithm.cpp
	g++ -std=c++11 -c -g graph.cpp
	g++ -std=c++11 -c -g main.cpp
	g++ -std=c++11 -c -g algorithm.cpp
	g++ -std=c++11 -c -g io.cpp
	g++ -std=c++11 -o tp1 graph.o main.o io.o algorithm.o

clean:
	rm tp1 *.o
