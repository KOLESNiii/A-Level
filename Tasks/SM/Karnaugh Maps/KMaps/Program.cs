using System.Collections;
using System.Collections.Generic;
using System.Linq;
using KMap;

namespace Program
{
    class ProgramMain
    {
        public static void Main(string[] args)
        {
            string letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
            List<string> values = new List<string>{"0000", "0001", "0100", "0101", "1100", "1101", "1000", "1001", "0010", "0110", "1010"};            
            if (!Validation.IsSameLength(values))
            {
                throw new Exception("All inputs must be the same number of bits");
            }
            else if (!Validation.IsWithinRange(values, letters.Length))
            {
                throw new Exception("Inputs must be smaller than number of letters denoting inputs");
            }
            
            var finalGroups = new List<Group>();
            var groups = Group.MakeGroups(values);
            groups = Simplifier.Combine(groups);
            foreach (Group g in groups)
            {
                Console.WriteLine(g.Value);
            }
            Console.WriteLine("\n");
            List<int> allPrimeImplicants = new List<int>();
            bool primeImplicantsLeft = true;
            foreach (Group g in groups)
                {
                    allPrimeImplicants.AddRange(g.Minterms);
                }
            int essentialPrimeImplicant;
            while (primeImplicantsLeft)
            {
                var essentialPrimeImplicants = allPrimeImplicants.GroupBy(i => i).Where(m => m.Count() == 1).Select(m => m.First()).ToList();
                if (essentialPrimeImplicants.Count() == 0)
                {
                    primeImplicantsLeft = false;
                    break;
                }
                else
                {
                    essentialPrimeImplicant = essentialPrimeImplicants[0];
                }
                foreach (Group g in groups)
                {
                    if (g.Minterms.Contains(essentialPrimeImplicant))
                    {
                        finalGroups.Add(g);
                        groups.Remove(g);
                        allPrimeImplicants = allPrimeImplicants.Where(m => !g.Minterms.Contains(m)).ToList();
                        break;
                    }
                }
            }
            if (allPrimeImplicants.Count() > 0)
            {
                finalGroups.Add(groups[0]);
            }
            //allPrimeImplicants = allPrimeImplicants.Distinct().ToList();
            foreach (Group g in finalGroups)
            {
                Console.WriteLine(g.Value);
            }
            Console.WriteLine(Simplifier.GenerateOutputString(finalGroups, letters));
        }
    }

    static class Validation
    {
        public static bool IsSameLength(List<string> values)
        {
            var current = values[0];
            foreach (string s in values)
            {
                if (s.Length != current.Length)
                {
                    return false;
                }
                else
                {
                    current = s;
                }
            }
            return true;
        }

        public static bool IsWithinRange(List<string> values, int maxValue)
        {
            if (maxValue < values[0].Length)
            {
                return false;
            }
            return true;
        }
    }

}
