using System;

namespace Safe
{
    class Program
    {
        public static void Main(string[] args)
        {
            bool playOn = true;
            while (playOn)
            {
                Game.Play();
                playOn = PlayAgain();
                Game.Reset();
            }    
        }
        public static bool PlayAgain()
        {
            string input;
            while (true)
            {
                Console.WriteLine("Play Again? (y/n)");
                input = Console.ReadLine();
                if (String.IsNullOrWhiteSpace(input))
                {
                    Console.WriteLine("Enter only y or n");
                    continue;
                }
                else if (input.ToLower() == "y")
                {
                    return true;
                }
                else if (input.ToLower() == "n")
                {
                    return false;
                }
                else
                {
                    Console.WriteLine("Enter only y or n");
                    continue;
                }
            }
        }
    }
}