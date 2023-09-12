using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using TMPro;

public class ServerDataFetcher : MonoBehaviour
{
    public TextMeshPro cpuTextMesh; // Reference to your TextMeshPro object for CPU
    public TextMeshPro ramTextMesh; // Reference to your TextMeshPro object for RAM
    public TextMeshPro diskTextMesh; // Reference to your TextMeshPro object for Disk

    void Start()
    {
        StartCoroutine(FetchCPUPercentage());
        StartCoroutine(FetchRAMUsage());
        StartCoroutine(FetchDiskSpace());
    }

    IEnumerator FetchCPUPercentage()
    {
        while (true) // Continuously fetch CPU data
        {
            using (UnityWebRequest webRequest = UnityWebRequest.Get("http://192.168.1.128:8000/cpu"))
            {
                yield return webRequest.SendWebRequest();

                if (webRequest.result == UnityWebRequest.Result.Success)
                {
                    string cpuData = webRequest.downloadHandler.text;
                    // Update your TextMeshPro object with the CPU data
                    cpuTextMesh.text = cpuData;
                }
                else
                {
                    Debug.LogError("Error fetching CPU data: " + webRequest.error);
                }
            }

            yield return new WaitForSeconds(5f); // Adjust the refresh rate as needed
        }
    }

    IEnumerator FetchRAMUsage()
    {
        while (true) // Continuously fetch RAM data
        {
            using (UnityWebRequest webRequest = UnityWebRequest.Get("http://192.168.1.128:8000/ram"))
            {
                yield return webRequest.SendWebRequest();

                if (webRequest.result == UnityWebRequest.Result.Success)
                {
                    string ramData = webRequest.downloadHandler.text;
                    // Update your TextMeshPro object with the RAM data
                    ramTextMesh.text = ramData;
                }
                else
                {
                    Debug.LogError("Error fetching RAM data: " + webRequest.error);
                }
            }

            yield return new WaitForSeconds(5f); // Adjust the refresh rate as needed
        }
    }

    IEnumerator FetchDiskSpace()
    {
        while (true) // Continuously fetch Disk data
        {
            using (UnityWebRequest webRequest = UnityWebRequest.Get("http://192.168.1.128:8000/disk"))
            {
                yield return webRequest.SendWebRequest();

                if (webRequest.result == UnityWebRequest.Result.Success)
                {
                    string diskData = webRequest.downloadHandler.text;
                    // Update your TextMeshPro object with the Disk data
                    diskTextMesh.text = diskData;
                }
                else
                {
                    Debug.LogError("Error fetching Disk data: " + webRequest.error);
                }
            }

            yield return new WaitForSeconds(5f); // Adjust the refresh rate as needed
        }
    }
}
