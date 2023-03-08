using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public static class GameUtil {

	private static KeyCode[] key;

	public static KeyCode[] GetKeyCodeByLineNum (int lineNum) {
		key = new KeyCode[7];
		switch (lineNum) {
			case 0:
				key[0] = KeyCode.Q;
                key[1] = KeyCode.A;
                key[2] = KeyCode.Z;
                return key;
            case 1:
                key[0] = KeyCode.W;
                key[1] = KeyCode.S;
                key[2] = KeyCode.X;
                return key;
            case 2:
                key[0] = KeyCode.E;
                key[1] = KeyCode.D;
                key[2] = KeyCode.C;
                return key;
            case 3:
                key[0] = KeyCode.R;
                key[1] = KeyCode.F;
                key[2] = KeyCode.V;
                key[3] = KeyCode.T;
                key[4] = KeyCode.G;
                key[5] = KeyCode.B;
                return key;
            case 4:
                key[0] = KeyCode.Y;
                key[1] = KeyCode.H;
                key[2] = KeyCode.N;
                key[3] = KeyCode.U;
                key[4] = KeyCode.J;
                key[5] = KeyCode.M;
                return key;
            case 5:
                key[0] = KeyCode.I;
                key[1] = KeyCode.K;
                return key;
            case 6:
                key[0] = KeyCode.O;
                key[1] = KeyCode.L;
                return key;
            case 7:
                key[0] = KeyCode.P;
                key[1] = KeyCode.Minus;
                return key;
            default:
                key[0] = KeyCode.None;
				return key;
		}
	}
}
