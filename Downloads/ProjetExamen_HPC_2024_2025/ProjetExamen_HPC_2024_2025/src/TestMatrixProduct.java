import sequentiel.MatrixProduct_sequentiel;
import parallel.MatrixProduct_parallel_static;
import parallel.MatrixProduct_parallel_self;

public class TestMatrixProduct {

    public static boolean matricesEgales(double[][] A, double[][] B) {
        if (A.length != B.length || A[0].length != B[0].length) return false;
        double tol = 1e-6;
        for (int i = 0; i < A.length; i++) {
            for (int j = 0; j < A[0].length; j++) {
                if (Math.abs(A[i][j] - B[i][j]) > tol) {
                    System.out.println("Différence à (" + i + "," + j + ")");
                    return false;
                }
            }
        }
        return true;
    }

    public static void main(String[] args) throws InterruptedException {
        int M = MatrixProduct_sequentiel.M;
        int N = MatrixProduct_sequentiel.N;
        int P = MatrixProduct_sequentiel.P;
        int nbThreads = 4;

        System.out.println("Dimensions : M=" + M + ", N=" + N + ", P=" + P);

        // Séquentiel
        double[][] A = new double[M][N];
        double[][] B = new double[N][P];
        double[][] C = new double[M][P];
        MatrixProduct_sequentiel seq = new MatrixProduct_sequentiel(A, B, C);
        seq.initialize();
        long startSeq = System.currentTimeMillis();
        seq.multiplierMatrice();
        long endSeq = System.currentTimeMillis();
        System.out.println("Temps séquentiel : " + (endSeq - startSeq) / 1000.0 + " s");

        // Parallèle statique
        MatrixProduct_parallel_static stat = new MatrixProduct_parallel_static(M, N, P, nbThreads);
        long startStat = System.currentTimeMillis();
        stat.multiplierMatrice();
        long endStat = System.currentTimeMillis();
        System.out.println("Temps parallèle statique : " + (endStat - startStat) / 1000.0 + " s");

        // Parallèle self
        MatrixProduct_parallel_self self = new MatrixProduct_parallel_self(M, N, P, nbThreads);
        long startSelf = System.currentTimeMillis();
        self.multiplierMatrice();
        long endSelf = System.currentTimeMillis();
        System.out.println("Temps parallèle self : " + (endSelf - startSelf) / 1000.0 + " s");

        // Comparaison
        System.out.println("Parallèle statique correct ? " + matricesEgales(seq.getResultat(), stat.getResultat()));
        System.out.println("Parallèle self correct ? " + matricesEgales(seq.getResultat(), self.getResultat()));
    }
}
