using System;

namespace Safe
{
    public static class Game
    {
        static Game()
        {
            Lives = 10;
            Numbers = new int[20];
            NumbersGuessed = new int[20];
            for (int i = 0; i < 20; i++)
            {
                Numbers[i] = i + 1;
            }
            Codes = new Locks[6];
            for (int i = 0; i < 6; i++)
            {
                Codes[i] = new Locks();
            }
        }
        public static void Reset()
        {
            Locks.Reset();
            Lives = 10;
            Numbers = new int[20];
            NumbersGuessed = new int[20];
            for (int i = 0; i < 20; i++)
            {
                Numbers[i] = i + 1;
            }
            Codes = new Locks[6];
            for (int i = 0; i < 6; i++)
            {
                Codes[i] = new Locks();
            }
        }
        public static int Lives
        {get; private set;}
        public static int[] Numbers
        {get; private set;}
        public static int[] NumbersGuessed
        {get; private set;}
        private static Locks[] Codes
        {get; set;}

        public static void Play()
        {
            Random rand = new Random();
            bool running = true;
            while (running)
            {
                Console.WriteLine($"\n\nKnown codes: {GenerateKnownCodesString()}");
                Console.WriteLine($"Available codes to guess: {GenerateNumberString()}");
                Console.WriteLine($"Attempts left: {Lives}");
                Console.WriteLine($"Locks left to open: {CodesLeftToGuess()}\n\n");
                int guess = GetGuess();
                NumbersGuessed[Array.IndexOf(NumbersGuessed, 0)] = guess;
                if (!CheckGuess(guess))
                {
                    Console.WriteLine($"{guess} did not work for any of the locks");
                }
                Lives --;
                string gameState = GetGameState();
                if (gameState == "WIN")
                {
                    Console.WriteLine($"You have cracked all the codes\nThe contents of the safe are yours\nYou found £{rand.Next(10000000)+Math.Round(rand.NextDouble(), 2)} worth of gold");
                    running = false;
                }
                else if(gameState == "LOSS")
                {
                    Console.WriteLine($"You have failed to crack all the codes\nYou will never know what the contents of the safe were\nIf only you unlocked those {CodesLeftToGuess()} locks");
                    running = false;
                }
            }

        }
        static int GetGuess()
        {
            Console.WriteLine("Enter an integer between 1 and 20 inclusive");
            int numericalGuess = -1;
            while (true)
            {
                string input = Console.ReadLine();
                if (string.IsNullOrWhiteSpace(input))
                {
                    //throw new ArgumentNullException(nameof(input), "Input numbers only");
                    Console.WriteLine("Input only numbers");
                    continue;
                }
                else if (!Int32.TryParse(input, out numericalGuess))
                {
                    //throw new ArgumentException(nameof(input), "Input only numbers");
                    Console.WriteLine("Input only numbers");
                    continue;
                }
                else if (numericalGuess < 0 || numericalGuess > 20)
                {
                    //throw new ArgumentOutOfRangeException(nameof(input), "Enter a number between 1 and 20 inclusive only");
                    Console.WriteLine("Enter a number between 1 and 20 inclusive only");
                    continue;
                }
                else if (Array.IndexOf(NumbersGuessed, numericalGuess) != -1)
                {
                    Console.WriteLine("Input a number you have not tried before");
                    continue;
                }
                else
                {
                    return numericalGuess;
                }
            }
        }

        static bool CheckGuess(int guess)
        {
            bool isNew = false;
            foreach (Locks code in Codes)
            {
                if (code.CheckGuess(guess))
                {
                    Console.WriteLine($"{guess} unlocked lock {code.CodeNumber}");
                    isNew = true;
                }
            }
            return isNew;
        }

        static string GenerateKnownCodesString()
        {
            string output = "";
            foreach (Locks code in Codes)
            {
                output += (code.Guessed == true) ? code.Value : "__";
                output += " ";
            }
            return output;
        }
        static string GenerateNumberString()
        {
            string output = "";
            foreach (int number in Numbers)
            {
                output += (Array.IndexOf(NumbersGuessed, number) == -1) ? number : "  ";
                output += " ";
            }
            
            return output;
        }

        static string GetGameState()
        {
            if (CodesLeftToGuess() == 0)
            {
                return "WIN";
            }
            else if (Lives == 0)
            {
                return "LOSS";
            }
            else
            {
                return "PLAY ON";
            }
        }


        static int CodesLeftToGuess()
        {
            int total = 0;
            foreach (Locks code in Codes)
            {
                total += code.Guessed == false ? 1 : 0;
            }
            return total;
        }
   
    }
}