using UnityEngine;
using System.IO;
using System;
using System.Text;
using UnityEngine.UI;
using TMPro;
using UnityEditor.Experimental.GraphView;
using System.Collections;
using System.Collections.Generic;


/*
using System.Collections;
using UnityEngine.Analytics;
using static UnityEngine.GraphicsBuffer;
using Newtonsoft.Json.Linq;
using UnityEngine.XR;
using UnityEngine.UIElements;
*/

public class GameController : MonoBehaviour
{
    [SerializeField] private TextMeshProUGUI textRoman;
    [SerializeField] AudioClip[] audioClips;

    public int fileNum;
    private string filePassT;
    public string filePassC;
    public string filePassA;
    private string filePassL;
    public string[] filePassIndex;

    private double[] _lineNumTag;
    private int[] _lineNumCon;
    private int[] _lineNumAlp;
    private double[] _lineNumLyr;
    private int _LineLength;
    private string[] _lineStrCon;
    private string[] _lineStrConA;
    private int[] _linetextNum;
    private int[] _linescoreNum;
    private char[] _lineStrAlp;
    private string[] _lineStrLyr;
    private List<char> _lineChar;

    public Text[] text;
    public TextMeshProUGUI lyricsText;
    private int lyricsNum = 0;
    private int RomanIndex = 0;

    public AudioSource audioSource;
    private float _soundLength = 0;

    private float _startTime = 0;
    private double _timeCoef = 0;
    
    public float timeOffset = -1;
    private bool _isPlaying = false;
    public GameObject startButton;
    public TextMeshProUGUI scoreText;
    public TextMeshProUGUI scoreText2;
    public TextMeshProUGUI scoreText3;
    private int _scoreBAD = 0;
    private int _scoreGOOD = 0;
    private int _scoreMISS = 0;
    private int _scoreAll = 0;
    private float _scoreGAGE = 0;

    private StreamWriter sw;
    private int[] write;
    public GameObject canvas;
    public enum ChatColor : uint
    {
        RED = 0xFF0000FF,
        GRN = 0x00FF00FF,
        BLR = 0x0000FFFF,
        BLK = 0x000000FF,
        GRY = 0x00000066
    }



    void Awake()
    {
        Application.targetFrameRate = 30;
        audioSource = GameObject.Find("GameMusic").GetComponent<AudioSource>();
        _lineChar = new List<char>();
        _lineNumTag = new double[1000];
        _lineStrCon = new string[1000];
        _lineStrConA = new string[1000];
        _lineNumCon = new int[1000];
        _linetextNum = new int[1000];
        _linescoreNum = new int[1000];
        _lineStrAlp = new char[1000];
        _lineNumAlp = new int[1000];
        _lineStrLyr = new string[1000];
        _lineNumLyr = new double[1000];
        write = new int[1000];

        filePassIndex = new string[]
        {   "Assets\\MusicEffectPack\\Resources\\Expansion\\convert.csv",
            "Assets\\MusicEffectPack\\Resources\\Expansion\\alphabet_convert.csv",
            "Assets\\MusicEffectPack\\Resources\\Expansion\\SelectSource\\tag.csv",
        };

        string str = fileNum.ToString();

        filePassC = filePassIndex[0];
        filePassA = filePassIndex[1];
        filePassT = filePassIndex[2];
        filePassL = "Assets\\MusicEffectPack\\Resources\\Expansion\\PlaySource\\M" + fileNum + "\\lyrics.csv";
        audioSource.clip = audioClips[fileNum - 1];
        _soundLength = audioSource.clip.length;
    }

    void Start()
    {
        Time.timeScale = 1;
        LoadCSV_Convert();//convert
        LoadCSV_Lyrics();//lyrics
        LoadCSV_TagBPM();//BPM of tag
        KanaToRomanToAlpha(_lineStrLyr);
        Invoke("StartGame", 5.0f);
    }

    private void OnGUI()
    {
        if (Event.current.type == EventType.KeyDown)
        {
            switch (InputKey(GetCharFromKeyCode(Event.current.keyCode)))
            {
                case 1: // 正解タイプ時
                    _scoreGOOD++;
                    RomanIndex++;
                    SliderUpdate();
                    break;
                case 2: // 誤りタイプ時
                    _scoreBAD++;
                    break;
            }
        }
    }
    void Update()
    {
        if (_isPlaying)
        {
            scoreText.text = $"BAD:{_scoreBAD.ToString()}";
            scoreText2.text = $"GOOD:{_scoreGOOD.ToString()}";
            scoreText3.text = $"MISS:{_scoreMISS.ToString()}";
            LyricsUpdate();
            textRoman.text = GenerateTextRoman();
            GameStopMenu();
            if (audioSource.time == _soundLength)
            {
                SceneFinish();
            }

        }
    }

    public void StartGame()
    {
        _startTime = Time.time;
        audioSource.Play();
        //OutputData1(true);
        _isPlaying = true;
    }

    void LyricsUpdate()
    {
        if (GetMusicTime() > _lineNumLyr[lyricsNum] * _timeCoef / 4 && _lineNumLyr[lyricsNum] != 0)
        {
            while (_lineChar[RomanIndex] != '@')
            {
                RomanIndex++;
                _scoreMISS++;
            }
            RomanIndex++;

            lyricscolor(_lineStrLyr[lyricsNum]);
            lyricsNum++;

        }
    }


    void lyricscolor(string str)
    {
        lyricsText.text = "";

        for (int i = 0; i < str.Length; i++)
        {
            lyricsText.text = lyricsText.text + $"{str[i]}";
        }

    }


    void LoadCSV_Convert()
    {
        int i = 0, j;
        TextAsset csv = Resources.Load(filePassC) as TextAsset;
        using (StreamReader reader = new StreamReader(filePassC, Encoding.GetEncoding("Shift_JIS")))
            while (reader.Peek() > -1)
            {

                string line = reader.ReadLine();
                string[] values = line.Split(',');
                for (j = 0; j < values.Length; j++)
                {
                    _lineStrCon[i] = values[0];
                    _lineStrConA[i] = values[2];

                }
                i++;
            }
    }


    void LoadCSV_Lyrics()
    {
        int i = 0, j;
        TextAsset csv = Resources.Load(filePassL) as TextAsset;
        using (StreamReader reader = new StreamReader(filePassL, Encoding.GetEncoding("Shift_JIS")))
            while (reader.Peek() > -1)
            {

                string line = reader.ReadLine();
                string[] values = line.Split(',');
                for (j = 0; j < values.Length; j++)
                {
                    _lineNumLyr[i] = double.Parse(values[0]);
                    _lineStrLyr[i] = values[1];
                }
                i++;
            }
    }
    void LoadCSV_TagBPM()
    {
        int i = 0, j;
        TextAsset csv = Resources.Load(filePassT) as TextAsset;
        using (StreamReader reader = new StreamReader(filePassT, Encoding.GetEncoding("Shift_JIS")))
            while (reader.Peek() > -1)
            {

                string line = reader.ReadLine();
                string[] values = line.Split(',');
                for (j = 0; j < values.Length; j++)
                {
                    _lineNumTag[i] = double.Parse(values[1]);
                }
                i++;
            }
        _timeCoef = 60 / _lineNumTag[fileNum - 1]; //method(=60/BPM)
    }

    void KanaToRomanToAlpha(string[] str)
    {
        int h, i, j;
        string sentence;
        string mozi;
        int pai;
        _lineChar.Add('@');
        for (h = 0; h < str.Length; h++)
        {
            sentence = str[h];
            i = 0;
            if (sentence == null)
            {
                break;
            }
            while (i < sentence.Length)
            {
                pai = Array.IndexOf(_lineStrCon, sentence[i].ToString());
                if (pai == -1)
                {
                    if (sentence[i] == 'っ')
                    {
                        pai = Array.IndexOf(_lineStrCon, sentence[i].ToString() + sentence[i + 1].ToString());
                        i++;
                    }
                    else
                    {
                        pai = Array.IndexOf(_lineStrCon, sentence[i - 1].ToString() + sentence[i].ToString());
                        _lineChar.RemoveAt(_lineChar.Count - 1);
                        _lineChar.RemoveAt(_lineChar.Count - 1);
                    }

                }
                mozi = _lineStrConA[pai];
                for (j = 0; j < mozi.Length; j++)
                {
                    _lineChar.Add(mozi[j]);
                    _scoreAll++;

                }
                i++;

            }
            _lineChar.Add('@');
        }
    }

    float GetMusicTime()
    {
        return (Time.time - _startTime);
    }

    void OutputData1(bool flag)//LOG
    {
        sw = new StreamWriter(@"OutputData1.csv", true, Encoding.GetEncoding("Shift_JIS"));

        if (flag)
        {
            sw.WriteLine("開始" + System.DateTime.Now.ToString());
        }
        else
            sw.WriteLine("終了" + System.DateTime.Now.ToString());
        sw.Close();
    }

    void OutputData2(int num)//RESULT
    {
        sw = new StreamWriter(@"OutputData2.csv", true, Encoding.GetEncoding("Shift_JIS"));
        sw.WriteLine(num);
        sw.Close();
    }
    void SceneFinish()
    {
        //OutputData1(false);
        //OutputData2(unci)
        UnityEditor.EditorApplication.isPlaying = false;//Change Me!!!
    }

    string GenerateTextRoman()//[memo]fixing now
    {
        string text = "<style=typed>";
        for (int i = RomanIndex; i < _lineChar.Count; i++)
        {
            if (_lineChar[i] == '@')
            {
                break;
            }

            if (i == RomanIndex)
            {
                text += "</style><style=untyped>";
            }

            text += _lineChar[i];
        }

        text += "</style>";

        return text;
    }

    int InputKey(char inputChar)
    {
        if (inputChar == '\0' || _lineChar[RomanIndex] == '@')
        {
            return 0;
        }

        if (inputChar == _lineChar[RomanIndex])
        {
            return 1;
        }

        return 2;
    }

    char GetCharFromKeyCode(KeyCode keyCode)
    {
        switch (keyCode)
        {
            case KeyCode.A:
                return 'a';
            case KeyCode.B:
                return 'b';
            case KeyCode.C:
                return 'c';
            case KeyCode.D:
                return 'd';
            case KeyCode.E:
                return 'e';
            case KeyCode.F:
                return 'f';
            case KeyCode.G:
                return 'g';
            case KeyCode.H:
                return 'h';
            case KeyCode.I:
                return 'i';
            case KeyCode.J:
                return 'j';
            case KeyCode.K:
                return 'k';
            case KeyCode.L:
                return 'l';
            case KeyCode.M:
                return 'm';
            case KeyCode.N:
                return 'n';
            case KeyCode.O:
                return 'o';
            case KeyCode.P:
                return 'p';
            case KeyCode.Q:
                return 'q';
            case KeyCode.R:
                return 'r';
            case KeyCode.S:
                return 's';
            case KeyCode.T:
                return 't';
            case KeyCode.U:
                return 'u';
            case KeyCode.V:
                return 'v';
            case KeyCode.W:
                return 'w';
            case KeyCode.X:
                return 'x';
            case KeyCode.Y:
                return 'y';
            case KeyCode.Z:
                return 'z';
            case KeyCode.Alpha0:
                return '0';
            case KeyCode.Alpha1:
                return '1';
            case KeyCode.Alpha2:
                return '2';
            case KeyCode.Alpha3:
                return '3';
            case KeyCode.Alpha4:
                return '4';
            case KeyCode.Alpha5:
                return '5';
            case KeyCode.Alpha6:
                return '6';
            case KeyCode.Alpha7:
                return '7';
            case KeyCode.Alpha8:
                return '8';
            case KeyCode.Alpha9:
                return '9';
            case KeyCode.Minus:
                return '-';
            case KeyCode.Caret:
                return '^';
            case KeyCode.Backslash:
                return '\\';
            case KeyCode.At:
                return '@';
            case KeyCode.LeftBracket:
                return '[';
            case KeyCode.Semicolon:
                return ';';
            case KeyCode.Colon:
                return ':';
            case KeyCode.RightBracket:
                return ']';
            case KeyCode.Comma:
                return ',';
            case KeyCode.Period:
                return '.';
            case KeyCode.Slash:
                return '/';
            case KeyCode.Underscore:
                return '_';
            case KeyCode.Backspace:
                return '\b';
            case KeyCode.Return:
                return '\r';
            case KeyCode.Space:
                return ' ';
            default: //上記以外のキーが押された場合は「null文字」を返す。
                return '\0';
        }
    }

    void SliderUpdate()
    {
        var gageTransform = GameObject.Find("gagecolor").gameObject.GetComponent<Transform>();

        _scoreGAGE = 4.5f * (float)_scoreGOOD / (float)_scoreAll;//4.5 is correction

        Vector3 worldPos = gageTransform.position; ;
        worldPos.y = _scoreGAGE / 1.18f;

        Vector3 localScale = gageTransform.localScale;
        localScale.y = _scoreGAGE;

        gageTransform.position = worldPos;
        gageTransform.localScale = localScale;
    }

    void GameStopMenu()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            if (Time.timeScale == 1)
            {
                Time.timeScale = 0;
                audioSource.Pause();
                canvas.SetActive(true);
            }
            else if (Time.timeScale == 0)
            {
                Time.timeScale = 1;
                audioSource.Play();
                canvas.SetActive(false);
            }
        }
    }
}