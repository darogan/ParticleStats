#include <Python.h>
#include <string.h>

/* define maximum x,y coord pairs and percentile for accepting/rejecting data for linear fit */
#define MAXVALS 100
#define PERCENTILE 2

/* define DEBUG to turn on debugging print statements */
//#define DEBUG 

/* function prototypes */
void addvalues(int i, double x[], double y[], double s[]);
void evalabr(int num, double s[], double *a, double *b, double *r);
void initlinRegressFit(void);

/* declare global variables */
double x[MAXVALS];
double y[MAXVALS];
double s[5];
double a, b, r;

/*** input format, description of important variables, compilation etc. ***/

  /* input tuple format: a1, a2, x1, y1, x2, y3, ..., xn, yn                          *
   *   where n (parameter 'num') = number of x, y pairs                               *
   *   NB. a1 and a2 are control arguments:-                                          *
   *        -if a1=a2=0, point selection for fit is dynamic (start at middle 5 pts)   *
   *        -if a1=j, a2=k, then x,y pairs n to m are used for fit                    *
   *           (NB. we count from pair 0, not 1)                                      *
   *  output is the following:-                                                       *
   *    lower and upper index of end point pairs used, 'j' and 'k' (counting from 0)  *
   *    followed by last results: intercept 'a', slope 'b', 'r' and r^2               */

  /* for equation of form y = a + bx, 
   *   - slope 'b' = ( (n * Sxy) - (Sx * Sy) ) / ( (n * Sxx) - (Sx * Sx) )
   *   - intercept 'a' = ( Sy - (b * Sx) ) / n
   *   - Pearson sample correlation coefficient, 
   *      'r' = ( (n * Sxy ) - (Sx * Sy) ) / ( sqrt( n*Sxx - Sx*Sx ) * sqrt( n*Syy - Sy*Sy ) )
   *       use 'rsq' ('r' squared) as criterion for accept/reject (since r can be -ve!)
   * where n is number of x,y pairs ; Sx,Sy are sums over x and y ;   
   *  Sxx,Syy,Sxy are sums of x*x, y*y and x*y respectively
   *
   * parameters, s[0]=Sx, s[1]=Sy, s[2]=Sxx, s[3]=Sxy, s[4]=Syy 
   */

  /* on linux:-  gcc linRegressFit.c -g -I/usr/include/python2.4 -fpic -shared -o linRegressFit.so -lm */
  /* on all platforms:-  python setup.py build ; python setup.py install */


/** this function defines calc method of the object - no prototype seems to be needed ***/
static PyObject *calc(PyObject *self, PyObject *args){

  PyObject *seq;
  double s_last[5]; // to store s values from last regression
  char result[12*((3*(MAXVALS-2))+MAXVALS)];

  int i;
  float a1, a2;
  int mid;
  double a_last, b_last, r_last, rsq;
  int num;
  float f;
  int search_up, search_down;
  int lim_up, lim_low;
  double first_rsq;
  
  /* check that we've been passed a tuple with something in it, then start */
  if(! PyArg_ParseTuple(args, "O", &seq))
    return NULL;
  seq = PySequence_Fast(seq, "Argument not iterable");
  if(!seq){
    return NULL;
  }else{
    /* check input is pairs, get size of input seq and divide by 2 to get num of x,y pairs */
    num = 0;
    num = PySequence_Fast_GET_SIZE(seq);
    if( num % 2 != 0 ){
      return NULL;
    }
    num = (num/2)-1;       // corrected number by -1 for first pair of control args
    /* check we have at least 3 pairs for regression */
    if(num<3){
      return NULL;
    } 

    /* get control args from input seq as int and store in a1 and a2 */
    PyObject *fitem;
    PyObject *item = PySequence_Fast_GET_ITEM(seq,0);
    fitem = PyNumber_Float(item);
    a1 = PyFloat_AS_DOUBLE(fitem);
    item = PySequence_Fast_GET_ITEM(seq,1);
    fitem = PyNumber_Float(item);
    a2 = PyFloat_AS_DOUBLE(fitem);
    #ifdef DEBUG
    printf("control args, a1=%.3f ; a2=%.3f\n", a1, a2);
    #endif

    /* get items from input seq as float and store in x and y arrays */
    for(i=0;i<num;i++){
      PyObject *fitem;
      PyObject *item = PySequence_Fast_GET_ITEM(seq,(2*(i+1)));
      fitem = PyNumber_Float(item);
      x[i] = PyFloat_AS_DOUBLE(fitem);
      item = PySequence_Fast_GET_ITEM(seq,((2*(i+1))+1));
      fitem = PyNumber_Float(item);
      y[i] = PyFloat_AS_DOUBLE(fitem);
    }
    /* zero the arrays of sums for regression and a, b, r variables */
    for(i=0;i<5;i++){
      s[i] = 0;
      s_last[i] = 0;
    }
    a = 0;
    b = 0;
    r = 0;


    /*** check if we are dynamically choosing limits (a1=a2=0) else use specified limits... ***/

    if( (a1==0) && (a2==0) ){

      /* find the middle point and do 1st regression using 5 points about the middle */
      mid = num/2;  // rounds down, so finds mid-point counting from zero...
      #ifdef DEBUG
      printf("num: %d ; mid: %d\n", num, mid);
      #endif
      for(i=mid-2;i<mid+3;i++){
        #ifdef DEBUG
        printf("%d ", i);
        #endif
        addvalues(i, x, y, s);
      }
      evalabr(5, s, &a, &b, &r);
      first_rsq = r*r;  // store 'rsq' from middle 3 pts to use as criterion for accepting/rejecting further x,y pairs
      a_last = a;
      b_last = b;
      r_last = r;
      #ifdef DEBUG
      printf("initial a=%.3f, b=%.3f, r=%.3f, rsq=%.3f\n", a, b, r, first_rsq);
      printf("        Sx=%.3f; Sy=%.3f; Sxx=%.3f; Sxy=%.3f; Syy=%.3f; \n", s[0], s[1], s[2], s[3], s[4]);
      #endif
        
      /* loop to do regression, adding in extra pairs one at a time (first +1, then -1)  *
       *  accept if 'r' is not reduced by more than given factor 'f'                     *
       *  stop searching in a given direction once a point is rejected                   */
      f = (float)(100-PERCENTILE)/100;
      search_up = 1;
      search_down = 1;
      lim_low = mid-2;
      lim_up = mid+2;

      while( (search_up + search_down) > 0 ){
        /* add in an x,y pair upwards from middle after storing last 's' values to come back to in case of rejection */
        if( search_up ){
          for(i=0;i<5;i++){                   // store last 's','a','b','r' values to come back to
            s_last[i] = s[i];
          }
          a_last = a;
          b_last = b;
          r_last = r;
          lim_up += 1;                        // increment upper limit then check < num-1
          if(lim_up>num-1){
            for(i=0;i<5;i++){                 // reset 's' values on reaching upper limit and stop searching up
              s[i] = s_last[i];
            }
            search_up = 0;
            lim_up = lim_up -1;
            break;
          }
          #ifdef DEBUG
          for(i=lim_low;i<lim_up+1;i++){      
            printf("%d ", i);
          }
          #endif
          addvalues(lim_up, x, y, s);         // update 's' values using an extra x,y pair
          evalabr(lim_up-lim_low+1, s, &a, &b, &r);    // calculate a, b, r
          rsq = r*r;
          if( rsq < (f*first_rsq) ){          // check whether 'r' value is significantly reduced on adding in this x,y pair
            #ifdef DEBUG
            printf("reject a=%.3f, b=%.3f, r=%.3f, rsq=%.3f\n", a, b, r, rsq);
            printf("       Sx=%.3f; Sy=%.3f; Sxx=%.3f; Sxy=%.3f; Syy=%.3f; \n", s[0], s[1], s[2], s[3], s[4]);
            #endif
            search_up = 0;
            for(i=0;i<5;i++){                 // reset 's','a','b','r' values and upper limit on rejection and stop searching up
              s[i] = s_last[i];
            }
            a = a_last;
            b = b_last;
            r = r_last;
            lim_up -= 1;
          }else{
            #ifdef DEBUG
            printf("accept a=%.3f, b=%.3f, r=%.3f, rsq=%.3f\n", a, b, r, rsq);
            printf("       Sx=%.3f; Sy=%.3f; Sxx=%.3f; Sxy=%.3f; Syy=%.3f; \n", s[0], s[1], s[2], s[3], s[4]);
            #endif
            ;                                 // empty statement if debug is off
          }
        }
        /* now try adding in an x,y pair downwards from middle (basically the same code) */
        if( search_down ){
          for(i=0;i<5;i++){
            s_last[i] = s[i];
          }
          a_last = a;
          b_last = b;
          r_last = r;
          lim_low -= 1;
          if(lim_low<0){
            for(i=0;i<5;i++){                // reset 's' values on reaching lower limit and stop searching down
              s[i] = s_last[i];
            }
            search_down = 0;
            lim_low = lim_low +1;
            break;
          }
          #ifdef DEBUG
          for(i=lim_low;i<lim_up+1;i++){
            printf("%d ", i);
          }
          #endif
          addvalues(lim_low, x, y, s);  
          evalabr(lim_up-lim_low+1, s, &a, &b, &r);
          rsq = r*r;
          if( rsq < (f*first_rsq) ){
            #ifdef DEBUG
            printf("reject a=%.3f, b=%.3f, r=%.3f, rsq=%.3f\n", a, b, r, rsq);
            printf("       Sx=%.3f; Sy=%.3f; Sxx=%.3f; Sxy=%.3f; Syy=%.3f; \n", s[0], s[1], s[2], s[3], s[4]);
            #endif
            search_down = 0;
            for(i=0;i<5;i++){
              s[i] = s_last[i];
            }
            a = a_last;
            b = b_last;
            r = r_last;
            lim_low += 1;
          }else{
            #ifdef DEBUG
            printf("accept a=%.3f, b=%.3f, r=%.3f, rsq=%.3f\n", a, b, r, rsq);
            printf("       Sx=%.3f; Sy=%.3f; Sxx=%.3f; Sxy=%.3f; Syy=%.3f; \n", s[0], s[1], s[2], s[3], s[4]);
            #endif
            ;
          }
        }
      }
    }else{
      /* using specified lim_low = a1, lim_up = a2 */
      lim_low = (int)a1;
      lim_up = (int)a2;
      for(i=lim_low;i<lim_up+1;i++){
        #ifdef DEBUG
        printf("%d ", i);
        #endif
        addvalues(i, x, y, s);
      }
      evalabr(lim_up-lim_low+1, s, &a, &b, &r);
      #ifdef DEBUG
      printf("using lim_low=%d & lim_up=%d: a=%.3f, b=%.3f, r=%.3f\n", lim_low, lim_up, a, b, r);
      printf("        Sx=%.3f; Sy=%.3f; Sxx=%.3f; Sxy=%.3f; Syy=%.3f; \n", s[0], s[1], s[2], s[3], s[4]);
      #endif
    }
  
    /* make a string of space-separated results:             *
     *  - order is a,b,R for first 3 points ... all n points *
     *  - followed by residuals at end for points 1 to n     */
    result[0] = '\0';
    #ifdef DEBUG
    printf("using lim_low and lim_up values: %d and %d, final results are: a=%.3f, b=%.3f, r=%.3f\n", lim_low, lim_up, a, b, r);
    #endif
    char value[12];
    sprintf(value, "%d ", lim_low);
    strcat(result,value);
    sprintf(value, "%d ", lim_up);
    strcat(result,value);
    sprintf(value, "%8g ", a);
    strcat(result,value);
    sprintf(value, "%8g ", b);
    strcat(result,value);
    sprintf(value, "%8g ", r);
    strcat(result,value);

    return Py_BuildValue("s",result);

  }
}


/*** some Python odds & sods ***/

/* registration table */
static struct PyMethodDef linRegress_methods[]={
  {"calc",calc,1},
  {NULL,NULL}
};

/* module initializer */
void initlinRegressFit(){
  (void) Py_InitModule("linRegressFit",linRegress_methods);
}


/*** normal C functions below ***/

/* add values to Sx, Sy, Sxx, Sxy and Syy */
void addvalues(int i, double x[], double y[], double s[]){
  s[0] = s[0] + x[i];
  s[1] = s[1] + y[i];
  s[2] = s[2] + (x[i] * x[i]);
  s[3] = s[3] + (x[i] * y[i]);
  s[4] = s[4] + (y[i] * y[i]);
}

/* evaluate a, b and r */
void evalabr(int n, double s[], double *a, double *b, double *r){
  //double *lpout = pout;  // copy output pointer 'pout' to 'lpout' for local use (=> we must also increment real pout by +3 later!)
  *b = ((n * s[3]) - (s[0] * s[1])) / ((n * s[2]) - (s[0] * s[0]));
  *a = (s[1] - (*b * s[0]))/n;
  *r = ((n * s[3]) - (s[0] * s[1]));
  *r = *r / ( sqrt((n * s[2]) - (s[0] * s[0])) * sqrt((n * s[4]) - (s[1] * s[1])) );
}

