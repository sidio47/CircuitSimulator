C=mpicc
# Standard
CFLAGS=-lm -std=gnu99 -g -W -Wall
# Optimized
CFLAGSOPT=-O3 -xavx2 -axmic-avx512 -ip -ipo -inline-forceinline -no-inline-max-size -no-inline-max-total-size -qoverride-limits -no-inline-min-size -no-inline-factor -qopt-report=5
LFLAGS=-I/usr/include -L/usr/lib 


all: opt standard

opt:
	$(C) $(LFLAGS) -c libcirc/utils/matrix.c -o matrix.o $(CFLAGS) $(CFLAGSOPT)
	$(C) $(LFLAGS) -c libcirc/utils/comms.c -o comms.o $(CFLAGS) $(CFLAGSOPT)
	$(C) $(LFLAGS) -c libcirc/stabilizer/stabilizer.c -o stabilizer.o $(CFLAGS) $(CFLAGSOPT)
	$(C) $(LFLAGS) -c libcirc/stateprep.c -o stateprep.o $(CFLAGS) $(CFLAGSOPT)
	$(C) $(LFLAGS) -c libcirc/innerprod.c -o innerprod.o $(CFLAGS) $(CFLAGSOPT)
	$(C) $(LFLAGS) -c libcirc/probability.c -o probability.o $(CFLAGS) $(CFLAGSOPT)
	$(C) $(LFLAGS) matrix.o comms.o stabilizer.o stateprep.o innerprod.o probability.o -o libcirc/mpibackend-opt $(CFLAGS) $(CFLAGSOPT)

standard:
	$(C) $(LFLAGS) -c libcirc/utils/matrix.c -o matrix.o $(CFLAGS)
	$(C) $(LFLAGS) -c libcirc/utils/comms.c -o comms.o $(CFLAGS)
	$(C) $(LFLAGS) -c libcirc/stabilizer/stabilizer.c -o stabilizer.o $(CFLAGS)
	$(C) $(LFLAGS) -c libcirc/stateprep.c -o stateprep.o $(CFLAGS)
	$(C) $(LFLAGS) -c libcirc/innerprod.c -o innerprod.o $(CFLAGS)
	$(C) $(LFLAGS) -c libcirc/probability.c -o probability.o $(CFLAGS)
	$(C) $(LFLAGS) matrix.o comms.o stabilizer.o stateprep.o innerprod.o probability.o -o libcirc/mpibackend $(CFLAGS)


BFLAGS=-lgsl -lgslcblas 

mpibackendblas:
	$(C) $(LFLAGS) -c libcirc/utils/matrix-blas.c -o matrix.o $(CFLAGS) $(BFLAGS)
	$(C) $(LFLAGS) -c libcirc/utils/comms.c -o comms.o $(CFLAGS)
	$(C) $(LFLAGS) -c libcirc/stabilizer/stabilizer.c -o stabilizer.o $(CFLAGS)
	$(C) $(LFLAGS) -c libcirc/stateprep.c -o stateprep.o $(CFLAGS)
	$(C) $(LFLAGS) -c libcirc/innerprod.c -o innerprod.o $(CFLAGS)
	$(C) $(LFLAGS) -D BLAS -c libcirc/probability.c -o probability.o $(CFLAGS)
	$(C) $(LFLAGS) matrix.o comms.o stabilizer.o stateprep.o innerprod.o probability.o -o libcirc/mpibackend $(CFLAGS) $(BFLAGS)

.PHONY: clean distclean
clean:
	rm -f *.o *.optrpt *.pyc

distclean: clean
	rm -rf libcirc/mpibackend* *.log *.out remora_* vtune_* batch_* impi_data.txt
