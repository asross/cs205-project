#include <stdio.h>
#include <ctime>
#include <stdlib.h>
#include <math.h>
#include <sys/time.h>

int main(int argc, char* argv[])
{
        int niter = 100000000;
        int repetitions = 10;
	double x,y;
        int count=0;
	double z;
	double phi;
	int a = 0;
	time_t t;
	double randomnums[100000000*2];
	double output[100000000];
	srand48(((unsigned)time(&t)));		
	for (a = 0; a<=2*niter; a++)
		randomnums[a] = (double)drand48();
	int i, j;

        for (j = 0; j<repetitions; j++)
        {
            count = 0;
            struct timeval begin, end;
            gettimeofday(&begin, NULL);
	    #pragma acc parallel copy(randomnums[0:100000000*2]) copyout(output[0:100000000]) create(x,y,z) 
	    {
		for (i = 0; i<niter; i++)	
		{
			int temp = i+i;
			x = randomnums[temp];
			y = randomnums[temp+1];
			z = 1/sqrt(2*M_PI) * exp(-.5*pow(x,2));
			output[i] = y/z;
		}
		for (i = 0; i<niter; i++)
		{
			if (output[i]<=1)
			{
				++count;
			}	
			else
				continue;
		}
	    }
          gettimeofday(&end, NULL);
          double elapsed = (end.tv_sec - begin.tv_sec) + ((end.tv_usec - begin.tv_usec)/10000000.0);

	phi = ((double)count/(double)niter)*1.0 + 0.5;		
	printf("OPENACC - area to left of 1 on standard normal: %f\n", phi);
        printf("runtime: %f\n", elapsed);			
        }
}
