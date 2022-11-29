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
            List<string> values = new List<string>{"0001","0011","0100","0101","0110","1100","1111","1110","1001","1011"};            
            if (!Validation.IsSameLength(values))
            {
                throw new Exception("All inputs must be the same number of bits");
            }
            else if (!Validation.IsWithinRange(values, letters.Length))
            {
                throw new Exception("Inputs must be smaller than number of letters denoting inputs");
            }

            var groups = Simplifier.Simplify(values);
            Console.WriteLine(Simplifier.GenerateOutputString(groups, letters));
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
