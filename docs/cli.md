# CLI 

GitHelp is used from the terminal with the `githelp` command.  
This page shows all available commands, options, and arguments.

For each command, the gray box shows the usage line.

These follow common bash / Unix conventions:
- the `[]` do not get used, they indicate that there might be more than one item in that position
- `[OPTIONS]` refers to any optional inputs or options 
- `[ARGS]` refers to required inputs, or arguments

examples of what usage lines mean:
- `githelp --help` or `githelp -h`
  Run `githelp` with the `--help` or `-h` option to see help.

- `githelp`  
  Run `githelp` with no subcommand. This will show the help text and the GitHelp menu (including available tip pages).

- `githelp list`  
  Run `githelp` with the `list` subcommand. This prints the menu and shows all available tips from `tips.yml`.


- `githelp explain [subcommand]` 
   Use `explain` to see llama2 tips for a specific Git subcommand. 
   For example:
   - `githelp explain status` to see help for `add`.  
   - `githelp explain commit` to see help for `branch`.
   - `githelp explain status` to see help for `checkout`.  
   - `githelp explain commit` to see help for `clone`.
   - `githelp explain status` to see help for `commit`.  
   - `githelp explain commit` to see help for `fetch`.
   - `githelp explain status` to see help for `logs`.  
   - `githelp explain commit` to see help for `pull`.
   - `githelp explain status` to see help for `push`.  
   - `githelp explain commit` to see help for `rebase`.
   - `githelp explain status` to see help for `status`.  
   - `githelp explain commit` to see help for `tag`.
