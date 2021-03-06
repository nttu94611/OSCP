#include <stdio.h>
//#include <sys/types.h>
//#include <unistd.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: %s PROGRAM\n\n", argv[0]);
        printf("Execute an external PROGRAM with root privileges.\n");
        printf("The %s must be called by root or by a program owned\n", argv[0]);
        printf("by root that has SUID bit set.\n\n");
        return 1;
    }

    printf("Setting UID to 0...\n");
    if (setuid(0))
    {
        perror("setuid");
        return 1;
    }
/*    
    printf("Setting GID to 0...\n");
    if (setgid(0))
    {
        perror("setgid");
        return 1;
    }
*/
    printf("Executing %s...\n", argv[1]);
    system(argv[1]);
    
    return 0;
}
