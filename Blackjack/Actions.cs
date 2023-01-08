using System;
using System.Security.Cryptography;
using System.Threading.Tasks.Dataflow;
using static blackjack.Program;

namespace blackjack
{ 
	public class Actions
	{	
        ///Used to calculate results when game is over (if player ran out of money or pressed Q)
        public static void endgame()
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

        ///Used to display the status of the game
        public static void showcards(Hand userhand, Hand dealerhand)
        {
            Console.WriteLine($"You    :  {String.Join(" ", userhand.hand)}  ({userhand.Score})");
            Console.WriteLine($"Dealer :  {String.Join(" ", dealerhand.hand)}  ({dealerhand.Score})");
        }

        ///Used for single card score
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

        ///Used to display results and change balance
        public static void getresults(Hand userhand, int dealerpoints)
        {
            if (userhand.Score > dealerpoints)
            {
                bank += userhand.Wager;
                Console.WriteLine($"Congratulations! You won {userhand.Wager} dollars, current bank balance {bank}");
            }

            else if (userhand.Score == dealerpoints)
            { 
                Console.WriteLine($"It's a tie, current bank balance {bank}");
            }

            else
            {
                bank -= userhand.Wager;
                Console.WriteLine($"Too bad! You lost {userhand.Wager}, current bank balance {bank}");
            }
        }

        ///Used to get valid budget from Player
        public static void getbudget()
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
                    { 
                        bank = r;
                        return;
                    }

                    else
                    {
                        Console.WriteLine("You have to put some of your own money on the table!");
                        continue;
                    }    
                }
            }
        }

        ///Used to get actions for Blackjack game from player
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

        public static string getandvalidatesecondinput()
        {
            while(true)
            { 
                Console.WriteLine("Hit (H) or Stand (S)?");
                string? input = Console.ReadLine();

                if (input!="H" && input!="S")
                {
                    Console.WriteLine("Please add a valid input!");
                    continue;
                }
                else
                    return input;
            }
        }

        public static int getuserbet()
        {
            while(true)
            {
                Console.WriteLine("\nPlace your bet! (Q to quit)");
                Console.WriteLine($"Bank balance = {bank}");

                string? input = Console.ReadLine();
                Console.Clear();
                
                /// if input = Q, quit game, calculate and show results.
                if (input == "Q")
                    endgame();

                /// if input is not valid jump to next iteration of while loop
                if (!int.TryParse(input, out int rr)||int.Parse(input)<=0 ||int.Parse(input)>bank)
                {
                    Console.WriteLine("Please add a valid bet or Q to quit the table!");
                    continue;
                }
                Console.WriteLine($"Your bet = {rr}, bank balance after bet = {bank-rr}");

                return rr;
            }
        }

        ///Used to check if initial hand is blackjack and calculate return if it is
        public static bool blackjackwin(Hand userhand)
        {
            bool win = false;

            if (userhand.Score == 21)
            {
                win = true;
                bank += (int)Math.Ceiling(userhand.Wager*1.5);
                Console.WriteLine($"Congratulations! Blackjack, you have won {(int)Math.Ceiling(userhand.Wager*1.5)}, bank balance {bank}");
            }
            return win;
        }
	}
}