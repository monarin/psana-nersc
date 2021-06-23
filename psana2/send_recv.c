// Author: Wes Kendall
// Copyright 2011 www.mpitutorial.com
// This code is provided freely with the tutorials on mpitutorial.com. Feel
// free to modify it for your own use. Any distribution of the code must
// either provide a link to www.mpitutorial.com or keep this header intact.
//
// MPI_Send, MPI_Recv example. Communicates the number -1 from process 0
// to process 1.
//
#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>                // for gettimeofday()


int main(int argc, char** argv) {
  // Initialize the MPI environment
  MPI_Init(NULL, NULL);
  // Find out rank, size
  int world_rank;
  MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
  int world_size;
  MPI_Comm_size(MPI_COMM_WORLD, &world_size);

  // We are assuming at least 2 processes for this task
  if (world_size < 2) {
    fprintf(stderr, "World size must be greater than 1 for %s\n", argv[0]);
    MPI_Abort(MPI_COMM_WORLD, 1);
  }

  // Set timing
  struct timeval t1, t2;
  double elapsedTime;

  // Prepare data
  int datasize = atoi(argv[1]);
  int *data[datasize];

  if (world_rank == 0) {
    // start timer
    gettimeofday(&t1, NULL);
    
    // If we are rank 0, set the number to -1 and send it to process 1
    MPI_Send(
      /* data         = */ data, 
      /* count        = */ datasize, 
      /* datatype     = */ MPI_INT, 
      /* destination  = */ 1, 
      /* tag          = */ 0, 
      /* communicator = */ MPI_COMM_WORLD);
    
    // stop timer
    gettimeofday(&t2, NULL);
    // compute and print the elapsed time in millisec
    elapsedTime = (t2.tv_sec - t1.tv_sec) * 1000.0;      // sec to ms
    elapsedTime += (t2.tv_usec - t1.tv_usec) / 1000.0;   // us to ms
    printf("%f ms.\n", elapsedTime);
  
  } else if (world_rank == 1) {
    MPI_Recv(
      /* data         = */ data, 
      /* count        = */ datasize, 
      /* datatype     = */ MPI_INT, 
      /* source       = */ 0, 
      /* tag          = */ 0, 
      /* communicator = */ MPI_COMM_WORLD, 
      /* status       = */ MPI_STATUS_IGNORE);
    printf("Process 1 received %d BYTE from process 0\n", datasize*sizeof(int));
  }
  MPI_Finalize();
}
