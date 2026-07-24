typedef struct c
{
  char **pgmlist;
  struct c *next;
} Pgm;

typedef struct node
{
  Pgm *pgm;
  char *rstdin;
  char *rstdout;
  char *rstderr;
  int background;
} Command;

extern void init(void);
extern int parse(char *, Command *);
extern int nexttoken(char *, char **);
extern int acmd(char *, Pgm **);
extern int isidentifier(char *);
