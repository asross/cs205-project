#=================================================
# Makefile
#=================================================
CFLAGS   = -c -O2 -fopenmp -lm
COMPILER = gcc
PRO         = openmp
OBJECTS     = ${PRO}.o

${PRO}.x : $(OBJECTS)
	$(COMPILER) -o ${PRO}.x $(OBJECTS) -fopenmp -lm

%.o : %.c
	$(COMPILER) $(CFLAGS) $(<F)

clean :
	rm -fr *.o *.x
