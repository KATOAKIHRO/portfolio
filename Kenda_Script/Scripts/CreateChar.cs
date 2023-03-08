using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public static class CreateChar
{
    public static int GetChar(char Alpha)
    {
        switch (Alpha)
        {
            case 'q':
                return 0;
            case 'a':
                return 0;
            case 'z':
                return 0;
            case 'w':
                return 1;
            case 's':
                return 1;
            case 'x':
                return 1;
            case 'e':
                return 2;
            case 'd':
                return 2;
            case 'c':
                return 2;
            case 'r':
                return 3;
            case 'f':
                return 3;
            case 'v':
                return 3;
            case 't':
                return 3;
            case 'g':
                return 3;
            case 'b':
                return 3;
            case 'y':
                return 3;
            case 'h':
                return 4;
            case 'n':
                return 4;
            case 'u':
                return 4;
            case 'j':
                return 4;
            case 'm':
                return 4;
            case 'i':
                return 5;
            case 'k':
                return 5;
            case 'o':
                return 6;
            case 'l':
                return 6;
            case 'p':
                return 2;
            default:
                return 0;
        }
    }
}