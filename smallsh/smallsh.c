#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <stdbool.h>
#include <signal.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <errno.h>
#include <stdlib.h>
#include <fcntl.h>
#include <time.h>

#define MAX_SIZE_CHAR 2048
#define MAX_SIZE_ARG 512

/*
Initiate the function names for the program, this could also be done when they are called, but I find this easier
*/
void smallsh();
void exit_cmd();
void get_exit_status(int);
void execute_other(char *[], int *, char[], char[], int *, struct sigaction);
char *expand(char *s, char *, char *);
void handle_SIGTSTP();
int background_toggle = 1; // 1 = on, 0 = off

int main()

{
    /*Program runs main, main calls the shell function*/
    smallsh();
    return 0;
}

void smallsh()
{
    int terminating_signal = 0; // must be outside of the while loop to keep track of exit status of last command
    /*
    This is the shell function that will prompt users for commands and decide what to do from there, I intended
    to write several helper functions when I started, but as I wrote the code I decided to keep it mostly in smallsh.
    I might be able to improve readability by separating the loop into separate helper functions, but
    in the interest of time, I decided to not risk breaking it.
    */
    while (1)
    {
        // this is from the exploration on signals
        // IGNORE SIGINT
        struct sigaction SIGINT_action = {0};
        SIGINT_action.sa_handler = SIG_IGN;
        sigfillset(&SIGINT_action.sa_mask);
        SIGINT_action.sa_flags = 0;
        sigaction(SIGINT, &SIGINT_action, NULL);

        // HANDLE SIGTSTP
        struct sigaction SIGTSTP_action = {0};
        SIGTSTP_action.sa_handler = handle_SIGTSTP;
        sigfillset(&SIGTSTP_action.sa_mask);
        SIGTSTP_action.sa_flags = 0;
        sigaction(SIGTSTP, &SIGTSTP_action, NULL);

        // prompt user for input
        printf(": ");
        fflush(stdout);

        // read in user input
        char input[MAX_SIZE_CHAR];
        fgets(input, MAX_SIZE_CHAR, stdin); // fgets used so we can dictate the size of the input
        strtok(input, "\n");                // strips the newline from the user hitting enter

        // parse input
        char *token;
        char *args[MAX_SIZE_ARG];
        int i = 0;
        char expand_me[] = "$$";  // passed to the expander function
        char source_FD[512] = ""; // stores the source file descriptor
        char target_FD[512] = ""; // stores the target file descriptor
        token = strtok(input, " "); // delimiter for the input is a space
        char pid[10];              // stores the pid of the shell which is passed to expander function
        sprintf(pid, "%d", getpid()); // converts the pid to a string
        int behind_the_scenes = 0; // this is used to determine if the command is to be run in the background
        while (token != NULL)
        {

            if (strcmp(token, "<") == 0) // read in
            {
                token = strtok(NULL, " ");
                // printf("read in\n");                 //debugging
                // fflush(stdout);
                strcpy(source_FD, token);
            }
            else if (strcmp(token, ">") == 0) // write out
            {
                token = strtok(NULL, " ");
                // printf("write out\n");  //debugging
                // fflush(stdout);
                strcpy(target_FD, token);
                // printf("%s\n", target_FD); //debugging
            }
            else
            {
                char* result = expand(token, expand_me, pid); // this expands the $$ by calling the expand function, 
                //it must be done before the token is added to the args array
                args[i] = result;
                i++;
            }
            token = strtok(NULL, " ");
        }

        // make last argument NULL
        args[i] = NULL;

        /*
        At this point in the program, we have read in the user input and populated our file descriptors (for O/I) and args array which is used 
        to execute the command. 
        */
        
        // check for & at the end of the command and then strip it or you get weird functionality with some functions
        if (strcmp(args[i-1], "&") == 0)
        {
            behind_the_scenes = 1;
            args[i-1] = NULL;
        }

        // check for comments
        if (args[0][0] == '#')
        {
            // printf("registered the # as separate command");     //debugging
            continue;
        }

        // check for blank lines
        else if (args[0][0] == '\n')
        {
            // printf("registered the newline as separate command");      //debugging
            continue;
        }

        // check for exit command
        else if (strcmp(args[0], "exit") == 0)
        {
            printf("exiting shell");
            fflush(stdout);
            exit_cmd();
        }

        // check for cd
        else if (strcmp(args[0], "cd") == 0)
        {
            if (args[1] == NULL)
            {
                chdir(getenv("HOME"));     // home is used from the environment variable as shown in the exploration
            }
            else
            {
                if (chdir(args[1]) == -1)
                {
                    printf("cd %s: No such file or directory\n", args[1]);  //mimics bash error message
                    fflush(stdout);
                };
                /*
                printf("changed directory to %s\n", args[1]);         //debugging
                char cwd[256];
                getcwd(cwd, sizeof(cwd));
                printf("current working directory is %s\n", cwd);
                */
            }
        }

        // check for status
        else if (strcmp(args[0], "status") == 0)
        {
            get_exit_status(terminating_signal);         // passes the previous terminating signal to the exit status function for printing
        }
        // Other commands that aren't built in
        else
        {
            /*
            args is the array of args, &terminating signal is the value of the exit status, source_FD is the source file descriptor,
            target_FD is the target file descriptor, &behind_the_scenes is the value of the background toggle, and SIGINT is the struct 
            for the behavior of SIGINT
            */
            
            execute_other(args, &terminating_signal, source_FD, target_FD, &behind_the_scenes, SIGINT_action);
        }
    }
}

void exit_cmd()
{
    exit(0);
}
void get_exit_status(int signal)
{ // check to see what the value of the exit status was for the last process
    if (WIFEXITED(signal))
    {
        printf("exit value %d\n", WEXITSTATUS(signal));
        fflush(stdout);
    }
    // if the process was terminated by a signal
    else
    {
        printf("terminated by signal %d\n", WTERMSIG(signal));
        fflush(stdout);
    }
}
void execute_other(char *args_vector[], int *child_signal, char read_in[], char write_out[], int *background, struct sigaction handler)
{ // this function will execute other commands that aren't built in like ls, echo, etc.
    // code inspired by exploration on forking
    pid_t spawnPid = -5;
    int childPid;
    spawnPid = fork();
    switch (spawnPid)
    {
    case -1:
    {
        perror("fork() failed\n");
        exit(1);
        break;
    }
    case 0:
    {   // child process
        handler.sa_handler = SIG_DFL; // changes the ctrl c handler to default for the children process
        sigaction(SIGINT, &handler, NULL);

        /*
        "First you hand the redirection to "junk" with dup(2) and then simply pass ls into exec()""
        this is why the O/I file redirections come before the execvp in the child process

        The redirect for O/I is from the exploration on file redirection
        */

        // Open source file
        if (strcmp(read_in, "")) // TODO: figure out why != doesn't work
        {
            int source_check = open(read_in, O_RDONLY);
            if (source_check == -1)
            {
                perror("source open()");
                exit(1);
            }
            // Redirect stdin to source file
            int source_dup = dup2(source_check, 0);
            if (source_dup == -1)
            {
                perror("source dup2()");
                exit(2);
            }
            // close the file
            fcntl(source_check, F_SETFD, FD_CLOEXEC);
        }

        // Open target file
        if (strcmp(write_out, ""))
        {
            int target_check = open(write_out, O_WRONLY | O_CREAT | O_TRUNC, 0644);
            if (target_check == -1)
            {
                perror("target open()");
                exit(1);
            }
            // Redirect stdout to target file
            int target_dup = dup2(target_check, 1);
            if (target_dup == -1)
            {
                perror("target dup2()");
                exit(2);
            }
            // close the file
            fcntl(target_check, F_SETFD, FD_CLOEXEC);
        }
        // printf("executing %s\n", args[0]);
        execvp(args_vector[0], args_vector); // execute the commands using v(vector)p(process)
        perror("execvp");
        exit(2);
        fflush(stdout);
        break;
    }
    default:
    {
        // parent process
        /*
         The WNOHANG allows processes to run in the background so we only want to use this part if background
         process are allowed
        */
        if (*background == 1 && background_toggle == 1)
        {
            pid_t childPid = waitpid(spawnPid, child_signal, WNOHANG);
            printf("background pid is %d\n", spawnPid);
            fflush(stdout);
        }
        // no background processes are allowed, or the process is intended to run in foreground
        else
        {
            pid_t childPid = waitpid(spawnPid, child_signal, 0);
        }
    }
    }
    // "your parent shell will need to periodically check for background child process to complete"
    
    while ((childPid = waitpid(-1, child_signal, WNOHANG)) > 0)
    {
        printf("background pid %d is done: ", childPid);
        fflush(stdout);
        get_exit_status(*child_signal);
    }
}

char *expand(char *arg, char *expander, char *process_ID)
{
  

    char *result;
    int i = 0;
    int count = 0;
    int process_ID_len = strlen(process_ID);
    int expander_len = strlen(expander);

    // Determine how much memory we need to allocate for the result string
    for (i = 0; arg[i] != '\0'; i++)
    {
        /*
        strstr is a needle and haystack function where arg is the haystack
        and expander is the needle. If the needle is found in the haystack, it
        increases the count variable by 1.
        */
        if (strstr(&arg[i], expander) == &arg[i])
        {
            count++;
            i += expander_len - 1;
        }
    }

    // Dynamic memory allocation for the new string
    result = (char *)malloc(i + count * (process_ID_len - expander_len) + 1);

    i = 0;
    while (*arg)
    {
        /*
        strstr here is used to find the instance of the expander in the arg and
        then we copy the process_ID into the result string. The increments are
        to update the place in memory that we are reading and writing to.
        */

        if (strstr(arg, expander) == arg)
        {
            strcpy(&result[i], process_ID);
            i += process_ID_len;
            arg += expander_len;
        }
        else
            result[i++] = *arg++;
    }
    // strings must end in a null terminator
    result[i] = '\0';
    return result;
}

void handle_SIGTSTP()
{
    /*
    this function will handle the SIGTSTP signal which is setup in the struct for SIGTSTP
    it is a simple toggle mechanism that displays a print message, however because of reentrancy,
    we cannot use printf so we write to STDOUT filestream instead. I dont think the fflush does anything here,
    because in testing it will sometimes print the message twice, but I left it in just in case.
    */

    if (background_toggle == 1)
    {
        background_toggle = 0;
        char *message = "\nEntering foreground-only mode (& is now ignored)\n";
        write(STDOUT_FILENO, message, 50);
        fflush(stdout);
    }
    else
    {
        background_toggle = 1;
        char *message = "\nExiting foreground-only mode\n";
        write(STDOUT_FILENO, message, 30);
        fflush(stdout);
    }
}


/*
TODO: doesn't print the error message when interrupted by a signal. Solution could be to make a handler for SIGINT and
      then call the function in the handler. The function would display the error message and then return to the main loop.

TODO: The blank line and comment don't trigger the completed message for a background message because they are checked too early in the loop
      I think the solution is to move the check for blank line and comment to after the check for background process. This would require
      a complete restructuring of my code because of how the variables are used. 
    */


