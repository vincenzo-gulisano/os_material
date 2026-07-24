/* This file contains the code for parser used to parse the input
 * given to shell program. You shouldn't need to modify this
 * file */

#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>
#include "parse.h"

#define PIPE ('|')
#define BG ('&')
#define RIN ('<')
#define RUT ('>')

#define ispipe(c) ((c) == PIPE)
#define isbg(c) ((c) == BG)
#define isrin(c) ((c) == RIN)
#define isrut(c) ((c) == RUT)
#define isspec(c) (ispipe(c) || isbg(c) || isrin(c) || isrut(c))

static Pgm cmdbuf[20], *cmds;
static char cbuf[256], *cp;
static char *pbuf[50], **pp;

int parse(char *buf, Command *c)
{
  int n;
  Pgm *cmd0;

  char *t = buf;
  char *tok;

  init();
  c->rstdin = NULL;
  c->rstdout = NULL;
  c->rstderr = NULL;
  c->background = false;
  c->pgm = NULL;

newcmd:
  if ((n = acmd(t, &cmd0)) <= 0)
  {
    return -1;
  }

  t += n;

  cmd0->next = c->pgm;
  c->pgm = cmd0;

newtoken:
  n = nexttoken(t, &tok);
  if (n == 0)
  {
    return 1;
  }
  t += n;

  switch (*tok)
  {
  case PIPE:
    goto newcmd;
  case BG:
    n = nexttoken(t, &tok);
    if (n == 0)
    {
      c->background = 1;
      return 1;
    }
    else
    {
      fprintf(stderr, "illegal bakgrounding\n");
      return -1;
    }
  case RIN:
    if (c->rstdin != NULL)
    {
      fprintf(stderr, "duplicate redirection of stdin\n");
      return -1;
    }
    if ((n = nexttoken(t, &(c->rstdin))) < 0)
    {
      return -1;
    }
    if (!isidentifier(c->rstdin))
    {
      fprintf(stderr, "Illegal filename: \"%s\"\n", c->rstdin);
      return -1;
    }
    t += n;
    goto newtoken;
  case RUT:
    if (c->rstdout != NULL)
    {
      fprintf(stderr, "duplicate redirection of stdout\n");
      return -1;
    }
    if ((n = nexttoken(t, &(c->rstdout))) < 0)
    {
      return -1;
    }
    if (!isidentifier(c->rstdout))
    {
      fprintf(stderr, "Illegal filename: \"%s\"\n", c->rstdout);
      return -1;
    }
    t += n;
    goto newtoken;
  default:
    return -1;
  }
}

void init(void)
{
  int i;
  for (i = 0; i < 19; i++)
  {
    cmdbuf[i].next = &cmdbuf[i + 1];
  }
  cmdbuf[19].next = NULL;
  cmds = cmdbuf;
  cp = cbuf;
  pp = pbuf;
}

int nexttoken(char *s, char **tok)
{
  char *s0 = s;
  char c;

  *tok = cp;
  while (isspace(c = *s++) && c)
    ;
  if (c == '\0')
  {
    return 0;
  }
  if (isspec(c))
  {
    *cp++ = c;
    *cp++ = '\0';
  }
  else
  {
    *cp++ = c;
    do
    {
      c = *cp++ = *s++;
    } while (!isspace(c) && !isspec(c) && (c != '\0'));
    --s;
    --cp;
    *cp++ = '\0';
  }
  return (int)(s - s0);
}

int acmd(char *s, Pgm **cmd)
{
  char *tok;
  int n, cnt = 0;
  Pgm *cmd0 = cmds;
  cmds = cmds->next;
  cmd0->next = NULL;
  cmd0->pgmlist = pp;

next:
  n = nexttoken(s, &tok);
  if (n == 0 || isspec(*tok))
  {
    *cmd = cmd0;
    *pp++ = NULL;
    return cnt;
  }
  else
  {
    *pp++ = tok;
    cnt += n;
    s += n;
    goto next;
  }
}

#define IDCHARS "_-.,/~+"

int isidentifier(char *s)
{
  while (*s)
  {
    char *p = strrchr(IDCHARS, *s);
    if (!isalnum(*s++) && (p == NULL))
      return 0;
  }
  return 1;
}

/* Print a (linked) list of Pgm:s.
 *
 * Helper function, no need to change. Might be useful to study as inpsiration.
 */
void PrintPgm(Pgm *p)
{
  if (p == NULL)
  {
    return;
  }
  else
  {
    char **pl = p->pgmlist;

    /* The list is in reversed order so print
     * it reversed to get right
     */
    PrintPgm(p->next);
    printf("            * [ ");
    while (*pl)
    {
      printf("%s ", *pl++);
    }
    printf("]\n");
  }
}


/*
 * Print a Command structure as returned by parse on stdout.
 *
 * Helper function, no need to change. Might be useful to study as inpsiration.
 */
void DebugPrintCommand(Command *cmd)
{
  printf("------------------------------\n");
  printf("Parse OK\n");
  printf("stdin:      %s\n", cmd->rstdin ? cmd->rstdin : "<none>");
  printf("stdout:     %s\n", cmd->rstdout ? cmd->rstdout : "<none>");
  printf("background: %s\n", cmd->background ? "true" : "false");
  printf("Pgms:\n");
  PrintPgm(cmd->pgm);
  printf("------------------------------\n");
}
