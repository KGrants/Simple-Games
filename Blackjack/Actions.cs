using System;
using System.Security.Cryptography;
using System.Threading.Tasks.Dataflow;

namespace blackjack
{ 
	public class Actions
	{	
        ///Used to add cards to the table
		public static string takecard()
        {
            string[] cards = new string[] {"2","3","4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"};
            var rndMember = cards[RandomNumberGenerator.GetInt32(cards.Length)];
            return rndMember;
        }

        ///Used to calculate results when game is over (if player ran out of money or pressed Q)
        public static void endgame(int bank, int startbank)
        {
            Console.WriteLine("Thank you for playing.");
                if (bank > startbank)
                    Console.WriteLine($"You have won {bank-startbank} dollars and walk away with {bank} dollars!");
                else if (bank == startbank)
                    Console.WriteLine($"You have the same balance as you started with - {bank}!");
                else
                    Console.WriteLine($"You have lost {startbank-bank} dollars and walk away with {bank} dollars");
            Console.ReadKey();
            Environment.Exit(0);
        }

        ///Used to display the status of the game (not for Split)
        public static void showcards(List<string> userhand, List<string> dealerhand, int userpoints, int dealerpoints)
        {
            Console.WriteLine($"You    :  {String.Join(" ", userhand)}  ({userpoints})");
            Console.WriteLine($"Dealer :  {String.Join(" ", dealerhand)}  ({dealerpoints})");
        }

        ///Used to calculate score based on player or dealer cards
        public static int calculatescore(List<string> a)
        {
            int[] scores = new int[a.Count];
            for (int i = 0; i < a.Count(); i++)
            {
                if (!int.TryParse(a[i], out int r))
                {
                    if (a[i] == "A")
                        scores[i] = 11;
                    else
                        scores[i] = 10;
                }
                else
                    scores[i] = r;
            }
            while (scores.Sum() > 21 && Array.IndexOf(scores,11)!=-1)
                scores[Array.IndexOf(scores,11)] = 1;

            return scores.Sum();
        }

        public static int calculatescore(string a)
        {
            if (!int.TryParse(a, out int r))
                {
                    if (a == "A")
                        return 11;
                    else
                        return 10;
                }
            else
                return r;
        }

        public static int getresults(int userpoints, int dealerpoints, int wager, int bank)
        {
            if (userpoints > dealerpoints) 
                Console.WriteLine($"Congratulations! You won {wager} dollars, current bank balance {bank + wager}");

            else if (userpoints == dealerpoints)
            { 
                Console.WriteLine($"It's a tie, current bank balance {bank}");
                wager = 0;
            }
            else
            {
                Console.WriteLine($"Too bad! You lost {wager}, current bank balance {bank-wager}");
                wager = -wager;
            }
            return wager;
        }

        public static int getbudget()
        {  
            while (true)
            {
                Console.WriteLine("How much did you wife allow you to spend on this game?");
                var input = Console.ReadLine();
                if (!int.TryParse(input, out int r))
                {
                    Console.WriteLine("Please add an integer value to continue;");
                    continue;
                }
                else
                {
                    if (r > 0) 
                        return r;

                    else
                    {
                        Console.WriteLine("We are not handing out any loans here! Please add a valid budget!");
                        continue;
                    }    
                }
            }
        }

        public static string getandvalidateinput()
        {
            while(true)
            { 
                Console.WriteLine("Hit (H), Stand (S), Double(D) or Split(X)?");
                string? input = Console.ReadLine();

                if (input!="H" && input!="S" && input!="D" && input!="X")
                {
                    Console.WriteLine("Please add a valid input!");
                    continue;
                }
                else
                    return input;
            }
        }

        public static string getandvalidateinputaftersplit()
        {
            while(true)
            { 
                Console.WriteLine("Hit (H), Stand (S), or Double(D)?");
                string? input = Console.ReadLine();

                if (input!="H" && input!="S" && input!="D")
                {
                    Console.WriteLine("Please add a valid input!");
                    continue;
                }
                else
                    return input;
            }
        }
	}
}

