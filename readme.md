# Flibusta repacker

Repacks flibusta archives and greatly reduces their size by removing books of certain genres and books marked as deleted in inpx file.

## HOW-TO

Prerequisites - you need to have a folder with zipped flibusta archives and inpx file in the same folder.

1. Get an overview of genre tags:
    ```commandline
    python -m repack -a list_genres
    ```
2. Repack archives by throwing away books of genres you are not interested in:
    ```commandline
    python -m repack -f <path to .inpx file> -a repack --drop_deleted -g <genres to throw away separated by comma>
    ```
   Example:
    ```commandline
    python -m repack -f C:\code\flibusta-repacker\data\flibusta_fb2_local.inpx -a repack --drop_deleted -g sf_action,sf_epic,sf_stimpank,sf_technofantasy,sf_litrpg,popadancy
    ```

NOTE: Python's built-in zip decoder is terribly slow. For frequent usage of this tool you may want to change it to use some external zip decoder.
