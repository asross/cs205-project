#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <math.h>
#include <time.h>

int main(int argc, char* argv[])
{
	int repeat = 3;
	double x,y;						
	int i, j;					
        int count=0;					
	double z;							
	double phi;							// area to left of 1 in standard normal
	int numthreads = atoi(argv[2]);
	int niter = atoi(argv[1])/numthreads;			
        //time_t t0, t1;
        //double t0, t1, tdiff; 

	for (j=0; j<=repeat; ++j)
        { 
        count = 0;
        struct timeval begin, end;
        gettimeofday(&begin, NULL);

	#pragma omp parallel firstprivate(x, y, z, i) reduction(+:count) num_threads(numthreads)
	{
		srand48((int)time(NULL) ^ omp_get_thread_num());	
		for (i=0; i<niter; ++i)					
		{
			x = (double)drand48();				
			y = (double)drand48();				
			z = 1/sqrt(2*M_PI) * exp(-.5*pow(x,2));		
			if (y<=z)
			{
				++count;					
			}		
		}
	} 

        gettimeofday(&end, NULL);
        double elapsed = (end.tv_sec - begin.tv_sec) + ((end.tv_usec - begin.tv_usec)/1000000.0);

	phi = ((double)count/(double)(niter*numthreads))*1.0 + 0.5;
	printf("OPENMP - area to left of 1 on standard normal: %f\n", phi);
	printf("runtime: %f\n", elapsed);
	}
	return 0;
}
