using UnityEngine;
using System.Collections;

public class TouchEffectManager : SingletonMonoBehaviour<TouchEffectManager> {

	private GameObject[] _touchEffects;
	AudioClip clip;

	void Start(){
		clip = gameObject.GetComponent<AudioSource>().clip;
		_touchEffects = new GameObject[8];
		for (int i = 0; i < 8; i++) {
			_touchEffects [i] = this.transform.GetChild (i).gameObject;
		}
	}

	void Update()
	{
		for(int i = 0; i < 8; i++ ){
			CheckInput(GameUtil.GetKeyCodeByLineNum(i), i);
		}
	}

	void CheckInput(KeyCode[] key, int num) {
		for (int i = 0; i < key.Length; i++)
		{
            if (Input.GetKeyDown(key[i]))
            {
                PlayEffect(num);
            }
        }
	}

	public void PlayEffect(int num){
		StartCoroutine (TouchEffect (num));
	}

	IEnumerator TouchEffect(int num){
		GetComponent<AudioSource>().PlayOneShot(clip);
		if (_touchEffects [num].activeInHierarchy)
			yield break;
		
		_touchEffects [num].SetActive (true);
		yield return new WaitForSeconds (0.1f);
		_touchEffects [num].SetActive (false);
	}
}
