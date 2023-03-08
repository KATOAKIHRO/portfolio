using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Struct : MonoBehaviour
{

    public struct GameNum
    {
        public bool[] cf;
    }

    void Awake()
    {
        GameNum flag=new GameNum();

        for (int i=0;i<8;i++)
        {
            flag.cf[i] = false;
        }

    }

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
