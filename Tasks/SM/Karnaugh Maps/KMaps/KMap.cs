using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System;

namespace KMap
{
    public class Group
    {
        public Group(string value, bool temp = false)
        {
            Value = value;
            Temp = temp;
            NumOnes = value.Count(v => v.ToString() == "1");
        }
        public string Value;
        bool Temp;
        public int NumOnes;
        public bool Merged = false;
        public List<int> Minterms = new List<int>();

        public static List<Group> MakeGroups(List<string> values)
        {
            List<Group> groups = new List<Group>();
            for (int i = 0; i < values.Count(); i++)
            {
                groups.Add(new Group(values[i]));
                groups[i].Minterms.Add(ConvertBinToDen(values[i]));
            }
            return groups;
        }

        public static int ConvertBinToDen(string binary)
        {
            int output = 0;
            binary = Reverse(binary);
            var binaryArray = binary.Select(s => int.Parse(s.ToString())).ToList();
            for (int i = 0; i < binary.Length; i++)
            {
                output += binaryArray[i]*(int)(Math.Pow(2, i));
            }
            return output;
        }

        public static string Reverse(string s)
        {
            char[] charArray = s.ToCharArray();
            Array.Reverse(charArray);
            return new string(charArray);
        }
    }

    
    public static class Simplifier
    {
        public static List<Group> Combine(List<Group> groups)
        {
            List<Group> newGroups = new List<Group>();
            bool finished = false;
            List<Group> finalGroups = new List<Group>();
            while (!finished)
            {
                var originalNumGroups = groups.Count();
                foreach (Group group in groups.OrderBy(g => g.NumOnes))
                {
                    foreach (Group possibleGroup in groups.Where(g => g.NumOnes == group.NumOnes + 1))
                    {
                        for (int i = 0; i < group.Value.Length; i++)
                        {
                            var tempString = ReplaceChar(group.Value, "-", i);
                            var possibleTempString = ReplaceChar(possibleGroup.Value, "-", i);
                            if (CompareStrings(tempString, possibleTempString))
                            {
                                if (newGroups.Where(g => g.Value == tempString).Count() == 0)
                                {
                                    newGroups.Add(new Group(tempString));
                                }
                                group.Merged = true;
                                possibleGroup.Merged = true;
                                foreach (Group workingGroup in newGroups.Where(g => g.Value == tempString))
                                {
                                    workingGroup.Minterms.AddRange(group.Minterms.Where(m => !workingGroup.Minterms.Contains(m)).ToList());
                                    workingGroup.Minterms.AddRange(possibleGroup.Minterms.Where(m => !workingGroup.Minterms.Contains(m)).ToList());
                                }
                            }
                        }
                    }
                }
                foreach (Group group in groups.Where(g => g.Merged == false))
                {
                    finalGroups.Add(group);
                }
                if (newGroups.Count() == 0)
                {
                    finished = true;
                }
                groups = newGroups.ToList();
                newGroups.Clear();

            }
            return finalGroups;
        }

        private static string ReplaceChar(string sourceStr, string toReplace, int index)
        {
            sourceStr = sourceStr.Remove(index, 1);
            sourceStr = sourceStr.Insert(index, toReplace);
            return sourceStr;
        }

        private static bool CompareStrings(string str1, string str2)
        {
            if (str1.Length != str2.Length)
            {
                return false;
            }
            for (int i = 0; i < str1.Length; i++)
            {
                if (str1[i] != str2[i])
                {
                    return false;
                }
            }
            return true;
        }

        public static string GenerateOutputString(List<Group> groups, string letters)
        {
            List<string> ANDGroups = new List<string>();
            foreach (Group g in groups)
            {
                ANDGroups.Add(GenerateANDGroup(g.Value, letters));
            }
            return string.Join(" + ", ANDGroups);
        }

        private static string GenerateANDGroup(string value, string letters)
        {
            string output = String.Empty;
            for (int i = 0; i < value.Length; i++)
            {
                string c = value[i].ToString();
                if (c == "-")
                {
                    continue;
                }
                output += letters[i];
                if (c == "0")
                {
                    output += "'";
                }
            }
            return output;
        }
    }
}
