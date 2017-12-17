#include <stdio.h>
#include <stdlib.h>

struct item_t {
    struct item_t *next;
    int v;
};

void spinlock(int step, int n) {
    struct item_t *heap;
    int next_free = 0;

    int i, j;
    struct item_t *p, *tmp;
    struct item_t *item, *init;

    heap = malloc(n * sizeof(struct item_t));

    p = &heap[next_free++];
    p->v = 0;
    p->next = p; // cirular list

    for (i = 0; i < n; i++) {
        for (j = 0; j < step; j++) {
            p = p->next;
        }
        
        // insert i+1 after p
        tmp = &heap[next_free++];
        tmp->next = p->next;
        tmp->v = i + 1;
        p->next = tmp;

        // move ahead
        p = tmp;

        if (i % 1024 == 0) {
            printf("\r%d", 100 * i / n);
        }
    }

    printf("%d\n", p->next->v);    
    
    for (item = &heap[0]; item->next != &heap[0]; item = item->next) {
        //printf("v: %d\n", item->v);
        if (item->v == 0) {
            printf("%d\n", item->next->v);
        }
    }

    free(heap);
}

int main() {
    int p, i;
    struct item_t *item;
    struct item_t *init;
    
    //spinlock(3, 2017);
    spinlock(382, 50000000);
}