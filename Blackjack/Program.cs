using System;
using System.Security.Cryptography;
using System.Threading.Tasks.Dataflow;

namespace blackjack
{
    class Program
    {
        static void Main(string[] args)
        {
            int bank = 100;

            Console.WriteLine("Let's play a little game of Blackjack.");
            Console.WriteLine("Your wife has noted that you only have 100 dollars available for this evening.");
            Console.WriteLine("To play the game of Blackjack, you have to bet at least 1 dollar.");
            Console.WriteLine("You can quit game at any point by adding Q to console when it asks for your bet");
            Console.WriteLine("\nLet's start!");
        
            while (bank>0)
            {
                List<string> userhand = new List<string>();
                List<string> dealerhand = new List<string>();
                int userpoints = 0, dealerpoints = 0, wager = 0;

                Console.Clear();
                Console.WriteLine("\nPlace your bet!");
                Console.WriteLine($"Bank balance = {bank}");
                string bet = Console.ReadLine();
                
                if (bet == "Q")
                    endgame(bank);

                if (!int.TryParse(bet, out int r)||int.Parse(bet)<0 ||int.Parse(bet)>bank)
                {
                    Console.WriteLine("Please add a valid bet or add Q to end game!");
                    continue;
                }

                wager = int.Parse(bet);

                userhand.Add(takecard().Item1);
                userhand.Add(takecard().Item1);
                userpoints = calculatescore(userhand);

                dealerhand.Add(takecard().Item1);
                dealerpoints = calculatescore(dealerhand);

                showcards(userhand,dealerhand,userpoints,dealerpoints);

                if (userpoints ==21)
                {
                    wager = (int)(Math.Ceiling(wager*1.5));
                    bank += wager;
                    Console.WriteLine($"Congratulations! Blackjack, you have won {wager}, bank balance {bank}");
                    continue;
                }

                while(true)
                {
                    Console.WriteLine("Hit (H), Stay (S) or Double(D)?");
                    string input = Console.ReadLine();

                    if (input!="H" && input!="S" && input!="D")
                    {
                        Console.WriteLine("Please add a valid input!");
                        continue;
                    }
                    else if (input=="H")
                    {
                        userhand.Add(takecard().Item1);
                        userpoints = calculatescore(userhand);
                        showcards(userhand,dealerhand,userpoints,dealerpoints);

                        if (userpoints>21)
                            break;
                    }
                    else if (input=="D")
                    {
                        if (wager*2>bank)
                        {
                            Console.WriteLine("Insufficient bank balance");
                            continue;
                        }
                        wager *=2;
                        userhand.Add(takecard().Item1);
                        userpoints = calculatescore(userhand);
                        showcards(userhand,dealerhand,userpoints,dealerpoints);
                        break;
                    }
                    else
                        break;
                }

                if (userpoints>21)
                {
                    bank -= wager;
                    Console.WriteLine($"You went bust! You lost {wager}, current bank balance {bank}");
                    continue;
                }

                Console.WriteLine("\nDealers turn:");
                while (dealerpoints<=16)
                {
                    dealerhand.Add(takecard().Item1);
                    dealerpoints = calculatescore(dealerhand);
                }

                showcards(userhand,dealerhand,userpoints,dealerpoints);

                if (dealerpoints>21)
                {
                    bank += wager;
                    Console.WriteLine($"Dealer went bust! You have won {wager}, current bank balance {bank}");
                    continue;
                }

                if (userpoints > dealerpoints)
                { 
                    bank += wager;
                    Console.WriteLine($"You won {wager}, current bank balance {bank}");
                }
                else if (userpoints == dealerpoints)
                { 
                    Console.WriteLine($"It's a tie, current bank balance {bank}");
                }
                else
                {
                    bank -= wager;
                    Console.WriteLine($"You lost {wager}, current bank balance {bank}");
                }
            if (bank ==0)
                Console.WriteLine("Thank you for playing, you can't continue as you are out of money.");
            }
        }
        public static (string, int) takecard()
        {
            string[] cards = new string[] {"2","3","4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"};
            var rndMember = cards[RandomNumberGenerator.GetInt32(cards.Length)];
            int score = 0;
            if (int.TryParse(rndMember, out int result))
                score = int.Parse(rndMember);
            else if (rndMember == "A")
                score = 11;
            else
                score = 10;

            return (rndMember, score);
        }

        public static void endgame(int bank)
        {
            Console.WriteLine("Thank you for playing.");
                if (bank > 100)
                    Console.WriteLine($"You have won {bank-100} dollars and walk away with {bank} dollars!");
                else if (bank == 100)
                    Console.WriteLine($"You have the same balance as you started with - {bank}!");
                else
                    Console.WriteLine($"You have lost {100-bank} dollars and walk away with {bank} dollars");
            Console.ReadKey();
            Environment.Exit(0);
        }

        public static void showcards(List<string> userhand, List<string> dealerhand, int userpoints, int dealerpoints)
        {
            Console.WriteLine($"You    :  {String.Join(" ", userhand)}  ({userpoints})");
            Console.WriteLine($"Dealer :  {String.Join(" ", dealerhand)}  ({dealerpoints})");
        }

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
                    scores[i] = int.Parse(a[i]);
            }
            while (scores.Sum() > 21 && Array.IndexOf(scores,11)!=-1)
                scores[Array.IndexOf(scores,11)] = 1;

            return scores.Sum();
        }
    }
}
