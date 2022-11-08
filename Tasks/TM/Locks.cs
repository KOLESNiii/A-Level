using System;

namespace Safe
{
    class Locks
    {
        public Locks()
        {
            Random rand = new Random();
            Value = rand.Next(1,20);
            Guessed = false;
            totalCodeNumber ++;
            CodeNumber = totalCodeNumber;

        }

        public int Value
        {get; private set;}
        public bool Guessed
        {get; private set;}
        public int CodeNumber
        {get; private set;}
        private static int totalCodeNumber = 0;

        public bool CheckGuess(int guess)
        {
            if (IsEqual(guess) && Guessed == false)
            {
                Guessed = true;
                return true;
            }
            else
            {
                return false;
            }
        }

        public bool IsEqual(int guess)
        {
            return (guess == Value);
        }
        public static void Reset()
        {
            totalCodeNumber = 0;
        }
    }
}