// input/23 as python
#include <stdio.h>

int main() {
    int a = 0;
    int b = 0, c = 0, d = 0, e = 0, f = 0, g = 0, h = 0;
    
    b = 65; // set b 65
    c = b; // set c b
    // jnz a 2
    // jnz 1 5
    if (a != 0) {
        b *= 100; // mul b 100
        b -= -100000; // sub b -100000
        c = b;  // set c b
        c -= -17000; // sub c -17000
    }

    do {
        printf("outer\n");
        f = 1; // set f 1
        d = 2; // set d 2
        do {
            e = 2; // set e 2
            do {
                g = d; // set g d
                g *= e; // mul g e
                g -= b; // sub g b
                // jnz g 2
                if (g == 0) {
                    f = 0; // set f 0
                }
                e -= -1;    // sub e -1
                g = e;      // set g e
                g -= b;     // sub g b
            } while (g != 0); // jnz g -8
            
            d -= -1; // sub d -1
            g = d; // set g d
            g -= b; // sub g b
        } while (g != 0);     // jnz g -13
        
        if (f == 0) { // jnz f 2
            printf("b: %d\n", b);
            h -= -1; // sub h -1
        }
        g = b; // set g b
        g -= c; // sub g c
        if (g != 0) {
            b -= -17;
        }
    } while (g != 0);
    printf("%d\n", h);
    
    // jnz g 2
    // jnz 1 3
    // sub b -17
    // jnz 1 -23
}
