using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UIElements;
using System.Linq;
using KMap;

public class MainScript : MonoBehaviour
{
    public static List<Box> mapValues = new List<Box>();
    private static List<Button> buttons = new List<Button>();
    public static List<string> values = new List<string>();
    public static Button settingsButton;
    public static RadioButtonGroup bitSelector;

    public static Label outputBox;
    private string letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    // Start is called before the first frame update
    void Start()
    {
        CreateGUI();
    }

    // Update is called once per frame
    void Update()
    {
        string output = string.Empty;
        foreach (Box box in mapValues)
        {
            if (box.State == true)
            {
                output += $"{box.Value} +";
            }
        }
    }

    public static bool CheckActive(VisualElement button)
    {
        foreach (Box box in mapValues) 
        {
            if (box.Value == button.name)
            {
                if (box.State == false)
                {
                    return true;
                }
            }
        }
        return false;
    }

    public static void ToggleButtonState(VisualElement button)
    {
        foreach (Box box in mapValues) 
        {
            if (box.Value == button.name)
            {
                box.State = !box.State;
            }
        }
    }

    public void CreateGUI()
    {
        var root = GetComponent<UIDocument>().rootVisualElement;
        outputBox = root.Query<Label>(className: "OutputBox").First();
        outputBox.text = "0";
        bitSelector = root.Query<RadioButtonGroup>().First();
        bitSelector.BringToFront();
        bitSelector.RegisterCallback<ChangeEvent<int>>(ChangeMenu);
        settingsButton = root.Query<Button>(className: "settings-button").First();
        settingsButton.clicked += () => 
        {
            bitSelector.visible = !bitSelector.visible;
        };
        var buttons = root.Query<Button>(className: "simpleButton");
        buttons.ForEach(SetupButton);
    }

    private void SetupButton(Button button)
    {
        mapValues.Add(new Box(button.name, false, button));
        buttons.Add(button);
        button.style.backgroundImage = Resources.Load<Texture2D>("Off");
        button.clicked += () => {foreach (Box box in mapValues) 
        {
            if (box.Value == button.name)
            {
                box.State = !box.State;
                string addOn;
                if (box.State == true)
                {
                    addOn = "On";
                }
                else
                {
                    addOn = "Off";
                }
                box.LinkedButton.style.backgroundImage = Resources.Load<Texture2D>(addOn);
            }
            values = mapValues.Where(b => b.State == true).Select(b => b.LinkedButton.name).ToList();
            outputBox.text = Simplifier.GenerateOutputString(Simplifier.Simplify(values), letters);

        }
        string str = string.Empty;
        foreach(Box box in mapValues)
        {
            if (box.State)
            {
                str += $"{box.LinkedButton.name} +"; 
            }
        }
        };

    }

    /*private void writeName(RadioButton button)
    {
        button.RegisterValueChangedCallback<int>(ChangeMenu);
    }*/
    private void ChangeMenu(ChangeEvent<int> _)
    {
        mapValues.Clear();
        values.Clear();
        if (bitSelector.value == 0)
        {
            SceneManager.LoadScene(sceneName: "2 Bit");
        }
        else
        {
            SceneManager.LoadScene(sceneName: "4 Bit");

        }
    }
}
public class Box
{
    public Box(string value, bool state, Button button)
    {
        Value = value;
        State = state;
        LinkedButton = button;
    }
    string value;
    public string Value
    {get; set;}
    bool state;
    public bool State
    {get; set;}
    public Button LinkedButton = new Button();

}

