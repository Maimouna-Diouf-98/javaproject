package parallel;

import schedule.selfSchedule;

public class MatrixProduct_parallel_self {
    private int M, N, P, nbThreads;
    private double[][] A, B, C;
    private int groupSize;

    public MatrixProduct_parallel_self(int M, int N, int P, int nbThreads, int groupSize) {
        this.M = M;
        this.N = N;
        this.P = P;
        this.nbThreads = nbThreads;
        this.groupSize = groupSize;

        A = new double[M][N];
        B = new double[N][P];
        C = new double[M][P];

        for (int i = 0; i < M; i++)
            for (int j = 0; j < N; j++)
                A[i][j] = 1.0;

        for (int i = 0; i < N; i++)
            for (int j = 0; j < P; j++)
                B[i][j] = 1.0;
    }

    public void multiplierMatrice() throws InterruptedException {
        Thread[] threads = new Thread[nbThreads];
        selfSchedule sched = new selfSchedule(0, M - 1, groupSize);

        for (int t = 0; t < nbThreads; t++) {
            threads[t] = new Thread(() -> {
                schedule.selfSchedule.LoopRange range;
                while ((range = sched.loopGetRange()) != null) {
                    for (int i = range.start; i <= range.end; i++) {
                        for (int j = 0; j < P; j++) {
                            double sum = 0;
                            for (int k = 0; k < N; k++) {
                                sum += A[i][k] * B[k][j];
                            }
                            C[i][j] = sum;
                        }
                    }
                }
            });
            threads[t].start();
        }

        for (Thread t : threads) {
            t.join();
        }
    }

    public double[][] getResultat() {
        return C;
    }

    public static void main(String[] args) throws InterruptedException {
        int M = 4096, N = 2048, P = 2048;
        double T_seq = 146.6;

        int[] threadCounts = {2, 4, 6, 8, 10, 12, 20, 30};
        int[] groupSizes = {8, 64, 128, 256, 512, 1024, 2048};

        System.out.println("GroupSize,Threads,Temps(s),Accélération");

        for (int groupSize : groupSizes) {
            for (int nbThreads : threadCounts) {
                MatrixProduct_parallel_self mp = new MatrixProduct_parallel_self(M, N, P, nbThreads, groupSize);

                long start = System.currentTimeMillis();
                mp.multiplierMatrice();
                long end = System.currentTimeMillis();

                double tempsPar = (end - start) / 1000.0;
                double acceleration = T_seq / tempsPar;

                System.out.printf("%d,%d,%.1f,%.1f\n", groupSize, nbThreads, tempsPar, acceleration);
            }
        }
    }
}
