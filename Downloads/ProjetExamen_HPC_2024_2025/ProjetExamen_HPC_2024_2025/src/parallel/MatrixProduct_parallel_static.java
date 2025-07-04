package parallel;

import schedule.staticSchedule;

public class MatrixProduct_parallel_static {
    private int M, N, P, nbThreads;
    private double[][] A, B, C;

    public MatrixProduct_parallel_static(int M, int N, int P, int nbThreads) {
        this.M = M;
        this.N = N;
        this.P = P;
        this.nbThreads = nbThreads;

        A = new double[M][N];
        B = new double[N][P];
        C = new double[M][P];

        // Initialise matrices à 1 (ou selon besoin)
        for (int i = 0; i < M; i++)
            for (int j = 0; j < N; j++)
                A[i][j] = 1.0;

        for (int i = 0; i < N; i++)
            for (int j = 0; j < P; j++)
                B[i][j] = 1.0;
    }

    public void multiplierMatrice() throws InterruptedException {
        Thread[] threads = new Thread[nbThreads];
        staticSchedule sched = new staticSchedule(0, M - 1, nbThreads);

        for (int t = 0; t < nbThreads; t++) {
            threads[t] = new Thread(() -> {
                schedule.staticSchedule.LoopRange range;
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
    double tempsSeq = 146.589; // À ajuster si ton T_seq est différent
    int[] threadCounts = {2, 4, 6, 8, 10, 12, 20, 30};

    System.out.println("THREADS\tTEMPS(s)\tACCÉLÉRATION");

    for (int nbThreads : threadCounts) {
        MatrixProduct_parallel_static mp = new MatrixProduct_parallel_static(M, N, P, nbThreads);

        long start = System.currentTimeMillis();
        mp.multiplierMatrice();
        long end = System.currentTimeMillis();

        double tempsPar = (end - start) / 1000.0;
        double acceleration = tempsSeq / tempsPar;

        System.out.printf("%d\t%.3f\t\t%.3f\n", nbThreads, tempsPar, acceleration);
    }
}

}
