# ALL = ti1

# # CC ?= "g++"

# CFLAGS ?= -std=c++11 -g -lm

# # OBJS = main.o io.o graph.o
# # CPPS =  io.cpp graph.cpp main.cpp

src = $(wildcard *.cpp)
obj = $(src:.cpp=.o)

# # : $(ALL)
# 	# $(CC) $(CFLAGS) -o $(ALL) $(OBJS)

# $(ALL): $(OBJS)
# 	# $(CC) $(CFLAGS) -c $(CPPS)
# 	$(CC) -o $@ $^ $(CFLAGS)

# clean:
# 	rm -f *.o


CC = g++
CFLAGS = -g -Wall -std=c++11 

all: tsp 

tsp: $(obj)
	$(CC) $(CFLAGS) -c $(src)
	$(CC) $(CFLAGS) $(obj) -o $@ 

# main.o: main.cpp  
# 	$(CC) $(CFLAGS) -c main.cpp

# constructive.o: constructive.hpp constructive.cpp  
# 	$(CC) $(CFLAGS) -c constructive.cpp

# tsp.o: tsp.hpp tsp.cpp
# 	$(CC) $(CFLAGS) -c tsp.cpp

# city.o: city.hpp city.cpp  
# 	$(CC) $(CFLAGS) -c city.cpp io_utils.o: io_utils.hpp io_utils.cpp 
# 	$(CC) $(CFLAGS) -c io_utils.cpp 

clean:
	rm tsp *.o