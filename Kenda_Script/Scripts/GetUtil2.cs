using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public static class GetUtil2
{
    public static string GetKeyCodeAnswer(KeyCode key)
    {
        switch (key)
        {
            case KeyCode.Q:
                return "q";
            case KeyCode.A:
                return "a";
            case KeyCode.Z:
                return "z";
            case KeyCode.W:
                return "w";
            case KeyCode.S:
                return "s";
            case KeyCode.X:
                return "x";
            case KeyCode.E:
                return "e";
            case KeyCode.D:
                return "d";
            case KeyCode.C:
                return "c";
            case KeyCode.R:
                return "r";
            case KeyCode.F:
                return "f";
            case KeyCode.V:
                return "v";
            case KeyCode.T:
                return "t";
            case KeyCode.G:
                return "g";
            case KeyCode.B:
                return "b";
            case KeyCode.Y:
                return "y";
            case KeyCode.H:
                return "h";
            case KeyCode.N:
                return "n";
            case KeyCode.U:
                return "u";
            case KeyCode.J:
                return "j";
            case KeyCode.M:
                return "m";
            case KeyCode.I:
                return "i";
            case KeyCode.K:
                return "k";
            case KeyCode.O:
                return "o";
            case KeyCode.L:
                return "l";
            case KeyCode.P:
                return "p";
            case KeyCode.Minus:
                return "-";
            default:
                return "0";
        }
    }
}
