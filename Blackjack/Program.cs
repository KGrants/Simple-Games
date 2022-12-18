using System;
using System.Security.Cryptography;
using System.Threading.Tasks.Dataflow;
using static blackjack.Actions;

namespace blackjack
{
    class Program
    {
        static void Main(string[] args)
        {

            Console.WriteLine("Let's play a little game of Blackjack.");

            ///Next line gets and validates budget from player.
            int bank = getbudget();  
            /// Will be used for calculating end results.
            int startbank = bank;
                            
            Console.WriteLine($"Your budget is {bank} dollars.");
            Console.WriteLine("To play a round of Blackjack, you have to bet at least 1 dollar.");
            Console.WriteLine("You can quit game at any point by adding Q to console when it asks for your bet.");

            /// Here starts the game
            while (bank>0)
            {
                Console.WriteLine("\nPlace your bet! (Q to quit)");
                Console.WriteLine($"Bank balance = {bank}");

                List<string> userhand = new List<string>();
                List<List<string>> alluserhands = new List<List<string>>();
                List<string> dealerhand = new List<string>();
                int wager = 0;
                string? bet = Console.ReadLine();
                Console.Clear();
                
                /// if Q, quit game,calculate and show results.
                if (bet == "Q")
                    endgame(bank, startbank);

                /// if input is not valid jump to next iteration of while loop
                if (!int.TryParse(bet, out int rr)||int.Parse(bet)<=0 ||int.Parse(bet)>bank)
                {
                    Console.WriteLine("Please add a valid bet or Q to quit the table!");
                    continue;
                }

                /// assign bet to wager to use as int
                wager = rr;

                /// This part get initial cards for player and dealer, calculates scores and shows both.
                userhand.Add(takecard());
                userhand.Add(takecard());
                dealerhand.Add(takecard());

                Console.WriteLine($"Your bet = {wager}, bank balance = {bank}");
                showcards(userhand,dealerhand,calculatescore(userhand),calculatescore(dealerhand));

                /// If player has blackjack, this round is over, dealer pays 1,5 times bet and goes to next while iteration
                if (calculatescore(userhand) == 21)
                {
                    wager = (int)(Math.Ceiling(wager*1.5));
                    bank += wager;
                    Console.WriteLine($"Congratulations! Blackjack, you have won {wager}, bank balance {bank}");
                    continue;
                }

                /// If there is no blackjack, we need further input from player
                while(true)
                {
                    /// Next line asks for player action, validates it and assigns to input
                    string input = getandvalidateinput();

                    /// If player wants to "STAY", we break loop and continue with dealer turns and results.
                    if (input == "S")
                    { 
                        alluserhands.Add(userhand);
                        break;    
                    }


                    /// If "HIT" then we add another card on the table, calculate scores and show latest situation
                    else if (input=="H")
                    {
                        userhand.Add(takecard());
                        showcards(userhand,dealerhand,calculatescore(userhand),calculatescore(dealerhand));

                        /// If userpoints goes over 21 then it's a bust - round is over for player.
                        if (calculatescore(userhand)>21)
                        { 
                            alluserhands.Add(userhand);
                            break;
                        }
                    }

                    /// If player wants to "DOUBLE" we double wager, add one card and break loop.
                    else if (input=="D")
                    {   
                        ///Validates if user has enough balance for this action
                        if (wager*2>bank)
                        {
                            Console.WriteLine("Insufficient bank balance");
                            continue;
                        }
                        wager *=2;
                        userhand.Add(takecard());
                        showcards(userhand,dealerhand,calculatescore(userhand),calculatescore(dealerhand));
                        alluserhands.Add(userhand);
                        break;
                        
                    }

                    /// if player wants to "SPLIT" -- this part I'm still working on
                    else if (input=="X")
                    {
                        ///Validates if user has enough balance for this action 
                        if (wager*2>bank)
                        {
                            Console.WriteLine("Insufficient bank balance");
                            continue;
                        }
                        ///Validates if both cards are of the same value.
                        if (calculatescore(userhand[0]) != calculatescore(userhand[1]))
                        {
                            Console.WriteLine("You can only split your hand if your initial two-card hand includes two cards of the same value!");
                            continue;
                        }

                        /// This is the moment we split both cards into two lists
                        List<string> userhand2 = new List<string>() {userhand.ElementAt(1)};
                        userhand.Remove(userhand.ElementAt(1));

                        Console.Clear();

                        Console.WriteLine($"Your bet is {wager} for each hand ({wager*2} in total), bank balance {bank}");
                        Console.WriteLine($"First hand    :  {String.Join(" ", userhand)}  ({calculatescore(userhand)})");
                        Console.WriteLine($"Second hand   :  {String.Join(" ", userhand2)}  ({calculatescore(userhand2)})");

                        /// Creating list of lists to use foreach after
                        List<List<string>> bothhands = new List<List<string>>() {userhand,userhand2};

                        foreach(List<string> hand in bothhands)
                        {
                            while(true)
                            {
                                Console.WriteLine($"\nHand at play: {String.Join(" ", hand)}  ({calculatescore(hand)})");
                                input = getandvalidateinputaftersplit();

                                if (input == "S")
                                    break;

                                else if (input=="H")
                                {
                                    hand.Add(takecard());
                                    showcards(hand,dealerhand,calculatescore(hand),calculatescore(dealerhand));

                                    /// If userpoints goes over 21 then it's a bust - round is over for player.
                                    if (calculatescore(hand)>21)
                                        break;
                                }

                                /// If player wants to "DOUBLE" we double wager, add one card and break loop.
                                else if (input=="D")
                                {   
                                    ///Validates if user has enough balance for this action
                                    if ((wager*bothhands.Count()) + wager>bank)
                                    {
                                        Console.WriteLine("Insufficient bank balance");
                                        continue;
                                    }
                                    wager *=2; ///// How to get back to wager if first hand was double and second was just a hit or stand
                                    hand.Add(takecard());
                                    showcards(hand,dealerhand,calculatescore(hand),calculatescore(dealerhand));
                                    break;
                                }
                            }
                            alluserhands.Add(hand);
                        }
                        break;
                    }
                }

                /// Dealers turn to pick up cards, dealer has to HIT on <17 and STAY on >=17.
                Console.WriteLine("\nDealers turn:");

                while (calculatescore(dealerhand)<=16)
                    dealerhand.Add(takecard());


                /// Start to evaluate player hand(s) against dealer hand
                foreach (List<string> hand in alluserhands)
                { 
                /// If player has more than 21, he has lost, take wager from bank, display results.
                if (calculatescore(userhand)>21)
                {
                    bank -= wager;
                    Console.WriteLine($"You went bust on hand {String.Join(" ", hand)}. You lost {wager}, current bank balance {bank}");
                    continue;
                }

                showcards(hand,dealerhand,calculatescore(hand),calculatescore(dealerhand));

                /// If dealer went bust, player has won, add wager to bank and display result.
                if (calculatescore(dealerhand)>21)
                {
                    bank += wager;
                    Console.WriteLine($"Dealer went bust! You have won {wager} for {String.Join(" ", hand)} hand, current bank balance {bank}");
                    continue;
                }

                ///If both are in the game at this point compare results and make an impact on the bank
                bank += getresults(calculatescore(hand), calculatescore(dealerhand), wager, bank);

                /// If player is out of money, go to endgame and show results.
                if (bank ==0)
                    endgame(bank, startbank);
                }
            }
        }
    }
}
