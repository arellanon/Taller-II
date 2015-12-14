#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
/* Dimensión de la matriz de M X M */
#define M 64                 


int main (int argc, char *argv[]) 
{
int	tid, nthreads, i, j, k, chunk;
double	
	a[M][M],           /* Matriz A*/
	b[M][M],           /* Matriz B*/
	c[M][M];           /* Matriz C*/

chunk = 10;                    /* Cantidad de iteraciones por bloque de iteraciones*/


clock_t begin, end;
double time_spent;
begin = clock();
omp_set_num_threads(0);  //Se establece la cantidad de hilos
#pragma omp parallel shared(a,b,c,nthreads,chunk) private(tid,i,j,k)
  {
  tid = omp_get_thread_num();
  if (tid == 0)
    {
    nthreads = omp_get_num_threads();
    printf("Ejecución con cantidad de hilos = %i",nthreads);
    }
  /* Asigna estáticamenta la cantidad de iteraciones de tamaño chunk */
  #pragma omp for schedule (static, chunk) 
  for (i=0; i<M; i++)
    for (j=0; j<M; j++)
      a[i][j]= i+j;
  #pragma omp for schedule (static, chunk)
  for (i=0; i<M; i++)
    for (j=0; j<M; j++)
      b[i][j]= i*j;
  #pragma omp for schedule (static, chunk)
  for (i=0; i<M; i++)
    for (j=0; j<M; j++)
      c[i][j]= 0;

  printf("El hilo %d comenzó la ejecución de la multiplicación...\n",tid);
  #pragma omp for schedule (static, chunk)
  for (i=0; i<M; i++)    
    {
    printf("Thread=%d calculó la columna = %d\n",tid,i);
    for(j=0; j<M; j++)       
      for (k=0; k<M; k++)
        c[i][j] += a[i][k] * b[k][j];
    }
  }   /* Fin de la región paralela */
  
  end = clock();
time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
printf("El tiempo consumido es: %f", time_spent);

}
