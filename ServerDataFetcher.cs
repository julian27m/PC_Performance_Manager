using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using TMPro;

[System.Serializable]
public class ComputerDynamicData
{
    public string CPUUsage;
    public string RAMUsage;
    public string DiskUsage;
}

public class ServerDataFetcher : MonoBehaviour
{
    public TextMeshPro cpuTextMesh; // Reference to the TextMeshPro object for CPU
    public TextMeshPro ramTextMesh; // Reference to the TextMeshPro object for RAM
    public TextMeshPro diskTextMesh; // Reference to the TextMeshPro object for Disk

    void Start()
    {
        StartCoroutine(FetchData());
    }

    IEnumerator FetchData()
    {
        while (true) // Continuously fetch data
        {
            using (UnityWebRequest webRequest = UnityWebRequest.Get("http://157.253.192.187:8000/data"))
            {
                yield return webRequest.SendWebRequest();

                if (webRequest.result == UnityWebRequest.Result.Success)
                {
                    string jsonData = webRequest.downloadHandler.text;

                    // Parse the JSON data into a ComputerDynamicData object
                    ComputerDynamicData computerData = JsonUtility.FromJson<ComputerDynamicData>(jsonData);

                    // Update the TextMeshPro objects with the parsed data
                    cpuTextMesh.text = "CPU Usage: " + computerData.CPUUsage;
                    ramTextMesh.text = "RAM Usage: " + computerData.RAMUsage;
                    diskTextMesh.text = "Disk Usage: " + computerData.DiskUsage;
                }
                else
                {
                    Debug.LogError("Error fetching data: " + webRequest.error);
                }
            }

            yield return new WaitForSeconds(5f); // Refresh rate
        }
    }
}
