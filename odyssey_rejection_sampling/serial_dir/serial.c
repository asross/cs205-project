#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <math.h>

void main(int argc, char* argv[])
{
        double niter = atoi(argv[1]); 
        int repeat = 3;
	double x,y;						// these will house random draws from 2d space
	int i, j;
        int count=0;						// count accepted samples
	double z;						// f(x) where f is the standard normal
	double phi;						// cumulative area to left of x
        time_t t;
	srand48(((unsigned)time(&t)));				// a seed value

        for (j=0; j<=repeat; ++j)
            {
            count=0;

        struct timeval begin, end;
        gettimeofday(&begin, NULL);

	    for (i=0; i<=niter; ++i)					// step through each proposed point
	    {
		x = (double)drand48();//RAND_MAX;			// get random x coordinate
		y = (double)drand48();//RAND_MAX;			// get random y coordinate
                z = 1/sqrt(2*M_PI) * exp(-.5*pow(x,2));                 // evaluate f(x)
		if (y<=z)                                               // acceptance check
		{
			++count;	
		}	
	    }	

        gettimeofday(&end, NULL);
        double elapsed = (end.tv_sec - begin.tv_sec) + ((end.tv_usec - begin.tv_usec)/1000000.0);
		
	    phi = ((double)count/(double)niter)*1.0 + 0.5;				
	    printf("SERIAL - area to left of 1 on standard normal: %f\n", phi);			
            printf("runtime: %f\n", elapsed);

        }
}



