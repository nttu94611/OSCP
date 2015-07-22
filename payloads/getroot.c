// Must be executed by root or by a program owned by root with suid bit set
int main(void) {
    if (setuid(0)) {
        perror("setuid");
        return 1;
    }
    system("/bin/bash");
    return 0;
}
