/*************************************************************************
¨   FJCOMP Previous version 0.0  - Date: Fevrier 2013*
*   FJCOMP Version 1.0  - updated : Avril 2023     *
*   Ce code est genere et mis en forme par le compilateur FJComp         *
* Auteur du Compilateur: Abdourahmane Senghor  -- boya2senghor@yahoo.fr  *
**************************************************************************/


package fjcomp ;
import java . util . concurrent . ForkJoinPool ;
import java . util . concurrent . RecursiveAction ;
public class Fibonacci {
   public long fibonacci ( int n ) {
      String nbthreadsStr = System . getProperty ( "fjcomp.threads" ) ;
      int numthreads = 2 ;
      try {
         numthreads = Integer . parseInt ( nbthreadsStr ) ;
         if ( numthreads == 0 ) {
            System . out . println ( "La valeur de fjcomp.threads doit etre differente de zero" ) ;
            System . exit ( 1 ) ;
         }
      }
      catch ( Exception ex ) {
         if ( nbthreadsStr == null ) ;
         else {
            System . out . println ( "La valeur fr fjcomp.threads doit etre un entier" ) ;
            System . exit ( 1 ) ;
         }
      }
      ForkJoinPool pool = new ForkJoinPool ( numthreads ) ;
      fibonacciImpl afibonacciImpl = new fibonacciImpl ( 0 , n ) ;
      pool . invoke ( afibonacciImpl ) ;
      return afibonacciImpl . result ;
   }
   private class fibonacciImpl extends RecursiveAction {
      private int maxdepth ;
      private int n ;
      private long result ;
      private fibonacciImpl ( int maxdepth , int n ) {
         this . maxdepth = maxdepth ;
         this . n = n ;
      }
      protected void compute ( ) {
         int MAX_DEPTH ;
         String maxdepthStr = System . getProperty ( "fjcomp.maxdepth" ) ;
         MAX_DEPTH = 20 ;
         try {
            MAX_DEPTH = Integer . parseInt ( maxdepthStr ) ;
            if ( MAX_DEPTH == 0 ) {
               System . out . println ( "La valeur de fjcomp.maxdepth doit etre differente de zero" ) ;
               System . exit ( 1 ) ;
            }
         }
         catch ( Exception ex ) {
            if ( maxdepthStr == null ) ;
            else {
               System . out . println ( "La valeur  fjcomp.maxdepth doit etre un entier" ) ;
               System . exit ( 1 ) ;
            }
         }
         if ( maxdepth >= MAX_DEPTH ) {
            result = fibonacci ( n ) ;
         }
         else {
            if ( n == 0 ) {
               result = 0 ;
            }
            if ( n == 1 ) {
               result = 1 ;
            }
            long x , y ;
            fibonacciImpl task1 = null ;
            fibonacciImpl task2 = null ;
            task1 = new fibonacciImpl ( maxdepth + 1 , n - 1 ) ;
            task2 = new fibonacciImpl ( maxdepth + 1 , n - 2 ) ;
            invokeAll ( task1 , task2 ) ;
            x = task1 . result ;
            y = task2 . result ;
            result = x + y ;
         }
      }
      private long fibonacci ( int n ) {
         if ( n == 0 ) {
            return 0 ;
         }
         if ( n == 1 ) {
            return 1 ;
         }
         long x , y ;
         x = fibonacci ( n - 1 ) ;
         y = fibonacci ( n - 2 ) ;
         return x + y ;
      }
   }
   public static void main(String[] args) {
    final int n = 50;
    final float tempsSeq = 64.4f; // Temps de référence séquentiel

    int[] threadsValues = {2, 4, 6, 8, 10, 12, 20, 30};
    int[] maxDepthValues = { 1, 2, 4, 6, 8, 10, 12, 14, 16, 18};

    System.out.printf("%-10s %-10s %-15s %-15s%n", "Threads", "MaxDepth", "Temps (s)", "Accélération");
    System.out.println("-------------------------------------------------------------");

    for (int maxdepth : maxDepthValues) {
        for (int nthreads : threadsValues) {
            // Définir les propriétés système pour chaque configuration
            System.setProperty("fjcomp.threads", String.valueOf(nthreads));
            System.setProperty("fjcomp.maxdepth", String.valueOf(maxdepth));

            long startTime = System.currentTimeMillis();
            Fibonacci fib = new Fibonacci();
            long resultat = fib.fibonacci(n); // Le résultat est toujours le même
            long stopTime = System.currentTimeMillis();

            float elapsedTime = (float) (stopTime - startTime) / 1000f;
            float acceleration = tempsSeq / elapsedTime;

            // Affichage arrondi à 1 chiffre après la virgule
            System.out.printf("%-10d %-10d %-15.1f %-15.1f%n", nthreads, maxdepth, elapsedTime, acceleration);
        }
    }
}

}
 