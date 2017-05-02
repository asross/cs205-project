#include <stdio.h>
#include <stdlib.h>
#include <cuda.h>
#include <curand.h>
#include <sys/time.h>
#include <math.h>

__global__ void kernel(int* count_d, float* randomnums)
{
	int i;
	double x,y,z;
	int tid = blockDim.x * blockIdx.x + threadIdx.x;
	i = tid;
	int xidx = 0, yidx = 0;

	xidx = (i+i);
	yidx = (xidx+1);

	x = randomnums[xidx];
	y = randomnums[yidx];
	z = 1/sqrt(2*M_PI) * exp(-0.5*pow(x,2));

	if (y<=z)
		count_d[tid] = 1;
	else
		count_d[tid] = 0;	
}

void CUDAErrorCheck()
{
	cudaError_t error = cudaGetLastError();
	if (error != cudaSuccess)
	{	
		printf("CUDA error : %s (%d)\n", cudaGetErrorString(error), error);
		exit(0);
	}
}

int main(int argc,char* argv[])
{
	int niter = atoi(argv[1]);
        int repetitions = 3;
        int j = 0;

        for (j=0; j<repetitions; j++) 
        {
	   float *randomnums;
	   double phi;
	   cudaMalloc((void**)&randomnums, (2*niter)*sizeof(float));
	   // Use CuRand to generate an array of random numbers on the device
	   int status;
	   curandGenerator_t gen;
	   status = curandCreateGenerator(&gen, CURAND_RNG_PSEUDO_MRG32K3A);
	   status |= curandSetPseudoRandomGeneratorSeed(gen, 2138+j);
	   // status |= curandSetPseudoRandomGeneratorSeed(gen, 4294967296ULL^time(NULL));
	   status |= curandGenerateUniform(gen, randomnums, (2*niter));
	   status |= curandDestroyGenerator(gen);
	   if (status != CURAND_STATUS_SUCCESS)
	   {
		printf("CuRand Failure\n");
		exit(EXIT_FAILURE);
	   }

	   int threads = 1000;
	   int blocks = 100;
	   int* count_d;
	   int *count = (int*)malloc(blocks*threads*sizeof(int));
	   unsigned int reducedcount = 0;
	   cudaMalloc((void**)&count_d, (blocks*threads)*sizeof(int));
	   CUDAErrorCheck();

struct timeval begin, end;
gettimeofday(&begin, NULL);

           cudaEvent_t start, stop;
           cudaEventCreate(&start);
           cudaEventCreate(&stop);
           cudaEventRecord(start, 0); 
	   //one point per thread
	   kernel <<<blocks, threads>>> (count_d, randomnums);
	   cudaDeviceSynchronize();
	   CUDAErrorCheck();
	   cudaMemcpy(count, count_d, blocks*threads*sizeof(int), cudaMemcpyDeviceToHost);
	   int i = 0;
	   //reduce array into int
	   for(i = 0; i<niter; i++)
		reducedcount += count[i];
           cudaEventRecord(stop, 0); 
           float elapsedTime = 0;
           cudaEventElapsedTime(&elapsedTime, start, stop);

gettimeofday(&end, NULL);
double elapsed = (end.tv_sec - begin.tv_sec) + ((end.tv_usec - begin.tv_usec)/1000000.0);

	   cudaFree(randomnums);
	   cudaFree(count_d);
	   free(count);
           cudaEventDestroy(start);
           cudaEventDestroy(stop);

	   phi = ((double)reducedcount/niter)*1.0 + 0.5;
	   printf("CUDA - area to left of 1 on standard normal: %f\n", phi);
           //printf("runtime: %f\n", elapsedTime);
           printf("runtime: %f\n", elapsed);
           //printf("runtime: %f\n", seconds);
       }
  
       return 0;
        
}
