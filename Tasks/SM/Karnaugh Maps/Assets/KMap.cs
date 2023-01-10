using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System;

/*
By T. Kolesnichenko 2022
Implementation of Quine McCluskey method for simplifying boolean expressions
*/
namespace KMap
{
    //Simple class for storing the data for a group, such as its implicant value, number of 1s and whether it was merged or not
    public class Group
    {
        public Group(string value)
        {
            Value = value;
            NumOnes = value.Count(v => v.ToString() == "1");
        }

        public Group(string value, int minterm)
        {
            Value = value;
            NumOnes = value.Count(v => v.ToString() == "1");
            Minterms.Add(minterm);
        }
        public string Value;
        public int NumOnes;
        public bool Merged = false;
        public List<int> Minterms = new List<int>();

        public static List<Group> MakeGroups(List<string> values)
        {
            List<Group> groups = new List<Group>();
            foreach (string v in values)
            {
                groups.Add(new Group(v, ConvertBinToDen(v)));
            }
            return groups;
        }

        //simple converter, so that comparing minterms is easier
        private static int ConvertBinToDen(string binary)
        {
            int output = 0;
            var binaryArray = binary.Select(s => int.Parse(s.ToString())).ToList();
            for (int i = binaryArray.Count-1; i >= 0; i--)
            {
                output += binaryArray[i]*(int)(Math.Pow(2, binaryArray.Count-1-i));
            }
            return output;
        }
    }

    
    public static class Simplifier
    {
        //iteratiely produces the largest groups possible
        public static List<Group> ReduceToPrimeImplicants(List<Group> groups)
        {
            List<Group> newGroups = new List<Group>(); //initialising lists 
            List<Group> finalGroups = new List<Group>();
            bool finished = false;
            while (!finished)
            {
                foreach (Group group in groups.OrderBy(g => g.NumOnes)) //iterates through each group 
                {
                    //iterates through each group where the number of ones is exactly one greater, as you can only have 1-bit changes if the number of 1s is one apart
                    foreach (Group possibleGroup in groups.Where(g => g.NumOnes == group.NumOnes + 1)) 
                    {
                        //iterates through every bit of a group, to see if the two groups can merge
                        for (int i = 0; i < group.Value.Length; i++)
                        {
                            //attempting to place a blank
                            var tempString = ReplaceChar(group.Value, "-", i);
                            var possibleTempString = ReplaceChar(possibleGroup.Value, "-", i);
                            //if the two strings are the same, it means there is only a 1-bit difference between them
                            if (CompareStrings(tempString, possibleTempString))
                            {
                                //if the group has not been created yet, this is checked to prevent any repetition
                                if (newGroups.Where(g => g.Value == tempString).Count() == 0)
                                {
                                    newGroups.Add(new Group(tempString));
                                }
                                //sets both groups' merged flags to true
                                group.Merged = true;
                                possibleGroup.Merged = true;
                                //adds the minterms of the smaller groups and combines them into the larger group, ensuring there are no duplicates
                                foreach (Group workingGroup in newGroups.Where(g => g.Value == tempString))
                                {
                                    workingGroup.Minterms.AddRange(group.Minterms.Where(m => !workingGroup.Minterms.Contains(m)).ToList());
                                    workingGroup.Minterms.AddRange(possibleGroup.Minterms.Where(m => !workingGroup.Minterms.Contains(m)).ToList());
                                }
                            }
                        }
                    }
                }
                //if a group could not be merged, it means it is necessary, so is added straight to the final list
                foreach (Group g in groups.Where(g => g.Merged == false))
                {
                    finalGroups.Add(g);
                }
                //if no merges occur, that means that the groups can not be combined any further
                if (newGroups.Count() == 0)
                {
                    finished = true;
                }
                //clones to main list, so that next iteration works using the newly created groups
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
                ANDGroups.Add(GenerateBooleanANDGroup(g.Value, letters));
            }
            return string.Join(" + ", ANDGroups); //adds OR gates between the groups of AND
        }

        //converts the prime implicants format into a boolean expression
        private static string GenerateBooleanANDGroup(string value, string letters)
        {
            string output = String.Empty;
            if (value == "x0")
            {
                return "0";
            }
            else if (value == "x1")
            {
                return "1";
            }
            for (int i = 0; i < value.Length; i++)
            {
                string c = value[i].ToString();
                //"-" indicates an input that is not relevant, so is ommitted
                if (c == "-") 
                {
                    continue;
                }
                output += letters[i];
                //if value is 0, that variable is meant to be off, so would give a logical on when a not gate is applied to it
                if (c == "0")
                {
                    output += "'";
                }
            }
            return output;
        }
        private static List<int> GenerateAllMintermsList(List<Group> groups)
        {
            List<int> allPrimeImplicants = new List<int>();
            foreach (Group g in groups)
            {
                allPrimeImplicants.AddRange(g.Minterms);
            }
            return allPrimeImplicants;
        }
        public static List<Group> FilterRedundantExpressions(List<Group> groups)
        {
            var finalGroups = new List<Group>();
            bool essentialMintermsLeft = true;
            bool first = true;
            int essentialMinterm;
            List<int> allMinterms = GenerateAllMintermsList(groups);

            while (essentialMintermsLeft)
            {
                //gets all minterms covered by only one prime implicant
                var essentialMinterms = allMinterms.GroupBy(i => i).Where(m => m.Count() == 1).Select(m => m.First()).ToList(); 
                if (essentialMinterms.Count() == 0)
                {
                    essentialMintermsLeft = false;
                    //If clause, as some instances can occur when there are no essential minterms left, and all are covered by several implicants
                    if (first == true)
                    {
                        finalGroups = GetLowestExpressions(groups, allMinterms);
                        allMinterms.Clear();
                    }
                    break;
                }
                else
                {
                    //Goes through to the next essential minterm
                    essentialMinterm = essentialMinterms[0];
                }
                //Finds the implicant that covers the essential minterm
                foreach (Group g in groups)
                {
                    if (g.Minterms.Contains(essentialMinterm))
                    {
                        finalGroups.Add(g);
                        groups.Remove(g);
                        //Removes the minterms covered by this implicant
                        allMinterms = allMinterms.Where(m => !g.Minterms.Contains(m)).ToList();
                        break; //prevents unncessary iterations
                    }
                }
                first = false;
            }
            //Removes duplicate minterms, if any
            allMinterms = allMinterms.Distinct().ToList();
            //iterates until the number of minterms left is 0, happens when all remaining minterms are covered by several implicants
            while (allMinterms.Count() > 0)
            {
                //repeats the above process but for non-essential minterms
                var targetMinterm = allMinterms[0];
                foreach (Group g in groups)
                {
                    if (g.Minterms.Contains(targetMinterm))
                    {
                        finalGroups.Add(g);
                        groups.Remove(g);
                        allMinterms = allMinterms.Where(m => !g.Minterms.Contains(m)).ToList();
                        break;
                    }
                }
            }

            return finalGroups;
        }
        //uses the random class to try to get the lowest number of expressions by selecting random implicants, when there are no essential minterms
        private static List<Group> GetLowestExpressions (List<Group> groups, List<int> allMinterms)
        {
            List<Group> fewestGroups = groups.ToList(); //copies of lists
            List<Group> possibleFewestGroups = new List<Group>();
            var rand = new Random();
            for (int i = 0; i < 1000; i++) //iterates through 1000 times
            {   
                possibleFewestGroups.Clear();
                var groupsCopy = groups.ToList();
                var allMintermsCopy = allMinterms.ToList();
                //same process as previous, but slight change as now there is a target group, not target minterm
                while (allMintermsCopy.Count() > 0)
                {
                    var g = groupsCopy[rand.Next(groupsCopy.Count()-1)];
                    possibleFewestGroups.Add(g);
                    groupsCopy.Remove(g);
                    allMintermsCopy = allMintermsCopy.Where(m => !g.Minterms.Contains(m)).ToList();
                }
                if (possibleFewestGroups.Count() < fewestGroups.Count())
                {
                    fewestGroups = possibleFewestGroups.ToList();
                }
            }
            return fewestGroups;
        }

        //wrapper method for simplification
        public static List<Group> Simplify(List<string> values)
        {
            var groups = new List<Group>();
            if (values.Count() == 0)
            {
                groups = new List<Group>{new Group("x0")};
            }
            else if (values.Count() == Math.Pow(2,values[0].Length))
            {
                groups = new List<Group>{new Group("x1")};
            }
            else {
                groups = Group.MakeGroups(values);
                groups = ReduceToPrimeImplicants(groups);
                
                groups = FilterRedundantExpressions(groups);
            }
            return groups;

        }
    }
}
